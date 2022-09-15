# from lxml.html.soupparser import fromstring
# from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import bs4
# from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd
import sys
import time as t

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl

relatorio = []

pd = pd.DataFrame()


# ---------------------------------------------------------------- Open the browser
url = "https://shopee.com.br/"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless') #TODO: Activate this option on production
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome('chromedriver', options=chrome_options)
browser.get(url)
# ----------------------------------------------------------------
# ---------------------------------------------------------------- Wait till find the element
while True:
    try:
        roboto = browser.find_element(
            By.CLASS_NAME, 'section-recommend-products-wrapper')
        t.sleep(1)
        break
    except:
        t.sleep(1)
# ----------------------------------------------------------------

soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
''' soup parser the page source'''

# TODO: Remove this, only needed for testing purposes
# print(soup)

categories = 'div[class="home-category-list__group"] a'
soup_categories = soup.select(categories)
'''Find all the categories in the home page'''

print(len(soup_categories))


for x in soup_categories:
    # TODO: Remove this, only needed for testing purposes
    print(unidecode(x.get_text()))
# ----------------------------------------------------------------

for i, soup_cat in enumerate(soup_categories):
    category = unidecode(soup_cat.get_text())
    print(i, category)

    link = soup_cat.find_all('a', href=True)
    link = soup_cat['href']
    ''' Find the href of the element'''
    print(link)

    url = f"https://shopee.com.br{link}"
    browser.get(url)

# ---------------------------------------------------------------- Wait till find the element
    while True:
        try:
            wait = browser.find_element(
                By.CLASS_NAME, 'shopee-category-list__header')
            t.sleep(2)
            break
        except:
            t.sleep(1)
# ----------------------------------------------------------------

    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    ''' soup parser the page source'''

    items = 'div[class="col-xs-2-4 shopee-search-item-result__item"]'
    soup_items = soup.select(items)
    '''Find the items container'''

    # TODO: Remove this, only needed for testing purposes
    print(len(soup_items))

    product_name = 'div[class="TxwJWV _2qhlJo rrh06d"]'
    soup_product_name = soup.select(product_name)
    ''' Find the product name container'''

    # TODO: Existem mais de uma span de preco em alguns produtos, resolver esse problema para gerar o valor correto para cada produto
    price = 'span[class="R+c8Pr"]'
    soup_price = soup.select(price)
    ''' Find the price container'''

    print(soup_price)  # TODO: Remove this, only needed for testing purposes

    items_links = 'div[class="col-xs-2-4 shopee-search-item-result__item"] a'
    soup_items_links = soup.select(items_links)
    links = []
    for ind, item in enumerate(soup_items_links):
        link = item.find_all('a', href=True)
        link = item['href']
        links.append(link)

    for index, product in enumerate(soup_product_name):
        print(product.string, soup_price[index].string, links[index])
        info = {
            "product": product.string,
            "price": soup_price[index].string,
            "link": f'https://shopee.com.br{links[index]}',
        }
        relatorio.append(info)

    while i <= 50-1:
        # ---------------------------------------------------------------- Wait till find the element
        while True:
            try:
                next_page = browser.find_element(
                    By.CSS_SELECTOR, 'button[class*="shopee-icon-button shopee-icon-button--right"]')
                next_page.send_keys(Keys.ENTER)
                print(i, 'Mudei de Página!')
                break
            except:
                t.sleep(1)
# ----------------------------------------------------------------
# ---------------------------------------------------------------- Wait till find the element
        while True:
            try:
                wait = browser.find_element(
                    By.CSS_SELECTOR, 'button[class*="shopee-icon-button shopee-icon-button--right"]')
                t.sleep(2)
                break
            except:
                t.sleep(1)
# ----------------------------------------------------------------

        soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
        soup_items = soup.select(items)
        '''Find the items container'''

        # TODO: Remove this, only needed for testing purposes
        print(len(soup_items))

        product_name = 'div[class="TxwJWV _2qhlJo rrh06d"]'
        soup_product_name = soup.select(product_name)
        '''Find the product name'''

        # TODO: Existem mais de uma span de preco em alguns produtos, resolver esse problema para gerar o valor correto para cada produto
        price = 'span[class="R+c8Pr"]'
        soup_price = soup.select(price)
        '''Find the product price'''

        items_links = 'div[class="col-xs-2-4 shopee-search-item-result__item"] a'
        soup_items_links = soup.select(items_links)
        links = []
        for ind, item in enumerate(soup_items_links):
            link = item.find_all('a', href=True)
            link = item['href']
            links.append(link)
            '''Iterate over the links'''

        for index, product in enumerate(soup_product_name):
            print(product.string, soup_price[index].string, links[index])
            info = {
                "product": product.string,
                "price": soup_price[index].string,
                "link": f'https://shopee.com.br{links[index]}',
            }
            relatorio.append(info)
            '''Iterate over the product names'''

        i += 1  # Add 1 to enumerate valor

    category_excel = link.find('.')
    category_excel = link[:category_excel]
    df = pd.append(relatorio)
    df = df.to_excel(f"{unidecode(category_excel)}.xlsx")
    '''Make the Report of the category'''

df = pd.append(relatorio, ignore_index=True)
df = df.to_excel("RelatorioPrecosShopeeGeral.xlsx")
'''Make the General Report'''

browser.quit()
'''Closes the browser'''
