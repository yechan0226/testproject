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


def getList(driver):
    file = open('KT.csv', 'a', newline='')
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
            # print(valueList)
            csvfile = csv.writer(file)
            csvfile.writerow(valueList)
    file.close()


options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# options.headless = True

driver = webdriver.Chrome(options=options)
url = 'https://product.kt.com/wDic/index.do?CateCode=6002'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
hrefs = driver.find_element_by_class_name('red-select, optionItemListClickEvent').find_elements_by_tag_name('a')

for href in hrefs:
    href.send_keys(Keys.ENTER)
    while True:
        try:
            element = EC.visibility_of_all_elements_located((By.CLASS_NAME, 'plan-list, detail-list'))
            WebDriverWait(driver, 5).until(element)
            button = driver.find_element_by_class_name('btn-more')
            if not button.is_displayed():
                break
            button.send_keys(Keys.ENTER)

        except TimeoutException as e:
            print(e.args)
            break
        except Exception:
            break

    getList(driver)

driver.close()
