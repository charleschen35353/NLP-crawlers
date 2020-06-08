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
        'https://std.stheadline.com/daily/formerly/%E6%97%A5%E5%A0%B1-%E6%98%94%E6%97%A5-' + date_string,
        'https://std.stheadline.com/daily/article/')
    return filtered_links

def get_all_links(driver, url, prefix):
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, 'a')
    filtered_links = []
    for link_elem in links:
        filtered_link = link_elem.get_attribute('href')
        if filtered_link.startswith(prefix):
            filtered_links.append(filtered_link)
    return filtered_links

driver = webdriver.Chrome()
driver.implicitly_wait(5)
try:
    driver.maximize_window()
except:
    print("Cannot maximize the window.")

output_link_file_prefix = 'downloaded/links/stheadline_'
today_date = datetime.datetime.today() #.datetime(2020, 6, 5)
date = datetime.datetime(2017, 6, 6)

while True:
    date_string = str(date.year).zfill(4) + '-' + str(date.month).zfill(2) + '-' + str(date.day).zfill(2)
    print(date_string)
    output_file_path = output_link_file_prefix + date_string + '.txt'
    if not(os.path.isfile(output_file_path)):
        # File not exists
        filtered_links = get_old_news_article_lines(driver, date_string)
        with open(output_file_path, 'w') as f:
            for item in filtered_links:
                f.write("%s\n" % item)
    
    date += datetime.timedelta(days=1)
    if date >= today_date:
        break

driver.close()