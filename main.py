from lxml.html.soupparser import fromstring
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd
import sys
import time as t

pd = pd.DataFrame()

sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')

url = "https://shopee.com.br/"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome('chromedriver', options=chrome_options)
browser.get(url)
t.sleep(5)
soup = BeautifulSoup(browser.page_source, "html.parser")

categories = 'div[class="pFceVI"] a'
soup_categories = soup.select(categories)

print(len(soup_categories))
print(unidecode(str(soup_categories)))

for i, j in enumerate(soup_categories):
    category = j.get_text()
    print(i, unidecode(category))
    link = j.find_all('a', href=True)
    print(j['href'])

browser.quit()
