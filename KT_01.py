from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def remove_ws(str):
    return ' '.join(str.replace('\n\n', '').replace('\t', '').strip('\n ').split())


def count(driver):
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    count = int(soup.find(class_='fare-list-area').find(class_='inner')
                .find(class_="btn-more").span.text.replace('더보기(', '').replace(')', ''))
    if count % 5 == 0:
        return (count // 5)
    else:
        return (count // 5 + 1)


def getList(driver):
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_="plan-list-area")
    tables = divs.find_all('table')
    for table in tables:
        if table['class'][0] == 'plan-list':
            title = 'td'
        elif table['class'][0] == 'detail-list':
            title = 'th'
        trs = table.tbody.find_all('tr')
        for tr in trs:
            valueList = ['', '', '', '', '', '']  # 7번째 목록닫기 및 비교하기 생략
            valueList[0] = remove_ws(tr.find(title, class_='title').text)
            lis = tr.ul.find_all('li')
            if lis[0] == lis[-1]:
                valueList[2] = remove_ws(lis[0].text)
            elif lis[1] == lis[-1]:
                valueList[1] = remove_ws(lis[0].text)
                valueList[3] = remove_ws(lis[1].text)
            else:
                valueList[1] = remove_ws(lis[0].text)
                valueList[2] = remove_ws(lis[1].text)
                valueList[3] = remove_ws(lis[2].text)
            valueList[4] = remove_ws(tr.find('td', class_='charge').text)
            valueList[5] = remove_ws(tr.find('td', class_='btns').a.text)
            print(valueList)


driver = webdriver.Chrome()
url = 'https://product.kt.com/wDic/index.do?CateCode=6002'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

page = int(soup.find(id='choice1').ul.find_all('li')[-1]['id']) - 1
cssSelector = '#cfmClContents > div.fare-list-area > div > div.inner > a'
for i in range(2, page + 2):
    number = count(driver)
    print(number)
    for j in range(0, number):
        try:
            driver.find_element_by_css_selector(cssSelector).send_keys(Keys.ENTER)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector))).click()
            # element = driver.find_element_by_css_selector(cssSelector)
            # driver.execute_script('arguments[0].click()', element)
        except:
            print('x')

    getList(driver)

    if i < page + 2:
        element = driver.find_element_by_xpath('//*[@id="%d"]' % i)
        driver.execute_script('arguments[0].click()', element)

driver.close()
