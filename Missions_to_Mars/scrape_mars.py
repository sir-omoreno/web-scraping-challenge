import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Mars news section from jupyter notebook for scraping
    base_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(base_url)
    time.sleep(5)
    base_url_html = browser.html
    soup = bs(base_url_html, 'html.parser')
    articles = soup.find('ul', class_='item_list')
    news_title = articles.find('div', class_='content_title').text
    news_text = soup.find('div', class_='article_teaser_body').text