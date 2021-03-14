import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)