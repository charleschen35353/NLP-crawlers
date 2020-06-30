import sys
import time
import datetime
import os
import json
import glob
import hashlib
import argparse
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

def extract_scheme_1(driver, link, sleep=0):
    driver.get(link)
    time.sleep(sleep)
    title_elems = driver.find_elements(By.CSS_SELECTOR, '.story-body__h1')
    pub_date_elems = driver.find_elements(By.TAG_NAME, 'body')[0].text.split("\n")
    content_elems = driver.find_elements(By.CSS_SELECTOR, ".story-body__inner p")
    tags_elems = driver.find_elements(By.CSS_SELECTOR, '.tags-list a')
    title, pub_date, content, tags = None, None, None, None
    if (title_elems is not None) and (len(title_elems) > 0):
        for t in title_elems:
            if t.text and len(t.text.strip())>0:
                title = t.text
                break
    if (pub_date_elems is not None) and (len(pub_date_elems) > 0):
        for date in pub_date_elems:
            if "年" in date and "月" in date and "日" in date:
                date = date.split("日")[0]
                date = date.replace(" ","").replace("年", "-").replace("月", "-")
                date = date.split("-")
                year = date[0]
                month = date[1]
                if len(month) < 2 : month = "0"+ month
                day = date[2]
                if len(day) < 2 : day = "0"+ day
                pub_date = year + "-" + month + "-" + day
                break

    if (content_elems is not None) and (len(content_elems) > 0):
        content = ""
        for c in content_elems:
            if content != "":
                content += "\n"
            content += c.text   
          
    if (tags_elems is not None) and (len(tags_elems) > 0):
        tags = []
        for elem in tags_elems:
            if elem.text not in tags:            
                tags.append(elem.text)

    print(pub_date)
    return {
        'title': title,
	    'url': link,
	    'content': content,
	    'category': '新聞',
	    'lang': 'TradChinese',
        "author" : "",
        'source': 'BBC Chinese',
        'pub_date': pub_date,
        'tags': tags,
    }

def load_links(file_path):
    links = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            links.append(line.strip())
    links = list(set(links))
    return links


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download articles from the files of links')
    parser.add_argument(
        'file_selector',
        #default='./downloaded/daily_links/',
        help='Files which contain a list of links to articles'
    )

    parser.add_argument(
        'output_folder',
        #default='./downloaded/daily_docs/',
        help='Output folder'
    )

    parser.add_argument(
        '--resume_from',
        default=None, #'./downloaded/daily_links/am730_daily_2018-05-12.txt'
        help='Output folder'
    )

    args = parser.parse_args(sys.argv[1:])
    target_folder = args.output_folder 
    link_file_regex = args.file_selector + '/*'
    BBC_link_files = glob.glob(link_file_regex)
    total_file_path = len(BBC_link_files)

    resume_from_file_path = args.resume_from
    
    while True:
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        
        print("Resume from {}".format(resume_from_file_path))
        begin_resume = False
        try:
            for n, file_path in enumerate(sorted(BBC_link_files)):
                if begin_resume or (resume_from_file_path is None) or (file_path == resume_from_file_path):
                    begin_resume = True

                if not begin_resume:
                    continue
                print("{} {}/{}".format(file_path, n, total_file_path))
                resume_from_file_path = file_path
                links = load_links(file_path)
                print("{} links".format(len(links)))
                first_link = True
                for cur_link in sorted(links):
                    link_name = hashlib.md5(cur_link.encode('utf-8')).hexdigest()
                    if os.path.isfile(os.path.join(target_folder, link_name + '.json')):
                        # File exists
                        continue
                    if first_link:
                        first_link = False
                        structured_data = extract_scheme_1(driver, cur_link, sleep=10) #Cloudfare slow start
                    else:
                        structured_data = extract_scheme_1(driver, cur_link, sleep=random.randint(5,8))
                    
                    if not structured_data["content"]: continue

                    with open(os.path.join(target_folder, link_name + '.json'), 'w') as fp:
                        json.dump(structured_data, fp)
        except TimeoutException:
            driver.close()
            print("Encounter selenium.common.exceptions.TimeoutException. Wait for 10 minutes and retry again.")
            time.sleep(10*60)
        except WebDriverException:
            driver.close()
            print("Encounter selenium.common.exceptions.WebDriverException. Restarting dirvier in 5 seconds.")
            time.sleep(5)

   
    
