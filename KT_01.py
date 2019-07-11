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


def isClickable(driver):
    try:
        WebDriverWait(driver, 3, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))
    except:
        pass

    style = driver.execute_script("return document.getElementsByClassName('btn-more')[0].style.display")
    if style == 'none':
        return False
    else:
        return True


def getList(driver):
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


# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
driver = webdriver.Chrome()  # 'chromedriver', chrome_options=options
url = 'https://product.kt.com/wDic/index.do?CateCode=6002'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

page = int(soup.find(id='choice1').ul.find_all('li')[-1]['id'])
cssSelector = '#cfmClContents > div.fare-list-area > div > div.inner > a'
time1 = time.time()
for i in range(2, page + 2):
    while 1:
        try:
            time2 = time.time()
            print(time2 - time1)
            # time.sleep(1)
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))
            time1 = time.time()
            driver.find_element_by_css_selector(cssSelector).send_keys(Keys.ENTER)

        except:
            print('에러')
            break


    getList(driver)

    if i < page + 1:
        element = driver.find_element_by_xpath('//*[@id="%d"]' % i)
        driver.execute_script('arguments[0].click()', element)

driver.close()
