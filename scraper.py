import config
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver.manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# loginurl = ('https://carleton.reclaimhosting.com:2087/login/?login_only=1')
# secureurl = ('https://carleton.reclaimhosting.com:2087/cpsess1745090637/?login=1&post_login=59666413072871')

payload = {
    'user': config.username,
    'pass': config.password,
}


def launchBrowser():
    s=Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    return driver

driver = launchBrowser()
driver.get('https://carleton.reclaimhosting.com:2087/')
driver.maximize_window()

# driver.findElement(By.id('user'));
driver.find_element(By.ID,'user').send_keys(config.username)
# driver.findElement(By.id("pass"))
driver.find_element(By.ID,'pass').send_keys(config.password)
# while(True):
driver.find_element(By.ID,'login_submit').click()
print('check1')
#driver.findElement(By.linkText("List Accounts")).click();
driver.implicitly_wait(3)
driver.find_element_by_xpath('//*[@id="sectionManageAccounts"]/ul/li[2]/a').click()
print('done')

#driver.close()


#driver.find_element_by_partial_link_text('List Accounts')

#     pass

# with requests.session() as s:
#     s.post(loginurl, data=payload)
#     r = s.get(secureurl)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     print(soup.prettify())
