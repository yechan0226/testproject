from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("chromedriver.exe")

# url = 'https://www.ktmmobile.com/loginForm.do'
url = 'https://nid.naver.com/'

driver.get(url)

ID = 'yechan010226'
PW = 'chan010226'
# a = input('보안문자:')

# driver.find_element_by_name('userId').send_keys(ID)
# driver.find_element_by_name('passWord').send_keys(PW)
# driver.find_element_by_name('answer').send_keys(a)

driver.execute_script("document.getElementsByName('id')[0].value=\'"+ ID +"\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ PW +"\'")

driver.find_element_by_id('goLoginBtn').click()

driver.get('https://www.ktmmobile.com/mypage/chargeView03.do')

monthly = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]').text
message = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/div[2]/table/tbody/tr[2]/td[2]').text
call = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/div[2]/table/tbody/tr[3]/td[2]').text
axtra = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/div[2]/table/tbody/tr[4]/td[2]').text
discount = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/div[2]/table/tbody/tr[5]/td[2]').text

print('월정액은 %s입니다. \n단문문자는 %s입니다. \n모바일 국내통화료는 %s입니다. \n부가세는 %s입니다. \n요금할인액은 %s입니다.'
      %(monthly,message,call,axtra,discount))