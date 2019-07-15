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


def getList(soupTable, sector):
    if sector == 'thead':
        fieldTag = 'th'
        soupObj = soupTable.thead

    else:
        fieldTag = 'td'
        soupObj = soupTable.tbody

    # file = open('tplus.csv', 'a', newline='')
    rowspancounts = []
    valueList = []

    line = soupObj.tr.find_all(fieldTag)
    headcolspanCount = 0
    for field in line:
        if field.get('colspan') != None:
            headcolspanCount += (int(field.get('colspan')) - 1)
    fieldCount = len(line) + headcolspanCount

    for i in range(0, fieldCount):
        rowspancounts.append(0)
        valueList.append('')

    trs = soupObj.find_all('tr')
    for tr in trs:
        fields = tr.find_all(fieldTag)
        for field in fields:
            if field.get('style') == "display: none;":
                field.clear()
            div = field.find('div', class_='rngbtn_wrap')
            if div != None:
                div.clear()

        virtualCount = 0
        colspanCount = 0

        for fieldIndex in range(0, fieldCount):
            realNum = fieldIndex - virtualCount
            if rowspancounts[fieldIndex] == 0:
                rowspanValue = fields[realNum].get('rowspan')
                if rowspanValue != None:  # rowspan있을떄 저장
                    rowspancounts[fieldIndex] = int(rowspanValue) - 1

                if colspanCount == 0:
                    colspanValue = fields[realNum].get('colspan')
                    if colspanValue != None:
                        colspanCount = int(colspanValue) - 1
                        virtualCount += 1
                else:
                    colspanCount -= 1
                    if colspanCount > 0:
                        virtualCount += 1
                valueList[fieldIndex] = remove_ws(fields[realNum].text)

            else:
                rowspancounts[fieldIndex] -= 1
                virtualCount += 1
        print(valueList)
        # csvfile = csv.writer(file)
        # csvfile.writerow(valueList)
    # file.close()


driver = webdriver.Chrome()
url = 'https://www.tplusdirectmall.com/view/phoneChrgeSystem/getUsimChrgeSystemList.do'
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
hrefs = driver.find_elements_by_class_name('btn, gray, small')
print(len(hrefs))
for href in hrefs:
    try:
        element = EC.element_to_be_clickable((By.CLASS_NAME, 'btn, gray, small'))
        WebDriverWait(driver, 5).until(element)
        time.sleep(2)
        href.send_keys(Keys.ENTER)
    except TimeoutException as e:
        print(e.args)
    try:
        element = EC.element_to_be_clickable((By.CLASS_NAME, 'btn, pink'))
        WebDriverWait(driver, 5).until(element)
    except TimeoutException as e:
        print(e.args)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(class_='tblPlanDetail mb10').find('table')
    getList(table, 'thead')
    getList(table, 'tbody')

    driver.find_element_by_class_name('btn, pink').send_keys(Keys.ENTER)

driver.close()
