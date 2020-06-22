import datetime
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_old_news_article_lines(driver, date_string):
    filtered_links = get_all_links(
        driver,
        'https://www.am730.com.hk/daily_news/all/' + date_string,
        'https://www.am730.com.hk/news/')
    return filtered_links

def get_all_links(driver, url, prefix):
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'option')
    filtered_links = []
    for link_elem in links:
        filtered_link = link_elem.get_attribute('value')
        if filtered_link.startswith(prefix):
            filtered_links.append(filtered_link)
    return filtered_links

driver = webdriver.Chrome()
driver.implicitly_wait(5)
try:
    driver.maximize_window()
except:
    print("Cannot maximize the window.")

output_link_file_prefix = './downloaded/links/am730_daily_'
today_date = datetime.datetime.today()
date = datetime.datetime(2020, 5, 8)

while date < today_date:
    date_string = str(date.year).zfill(4) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2)
    output_file_path = output_link_file_prefix + date_string + '.txt'
    if not(os.path.isfile(output_file_path)):
        # File not exists
        filtered_links = get_old_news_article_lines(driver, date_string)
        with open(output_file_path, 'w') as f:
            for item in filtered_links:
               	f.write("%s\n" % item)
    
    date += datetime.timedelta(days=1)

driver.close()
