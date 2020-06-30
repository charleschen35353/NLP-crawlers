import datetime
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def get_page_urls(driver, url, targets):
    driver.get(url)
    tags = driver.find_elements(By.CSS_SELECTOR, targets) 
    links = [elem.get_attribute('href') for elem in tags]
    return links



driver = webdriver.Chrome()
driver.implicitly_wait(5)
try:
    driver.maximize_window()
except:
    print("Cannot maximize the window.")



categories = []
'''
#pre-fetch categories using main page
main_page = "https://www.bbc.com/zhongwen/trad"
links = get_page_urls(driver, main_page, ".Headline-sc-1dvfmi3-3.knMLuh a")
for item in links:
    if item.startswith("https://www.bbc.com/zhongwen/trad/"):
        print(item)
        urls = get_page_urls(driver, item, '.tags-list a')
        for url in urls:
            if url not in categories: categories.append(url)
'''
print("Pre-fetching done.")

categories = ['https://www.bbc.com/zhongwen/trad/topics/5fe79b8d-56e5-4aff-8b05-21f9ad731912', 'https://www.bbc.com/zhongwen/trad/topics/78080d81-2849-497e-bc3a-bf364626456b', 'https://www.bbc.com/zhongwen/trad/topics/82857f8e-8134-462a-bb32-b7b14f4eab75', 'https://www.bbc.com/zhongwen/trad/topics/ca170ae3-99c1-48db-9b67-2866f85e7342', 'https://www.bbc.com/zhongwen/trad/topics/dec4ac75-3f1c-492b-a93f-2b5aafd52806', 'https://www.bbc.com/zhongwen/trad/topics/ee4d5541-afdc-4511-9ba6-a42823b19429', 'https://www.bbc.com/zhongwen/trad/topics/10164f51-11a5-42a0-8946-ffbead9a5413', 'https://www.bbc.com/zhongwen/trad/topics/382a3aa6-52f2-485d-9d10-e9e9888c48a0', 'https://www.bbc.com/zhongwen/trad/topics/667ecf35-a325-4eed-adf9-80aac7d58eaf', 'https://www.bbc.com/zhongwen/trad/topics/6892384e-1966-4c03-9ce3-f694a8f9f69e', 'https://www.bbc.com/zhongwen/trad/topics/db766560-6b05-4eb5-b690-4c6118e0faf1', 'https://www.bbc.com/zhongwen/trad/topics/0f469e6a-d4a6-46f2-b727-2bd039cb6b53', 'https://www.bbc.com/zhongwen/trad/topics/918e9487-dc88-44e2-8168-057149670ec3', 'https://www.bbc.com/zhongwen/trad/topics/14745d1f-885d-4b9f-b28a-24540e7beb15', 'https://www.bbc.com/zhongwen/trad/topics/8455721e-3da5-4a1c-a114-180dbc2bbd92', 'https://www.bbc.com/zhongwen/trad/topics/a4e315c5-007c-4b8a-9762-bebd79fb8b6b', 'https://www.bbc.com/zhongwen/trad/topics/bce059a1-1a05-4b8d-aac8-381699aaa2f0', 'https://www.bbc.com/zhongwen/trad/topics/c4794229-7f87-43ce-ac0a-6cfcd6d3cef2', 'https://www.bbc.com/zhongwen/trad/topics/eb277d57-53fc-4859-b210-778a1941dd7d', 'https://www.bbc.com/zhongwen/trad/topics/4ad591cb-c2a8-4e28-931f-c8edadee1f43', 'https://www.bbc.com/zhongwen/trad/topics/597ce03d-e3ea-4a39-bf7e-6546e4a5791e', 'https://www.bbc.com/zhongwen/trad/topics/a3b15769-775e-471d-a511-a7b78f346859', 'https://www.bbc.com/zhongwen/trad/topics/b3ca5a45-59cf-4c5a-880a-e69a9ec96209', 'https://www.bbc.com/zhongwen/trad/topics/d94f45db-bb47-4e7b-b1a2-5bc3e6afd0aa', 'https://www.bbc.com/zhongwen/trad/topics/3c705018-0847-4676-8453-8fdaf9603bf3', 'https://www.bbc.com/zhongwen/trad/topics/cfb8bd8c-0638-4383-9dec-8d1703c8b4b8', 'https://www.bbc.com/zhongwen/trad/topics/22d5dbb6-b5f5-4a5b-be0f-ded92f7e6a2e', 'https://www.bbc.com/zhongwen/trad/topics/814465c5-404b-4c88-889f-45907ba1f402', 'https://www.bbc.com/zhongwen/trad/topics/e45cb5f8-3c87-4ebd-ac1c-058e9be22862', 'https://www.bbc.com/zhongwen/trad/topics/faa8885f-9e69-4c29-a8a5-516d508075dc', 'https://www.bbc.com/zhongwen/trad/topics/1c3b60a9-14eb-484b-a750-9f5b1aeaac31', 'https://www.bbc.com/zhongwen/trad/topics/2e91364c-5c77-4660-b76e-d76202785e64', 'https://www.bbc.com/zhongwen/trad/topics/61e63af6-03e6-4329-aede-21ec4992a675', 'https://www.bbc.com/zhongwen/trad/topics/6a73afa3-ea6b-45c1-80bb-49060b99f864', 'https://www.bbc.com/zhongwen/trad/topics/86862bb2-3d45-44c5-9156-a0c8982cd0c7', 'https://www.bbc.com/zhongwen/trad/topics/992e096e-28e6-412d-b6a1-652f78be63c7', 'https://www.bbc.com/zhongwen/trad/topics/de648736-7268-454c-a7b1-dbff416f2865', 'https://www.bbc.com/zhongwen/trad/topics/f6ec89fd-3823-498e-a888-572e96f791b2', 'https://www.bbc.com/zhongwen/trad/topics/427b2db2-b4a5-4ba2-88cd-9791e1df3c7d', 'https://www.bbc.com/zhongwen/trad/topics/5307a8d9-f620-40f5-92d4-f99c919a6ffa', 'https://www.bbc.com/zhongwen/trad/topics/5a08f030-710f-4168-acee-67294a90fc75', 'https://www.bbc.com/zhongwen/trad/topics/755f36fe-2126-4225-92bf-ac459c3c8832', 'https://www.bbc.com/zhongwen/trad/topics/ba90754a-9033-4e9c-990b-d1139e5070a3', 'https://www.bbc.com/zhongwen/trad/topics/ce5c43ee-8982-4f88-9472-9aa79aeb09cc', 'https://www.bbc.com/zhongwen/trad/topics/75612fa6-147c-4a43-97fa-fcf70d9cced3', 'https://www.bbc.com/zhongwen/trad/topics/5cd4682a-7643-f445-8b1f-bcbaf450bc89', 'https://www.bbc.com/zhongwen/trad/topics/b541a17f-f101-43f2-b56c-34cd909cc1cc', 'https://www.bbc.com/zhongwen/trad/topics/ba6e1118-f874-054e-b159-b797c16e9250', 'https://www.bbc.com/zhongwen/trad/topics/31684f19-84d6-41f6-b033-7ae08098572a', 'https://www.bbc.com/zhongwen/trad/topics/839cfd32-9a3d-47eb-a591-bf0e136d1f4b', 'https://www.bbc.com/zhongwen/trad/topics/03eb3674-6190-4cd7-8104-1a00991d67a3', 'https://www.bbc.com/zhongwen/trad/topics/20c1dc62-185a-46ca-b549-2f8aa162abc0', 'https://www.bbc.com/zhongwen/trad/topics/99fb9bbd-9150-4e13-a3ac-3fa0610683f8', 'https://www.bbc.com/zhongwen/trad/topics/ac90f011-0779-4da9-8ac5-4de96fcc2b93', 'https://www.bbc.com/zhongwen/trad/topics/ae43b7ed-1477-4bcc-8a84-d6d75919cbbc', 'https://www.bbc.com/zhongwen/trad/topics/6942cb29-9d3f-4c9c-9806-0a0578c286d6', 'https://www.bbc.com/zhongwen/trad/topics/b6313976-a311-480f-a813-08caddad7a2f', 'https://www.bbc.com/zhongwen/trad/topics/cec5d136-f83d-4e00-a3be-d22a7b89401f', 'https://www.bbc.com/zhongwen/trad/topics/10f9cc6b-0a52-46d3-bce6-9cd78b34600f', 'https://www.bbc.com/zhongwen/trad/topics/83a45ff0-d5b2-4cdb-be7e-523c6001751b', 'https://www.bbc.com/zhongwen/trad/topics/911f368c-e756-4ac3-9667-ec8900ceb4ce', 'https://www.bbc.com/zhongwen/trad/topics/ea2c5d34-4279-4e06-b69a-e699321d7f9f', 'https://www.bbc.com/zhongwen/trad/topics/4bc7e064-44b5-4f17-870c-8bf927f0c9bd', 'https://www.bbc.com/zhongwen/trad/topics/561a3920-eca1-4c21-b214-658837311fd1', 'https://www.bbc.com/zhongwen/trad/topics/df8633e3-7ad2-48f1-a60f-3a1698c8ddab', 'https://www.bbc.com/zhongwen/trad/topics/39267b85-1784-4f4b-80ed-f8cb4a35f337', 'https://www.bbc.com/zhongwen/trad/topics/47172845-9973-40ac-8d1e-b18a302cabf0', 'https://www.bbc.com/zhongwen/trad/topics/860d0ba1-52ca-4fa0-9576-90443551c034', 'https://www.bbc.com/zhongwen/trad/topics/b330e2a5-9d88-4e62-a688-c6d5f4987708', 'https://www.bbc.com/zhongwen/trad/topics/4fdf1711-6845-4344-98cc-1a382ed91b65', 'https://www.bbc.com/zhongwen/trad/topics/58d96fa3-becf-4fb9-8d1d-3a772bf88f59', 'https://www.bbc.com/zhongwen/trad/topics/84915d8d-467d-4c5e-88f7-bbb1bb5cf0dc', 'https://www.bbc.com/zhongwen/trad/topics/7a48b6e0-9074-4303-ae82-011003058e16', 'https://www.bbc.com/zhongwen/trad/topics/35ecb5ca-1001-4a90-a61c-f13a27f4e8e2', 'https://www.bbc.com/zhongwen/trad/topics/5098b057-41c4-48dd-b8a8-56673822a206', 'https://www.bbc.com/zhongwen/trad/topics/8b04c2e8-5409-4e7d-9877-3ccaf04727af', 'https://www.bbc.com/zhongwen/trad/topics/cd2b638b-71a7-4330-b549-21d3687134ee', 'https://www.bbc.com/zhongwen/trad/topics/f8694a4e-7ffd-4fc1-ab94-6d1d5597528a', 'https://www.bbc.com/zhongwen/trad/topics/18ea2cd2-2860-433f-bd4d-ff5bbd241d7e', 'https://www.bbc.com/zhongwen/trad/topics/3d303e09-05ad-4f46-89fb-4ff9921219a7', 'https://www.bbc.com/zhongwen/trad/topics/4795be02-dfe8-4a8d-b318-0609533ae17a', 'https://www.bbc.com/zhongwen/trad/topics/a61843ab-8ea2-4c93-88cd-fbb29f1993bf', 'https://www.bbc.com/zhongwen/trad/topics/02cfdd49-c5f4-4906-9657-055a810bca41', 'https://www.bbc.com/zhongwen/trad/topics/511accd7-6ee6-4dfb-8e2b-b236be8cb14c', 'https://www.bbc.com/zhongwen/trad/topics/862db3cf-b724-4e5d-9ed5-19e5bfa0ccbf', 'https://www.bbc.com/zhongwen/trad/topics/b74f28ac-bbb9-4103-a18e-856aee7ad9a2', 'https://www.bbc.com/zhongwen/trad/topics/b79ae056-59b1-49c7-8630-50f7e223e906', 'https://www.bbc.com/zhongwen/trad/topics/bd7b89a7-78bd-4c60-a78c-9983a479f70f', 'https://www.bbc.com/zhongwen/trad/topics/12e69b92-a7ba-4463-84e0-be107b9805d0', 'https://www.bbc.com/zhongwen/trad/topics/03460c2c-34b5-4681-ba1f-6d5aa1d2659e', 'https://www.bbc.com/zhongwen/trad/topics/2d46b4e1-05a6-495f-afdd-f253a3b95bc7', 'https://www.bbc.com/zhongwen/trad/topics/e6628cd5-c2d2-421f-a04d-7de92a105ba1', 'https://www.bbc.com/zhongwen/trad/topics/5b7a6e71-b3b5-40a0-9d55-dfdf90f8d34e', 'https://www.bbc.com/zhongwen/trad/topics/2e3befc0-e70a-41c7-b6cb-2f8f0d69a7db', 'https://www.bbc.com/zhongwen/trad/topics/9a18805c-fb88-40ba-9763-bcc121d5d55c', 'https://www.bbc.com/zhongwen/trad/topics/b3f4238f-ae69-4c19-8f0e-8bef7d4f359c', 'https://www.bbc.com/zhongwen/trad/topics/fe536195-d9a5-40ff-89c4-f216213cfd9e', 'https://www.bbc.com/zhongwen/trad/topics/6105fd8d-33f4-4de4-9525-abf33697324a', 'https://www.bbc.com/zhongwen/trad/topics/62d838bb-2471-432c-b4db-f134f98157c2', 'https://www.bbc.com/zhongwen/trad/topics/72d243a7-687b-4e7d-a022-1e36a138b0be', 'https://www.bbc.com/zhongwen/trad/topics/817a611b-967c-47e2-8b24-835576b97be7', 'https://www.bbc.com/zhongwen/trad/topics/b46d0167-5dc3-417e-8c4b-a73e2c81f3a0', 'https://www.bbc.com/zhongwen/trad/topics/2f2db234-3c2d-40a4-b4ac-eea661faadd0', 'https://www.bbc.com/zhongwen/trad/topics/d422d03a-ac5e-4d3f-b18b-c28b227375fc']

#iterate through category pages

output_link_file_prefix = './downloaded/BBC_Chinese_links/'
seen = []
while categories != []:
    #add new category if not seen
    cat = categories.pop() # sth like https://www.bbc.com/zhongwen/trad/topics/5a08f030-710f-4168-acee-67294a90fc75
    i = 1
    while True:

        url = cat + "/page/{}".format(i)

        output_file_path = output_link_file_prefix +cat.split('/')[-1] + "_page_{}".format(i) + '.txt'
        print("writing to" + output_file_path)
        if not(os.path.isfile(output_file_path)):
            filtered_links = get_page_urls(driver, url, '.qa-heading-link.lx-stream-post__header-link')
            if filtered_links == []: break
            else:
                for item in filtered_links:
                    if item not in seen:
                        with open(output_file_path, 'a') as f:
                            f.write("%s\n" % item)
                        seen.append(item)
                        links = get_page_urls(driver, item, '.tags-list a')
                        for link in links:
                            if link not in categories: categories.append(link)
                
        i+=1

driver.close()
