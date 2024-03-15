from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import calendar
import pandas as pd

def scrape_monthly_weather(driver, month, year):
    # URL untuk bulan dan tahun tertentu
    base_url = "https://www.accuweather.com/en/id/jakarta/208971/"
    month_name = calendar.month_name[month].lower()
    url = f"{base_url}{month_name}-weather/208971?year={year}"

    driver.get(url)

    # Get data: tanggal, suhu tinggi, suhu rendah
    dates = driver.find_elements(By.CSS_SELECTOR, ".monthly-calendar .monthly-daypanel .date")
    highs = driver.find_elements(By.CSS_SELECTOR, ".monthly-calendar .monthly-daypanel .high")
    lows = driver.find_elements(By.CSS_SELECTOR, ".monthly-calendar .monthly-daypanel .low")

    data = []
    added_dates = set()  # Keep track of added dates

    # Find the index of the first occurrence of the 1st day of the month
    start_index = dates.index(next(date_elem for date_elem in dates if date_elem.text == '1'))

    for i in range(start_index, len(dates)):
        current_date = f"{dates[i].text} {calendar.month_abbr[month]} {year}"
        
        # Check if the date has already been added
        if current_date not in added_dates:
            data.append({
                'Date': current_date,
                'High Temperature': highs[i].text,
                'Low Temperature': lows[i].text
            })
            
            # Add the date to the set of added dates
            added_dates.add(current_date)

    return data

# WebDriver
service = Service()
driver = webdriver.Chrome(service=service)

# Get tahun ini
current_year = datetime.now().year

# loop setiap bulan
all_data = []

for current_month in range(1, 13):
    # Scrape data cuaca bulanan
    weather_data = scrape_monthly_weather(driver, current_month, current_year)
    all_data.extend(weather_data)

# buat DataFrame dari data yang diambil
df = pd.DataFrame(all_data)

# simpan DataFrame ke file Excel
excel_file = 'Data_Cuaca_Jakarta_2024.xlsx'
df.to_excel(excel_file, index=False)

# Close WebDriver
driver.quit()

print(f'Data berhasil disimpan ke dalam {excel_file}')
