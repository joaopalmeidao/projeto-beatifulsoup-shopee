from lxml.html.soupparser import fromstring
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd
import sys
import time as t

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


pd = pd.DataFrame()

sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')

url = "https://shopee.com.br/"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome('chromedriver', options=chrome_options)
browser.get(url)


while True:
    try:
        roboto = browser.find_element(
            By.CLASS_NAME, 'section-recommend-products-wrapper')
        t.sleep(1)
        break
    except:
        t.sleep(1)


soup = BeautifulSoup(browser.page_source, "html.parser")
# print(soup)

categories = 'div[class="home-category-list__group"] a'
soup_categories = soup.select(categories)

print(len(soup_categories))
# print(unidecode(str(soup_categories)))

for i, j in enumerate(soup_categories):
    category = j.get_text()
    print(i, unidecode(category))
    link = j.find_all('a', href=True)
    link = j['href']
    print(link)
    url = f"https://shopee.com.br{link}"
    browser.get(url)
    while True:
        try:
            roboto = browser.find_element(
                By.CLASS_NAME, 'shopee-category-list__header')
            t.sleep(2)
            break
        except:
            t.sleep(1)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    # print(soup.encode('utf-8'))
    items = 'div[class="col-xs-2-4 shopee-search-item-result__item"]'
    soup_items = soup.select(items)
    print(len(soup_items))

# browser.quit()
