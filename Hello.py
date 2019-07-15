from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
url = 'http://www.cjhellodirect.com/ratePopupView.do'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
herfs = soup.find(class_='pagingBox').find_all('a')
for herf in herfs