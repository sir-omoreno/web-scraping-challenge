import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    base_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(base_url)
    time.sleep(5)

    base_url_html = browser.html
    soup = bs(base_url_html, 'html.parser')

    # Finds the article title and the description
    articles = soup.find('ul', class_='item_list')
    news_title = articles.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print(news_p)

    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p
        # "featured_image_url": featured_image_url,
        # "mars_facts_html": mars_facts_html,
        # "hemisphere_image_urls": hemisphere_image_urls
    }

    # Return results
    return mars_data
