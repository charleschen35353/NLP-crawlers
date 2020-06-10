import datetime
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Database Update Parameters
WITHIN_PAST_N_DAYS = None #Note that only affect the load more button. None: unrestricted
####

def get_all_links(driver, prefix, link_db):
    #Will not update link_db
    links = driver.find_elements(By.TAG_NAME, 'a')
    filtered_new_links = []
    for link_elem in links:
        filtered_link = link_elem.get_attribute('href')
        if filtered_link.startswith(prefix):
            if filtered_link in link_db:
                continue
            filtered_new_links.append(filtered_link)
            #link_db.add(filtered_link)
    return list(set(filtered_new_links))

def find_load_more_button(driver, button_css_selector):
    try:
        driver.find_element_by_css_selector(button_css_selector).click()
        return True
    except:
        print('Load more button cannot be found or clicked any more.')
        return False

def load_url_db(db_file_path):
    if not(os.path.isfile(db_file_path)):
        return set()
    links = []
    with open(db_file_path, "r") as f:
        for line in f.readlines():
            links.append(line.strip())
    return set(links)

def cleanse_url_db(db_file_path):
    links = []
    if os.path.isfile(db_file_path):
        with open(db_file_path, "r") as f:
            for line in f.readlines():
                links.append(line.strip())
    links = list(set(links))
    with open(db_file_path, 'w') as f:
        for item in links:
            f.write("%s\n" % item)
    print("Done")

def get_earliest_date(driver, date_css_selector):
    # Find the articles with the earliest publication date on the web page (does not press the "load more" button)
    date_elems = driver.find_element_by_css_selector(date_css_selector) #driver.find_elements(By.XPATH, '//article/header/h1')
    earliest_date = None
    for elem in date_elems:
        try:
            #elem_date = dateutil.parser.parse(elem.text) #More intelligent
            elem_date = datetime.datetime.strptime(elem.text, "%Y-%m-%d %H:%M:%S") #More stable
            if (earliest_date is None) or (elem_date < earliest_date):
                earliest_date = elem_date
        except ValueError as e:
            print("Cannot parse the date from {}".format(elem.text))
    return earliest_date

def observe_too_old_articles(driver, page_date_css_selector, today_date, within_past_days=None):
    if within_past_days is not None:
        earliest_date = get_earliest_date(driver, date_css_selector=page_date_css_selector)
        if earliest_date <= (today_date-datetime.timedelta(days=within_past_days)):
            return True
    return False

driver = webdriver.Chrome()
driver.implicitly_wait(2)
# try:
#     driver.maximize_window()
# except:
#     print("Cannot maximize the window.")

output_link_file_prefix = 'downloaded/links/stheadline_'
sections = {
    # 'politics_news': {
    #     'url': 'https://std.stheadline.com/politics/%E6%94%BF%E6%B2%BB-%E6%96%B0%E8%81%9E',
    #     'target_url_prefix': 'https://std.stheadline.com/politics/article/'
    # },
    # 'politics_commentary': {
    #     'url': 'https://std.stheadline.com/politics/%E6%94%BF%E6%B2%BB-%E6%99%82%E5%B1%80%E8%A7%A3%E7%A2%BC',
    #     'target_url_prefix': 'https://std.stheadline.com/politics/article/'
    # },
    # 'exclusive': {
    #     'url': 'https://std.stheadline.com/exclusive/%E7%8D%A8%E5%AE%B6',
    #     'target_url_prefix': 'https://std.stheadline.com/exclusive/article/'
    # },
    # 'property_news': {
    #     'url': 'https://std.stheadline.com/property/%E5%9C%B0%E7%94%A2-%E6%96%B0%E8%81%9E',
    #     'target_url_prefix': 'https://std.stheadline.com/property/article/'
    # },
    'property_demo': {
        'url': 'https://std.stheadline.com/property/%E5%9C%B0%E7%94%A2-%E6%A8%93%E7%9B%A4%E9%80%8F%E8%A6%96',
        'target_url_prefix': 'https://std.stheadline.com/property/article/'
    },
    'education_news': {
        'url': 'https://std.stheadline.com/education/%E6%95%99%E8%82%B2-%E6%96%B0%E8%81%9E',
        'target_url_prefix': 'https://std.stheadline.com/education/article/'
    },
    'education_kindergarten': {
        'url': 'https://std.stheadline.com/education/%E6%95%99%E8%82%B2-%E5%B9%BC%E7%A8%9A%E5%9C%92',
        'target_url_prefix': 'https://std.stheadline.com/education/article/'
    },
    'education_primary': {
        'url': 'https://std.stheadline.com/education/%E6%95%99%E8%82%B2-%E5%B0%8F%E5%AD%B8',
        'target_url_prefix': 'https://std.stheadline.com/education/article/'
    },
    'education_secondary': {
        'url': 'https://std.stheadline.com/education/%E6%95%99%E8%82%B2-%E4%B8%AD%E5%AD%B8',
        'target_url_prefix': 'https://std.stheadline.com/education/article/'
    },
    'education_tertiary': {
        'url': 'https://std.stheadline.com/education/%E6%95%99%E8%82%B2-%E5%A4%A7%E5%B0%88',
        'target_url_prefix': 'https://std.stheadline.com/education/article/'
    },
    'education_oversea': {
        'url': 'https://std.stheadline.com/education/%E6%95%99%E8%82%B2-%E6%B5%B7%E5%A4%96%E5%8D%87%E5%AD%B8',
        'target_url_prefix': 'https://std.stheadline.com/education/article/'
    },
    'kol_gaa3sai3tong4': {
        'url': 'https://std.stheadline.com/kol/%E6%9E%B6%E5%8B%A2%E5%A0%82',
        'target_url_prefix': 'https://std.stheadline.com/kol/article/'
    },
    'kol_zing3soeng1KOL': {
        'url': 'https://std.stheadline.com/kol/%E6%94%BF%E5%95%86KOL',
        'target_url_prefix': 'https://std.stheadline.com/kol/article/'
    },
    'kol_gong2gu2daai6si4doi6': {
        'url': 'https://std.stheadline.com/kol/%E6%B8%AF%E8%82%A1%E5%A4%A7%E6%99%82%E4%BB%A3',
        'target_url_prefix': 'https://std.stheadline.com/kol/article/'
    },
    'kol_san1gu2kong4jit6': {
        'url': 'https://std.stheadline.com/kol/%E6%96%B0%E8%82%A1%E7%8B%82%E7%86%B1',
        'target_url_prefix': 'https://std.stheadline.com/kol/article/'
    },
    'kol_cong3fo1saang1wut6': {
        'url': 'https://std.stheadline.com/kol/%E5%89%B5%E7%A7%91%E7%94%9F%E6%B4%BB',
        'target_url_prefix': 'https://std.stheadline.com/kol/article/'
    },
    'kol_40plus': {
        'url': 'https://std.stheadline.com/kol/40Plus',
        'target_url_prefix': 'https://std.stheadline.com/kol/article/'
    },
    'racing_post_race_news': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E8%B3%BD%E5%BE%8C%E6%96%B0%E8%81%9E',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'racing_news': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'racing_jockey_club_news': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E9%A6%AC%E6%9C%83%E6%B6%88%E6%81%AF',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'racing_hou4mou4lei5geoi3': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E8%B1%AA%E6%A8%A1%E7%90%86%E6%93%9A',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'racing_morning_practice': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E6%99%A8%E5%85%89%E8%BF%BD%E6%93%8A',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'racing_noi6hyun1bou6jing2': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E5%85%A7%E5%9C%88%E6%8D%95%E5%BD%B1',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'racing_maa5coeng4fau4sai3kui2': {
        'url': 'https://std.stheadline.com/racing/%E9%A6%AC%E7%B6%93-%E9%A6%AC%E5%A0%B4%E6%B5%AE%E4%B8%96%E7%B9%AA',
        'target_url_prefix': 'https://std.stheadline.com/racing/article/'
    },
    'supplement_gam1jat6gun2': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-%E4%BB%8A%E6%97%A5%E9%A4%A8',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_artcan': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-ArtCan',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_luxestyle': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-LUXESTYLE',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_cuisine': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-%E9%A3%B2%E9%A3%9F%E8%A1%97',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_travel': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-%E5%84%AA%E9%81%8A%E6%B4%BE',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_electronics': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-%E9%9B%BB%E6%B0%A3%E5%BB%8A',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_cars': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-%E9%A7%95%E9%A7%9B%E8%89%99',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'supplement_health': {
        'url': 'https://std.stheadline.com/supplement/%E5%89%AF%E5%88%8A-%E5%81%A5%E5%BA%B7%E6%B8%AF',
        'target_url_prefix': 'https://std.stheadline.com/supplement/article/'
    },
    'overseas_europe': {
        'url': 'https://std.stheadline.com/overseas/%E6%B5%B7%E5%A4%96%E7%B6%9C%E5%90%88-%E6%AD%90%E6%B4%B2',
        'target_url_prefix': 'https://std.stheadline.com/overseas/article/'
    },
    'overseas_los_angeles': {
        'url': 'https://std.stheadline.com/overseas/%E6%B5%B7%E5%A4%96%E7%B6%9C%E5%90%88-%E6%B4%9B%E6%9D%89%E7%A3%AF',
        'target_url_prefix': 'https://std.stheadline.com/overseas/article/'
    },
    'overseas_new_york': {
        'url': 'https://std.stheadline.com/overseas/%E6%B5%B7%E5%A4%96%E7%B6%9C%E5%90%88-%E7%B4%90%E7%B4%84',
        'target_url_prefix': 'https://std.stheadline.com/overseas/article/'
    },
    'overseas_san_francisco': {
        'url': 'https://std.stheadline.com/overseas/%E6%B5%B7%E5%A4%96%E7%B6%9C%E5%90%88-%E4%B8%89%E8%97%A9%E5%B8%82',
        'target_url_prefix': 'https://std.stheadline.com/overseas/article/'
    },
    'overseas_toronto': {
        'url': 'https://std.stheadline.com/overseas/%E6%B5%B7%E5%A4%96%E7%B6%9C%E5%90%88-%E5%A4%9A%E5%80%AB%E5%A4%9A',
        'target_url_prefix': 'https://std.stheadline.com/overseas/article/'
    },
    'overseas_vancouver': {
        'url': 'https://std.stheadline.com/overseas/%E6%B5%B7%E5%A4%96%E7%B6%9C%E5%90%88-%E6%BA%AB%E5%93%A5%E8%8F%AF',
        'target_url_prefix': 'https://std.stheadline.com/overseas/article/'
    }
    
}

today_date = datetime.datetime.today()
for section in sections:
    print("Section: {}".format(section))
    section_url = sections[section]['url']
    target_url_prefix = sections[section]['target_url_prefix']

    url_db_file_path = "{}{}.txt".format(output_link_file_prefix, section)
    cleanse_url_db(url_db_file_path)
    db_link_set = load_url_db(url_db_file_path)

    driver.get(section_url)
    # Disable auto refresh by disabling the timer
    driver.execute_script('var highestTimeoutId = setTimeout(";");for (var i = 0 ; i < highestTimeoutId ; i++) { clearTimeout(i); }')

    # Load all news
    while find_load_more_button(driver, '.btn-load-more'):
        if observe_too_old_articles(driver, page_date_css_selector='date', today_date=today_date, within_past_days=WITHIN_PAST_N_DAYS):
            print("Observe old articles")
            break
        time.sleep(2) # Wait how long before the next press
        continue
    filtered_links = get_all_links(driver, target_url_prefix, db_link_set)

    if not(os.path.isfile(url_db_file_path)):
        open_mode = 'w'
    else:
        open_mode = 'a+'
    with open(url_db_file_path, open_mode) as f:
        for item in filtered_links:
            f.write("%s\n" % item)
            
driver.close()