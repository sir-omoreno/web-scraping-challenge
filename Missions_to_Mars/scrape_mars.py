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
    # print(news_title)
    # print(news_p)
    browser.quit()

#### MARS FACTS SECTIONS ####
    browser = init_browser()
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    html = browser.html
    soup = bs(html, 'html')
    time.sleep(5)
    tables_to_pandas = pd.read_html(mars_facts_url)
    facts_table = tables_to_pandas[0]
    facts_table.columns = ["Description", "Value"]
    facts_table.set_index("Description", inplace=True)
    table_html = facts_table.to_html()

    browser.quit()

 ####  MARS HEMISPHERES SECTIONS #####
    browser = init_browser()

    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    test_html = browser.html
    soup = bs(test_html,'html')
    time.sleep(5)

    all_hemispheres = soup.find('div', class_='collapsible results')
    hemispheres = all_hemispheres.find_all('div', class_='item')
    beginning_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

    for result in hemispheres:
        hemisphere = result.find('div', class_="description")
        title = hemisphere.h3.text

        ending_url = hemisphere.a["href"]
        browser.visit(beginning_url + ending_url)

        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = image_url

        hemisphere_image_urls.append(hemisphere_dict)

        browser.quit()


    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        # "featured_image_url": featured_image_url,
        "fact_table": table_html,
        "hemisphere.img_url": hemisphere_image_urls
    }

    # Return results
    return mars_data
