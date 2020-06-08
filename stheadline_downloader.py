import sys
import time
import os
import json
import glob
import hashlib
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Some links obtained from
#https://std.stheadline.com/daily/formerly/%E6%97%A5%E5%A0%B1-%E6%98%94%E6%97%A5-2017-06-06
stheadline_daily_home = ['https://std.stheadline.com/daily/formerly/%E6%97%A5%E5%A0%B1-%E6%98%94%E6%97%A5-2017-06-06']
stheadline_links = [
    'https://std.stheadline.com/daily/article/1611132/%E6%97%A5%E5%A0%B1-%E7%A4%BE%E8%AB%96-%E6%89%B9%E5%A1%AB%E6%B5%B7%E6%92%A5%E6%AC%BE-%E7%82%BA%E6%A8%93%E5%B8%82%E9%99%8D%E6%BA%AB',
    'https://std.stheadline.com/daily/article/1611165/%E6%97%A5%E5%A0%B1-%E6%B8%AF%E8%81%9E-%E6%A2%81%E5%90%9B%E5%BD%A5%E6%93%AC%E8%AE%93%E8%B7%AF%E8%B2%A1%E6%9C%83-%E6%B3%9B%E6%B0%91%E8%AD%B0%E5%93%A1%E8%81%AF%E7%BD%B2%E5%8F%8D%E5%B0%8D',
    'https://std.stheadline.com/daily/article/1611183/%E6%97%A5%E5%A0%B1-%E6%B8%AF%E8%81%9E-%E8%B3%87%E7%A7%91%E8%BE%A6%E9%96%8B%E7%99%BCAPI-%E4%BE%BF%E5%88%A9%E7%A8%8B%E5%BC%8F%E9%96%8B%E7%99%BC%E5%93%A1'
]

def extract_scheme_1(driver, link, sleep=0):
    driver.get(link)
    time.sleep(sleep)
    title_elems = driver.find_elements(By.XPATH, '//article/header/h1')
    pub_date_elems = driver.find_elements(By.XPATH, '//article/header/span')
    content_elems = driver.find_elements(By.XPATH, "//article/section/div[position() = 2]/p")
    #return header_elems[0].text, date_elems[0].text, section_elems[0].text, 'traditional_chinese'
    title, pub_date, content = None, None, None
    if (title_elems is not None) and (len(title_elems) > 0):
        title = title_elems[0].text
    if (pub_date_elems is not None) and (len(pub_date_elems) > 0):
        pub_date = pub_date_elems[0].text
    if (content_elems is not None) and (len(content_elems) > 0):
        content = content_elems[0].text
    return {
        'title': title,
        'author': None,
        'source': link,
        'category': None,
        'pub_date': pub_date,
        'language': 'traditional_chinese',
        'content': content,
        'tags': None,
        'extractor': 'extract_scheme_1.v1',
    }

def load_links(file_path):
    links = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            links.append(line.strip())
    links = list(set(links))
    return links

jobs = {
    'job1': {
        'name': 'singtao_news',
        'extractor': extract_scheme_1,
        'links': stheadline_links
    }
}

driver = webdriver.Chrome()
driver.implicitly_wait(3)
try:
    driver.maximize_window()
except:
    print("Cannot maximize the window.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download articles from the files of links')
    parser.add_argument(
        'file_selector',
        #default='downloaded/links/stheadline_2*',
        help='Files which contain a list of links to articles'
    )

    parser.add_argument(
        'output_folder',
        #default='/home/pacowong/research/website-crawler/downloaded/sites/stheadline/',
        help='Output folder'
    )

    parser.add_argument(
        '--resume_from',
        default=None, #'downloaded/links/stheadline_2017-11-22.txt'
        help='Output folder'
    )

    args = parser.parse_args(sys.argv[1:])
    prev_stheadline_link_files = []
    target_folder = args.output_folder #'/home/pacowong/research/website-crawler/downloaded/sites/stheadline/'
    link_file_regex = args.file_selector #"downloaded/links/stheadline_2*"
    stheadline_link_files = glob.glob(link_file_regex)
    total_file_path = len(stheadline_link_files)

    resume_from_file_path = args.resume_from #'downloaded/links/stheadline_2017-11-22.txt'
    begin_resume = False
    for n, file_path in enumerate(sorted(stheadline_link_files)):
        print("{} {}/{}".format(file_path, n, total_file_path))
        if begin_resume or (resume_from_file_path is None) or (file_path == resume_from_file_path):
            begin_resume = True

        if not begin_resume:
            continue

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
                structured_data = extract_scheme_1(driver, cur_link)

            with open(os.path.join(target_folder, link_name + '.json'), 'w') as fp:
                json.dump(structured_data, fp)

    # for job_name in jobs:
    #     job = jobs[job_name]
    #     for cur_link in job['links']:
    #         structured_data = job['extractor'](driver, cur_link)
    #         print(structured_data)


        #https://stackoverflow.com/questions/30403415/using-multiple-criteria-to-find-a-webelement-in-selenium
        #header_tags = driver.find_elements(By.TAG_NAME, 'header')

        #header_elems = driver.find_elements(By.XPATH, '//article/header/h1')
        #date_elems = driver.find_elements(By.XPATH, '//article/header/span')
        #section_elems = driver.find_elements(By.XPATH, "//article/section/div[position() = 2]/p")

    driver.close()