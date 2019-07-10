from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def remove_ws(str):
    return ' '.join(str.replace('\n\n','').replace('\t','').strip('\n ').split())

def getList(tableClass):
    try:
        file = open('LG U+.csv', 'a', newline='')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if tableClass == 'chargeItemWrp':
            divsClass = 'charge_box'
            titleClass = 'charge_tit'
            priceClass = 'charge_price'
        elif tableClass == 'fivegServiceCont':
            divsClass = 'conTxt'
            titleClass = 'titLevel02 pdtTitle'
            priceClass = 'priceTag hidden-xs'
        table = soup.find('div', class_=tableClass)
        divs = table.find_all('div', class_=divsClass)
        for div in divs:
            valueList = ['','','','','']
            valueList[0] = remove_ws(div.div.find(class_=titleClass).text)
            lis = div.ul.find_all('li')
            valueList[1] = remove_ws(lis[0].text)
            valueList[2] = remove_ws(lis[1].text)
            valueList[3] = remove_ws(lis[2].text)
            valueList[4] = remove_ws(div.find(class_=priceClass).text)

            csvfile = csv.writer(file)
            csvfile.writerow(valueList)
        file.close()
    except:
        driver.close()
        raise

def page(tableClass):
    delay = 5
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    pageNum = soup.find('span', class_='number')
    if pageNum == None:
        lastPageNum = 1
    elif len(pageNum.find_all('a')) > 1:
        lastPageNum = int(pageNum.find_all('a')[-1].text)
    else:
        lastPageNum = 1
    for i in range(2, lastPageNum + 1):
        getList(tableClass)
        driver.find_element_by_css_selector('#svcForm > div > div.pagenavi > div > div > span.number > a:nth-child(%d)'%i).send_keys(Keys.ENTER)

        # element = driver.find_element_by_css_selector('#svcForm > div > div.pagenavi > div > div > span.number > a:nth-child(%d)'%i)
        # driver.execute_script('arguments[0].click()',element)

        # for j in range(1, 5):
        #     try:
        #         WebDriverWait(driver, delay).until(
        #             EC.element_to_be_clickable(
        #                 (By.CSS_SELECTOR,
        #                  '#svcForm > div > div.pagenavi > div > div > span.number > a:nth-child(%d)' % i)
        #             )
        #         ).click()
        #         break
        #     except:
        #         pass
    getList(tableClass)

driver = webdriver.Chrome()
url = 'http://www.uplus.co.kr/ent/spps/chrg/RetrieveChrgList.hpi'
driver.get(url)

page('chargeItemWrp')
driver.find_element_by_css_selector('#select_wrap1 > a').click()
driver.find_element_by_css_selector('#select_wrap1 > ul > li:nth-child(2) > a').click()
driver.find_element_by_css_selector('#searchListBtn').click()
page('chargeItemWrp')
driver.find_element_by_css_selector('#select_wrap1 > a').click()
driver.find_element_by_css_selector('#select_wrap1 > ul > li:nth-child(3) > a').click()
driver.find_element_by_css_selector('#searchListBtn').click()
page('chargeItemWrp')
driver.get('http://www.uplus.co.kr/ent/fiveg/5GPlanList.hpi?mid=13049')
page('fivegServiceCont')

driver.close()