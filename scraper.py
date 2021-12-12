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

# driver_path = './chromedriver'
# driver = webdriver.Chrome(executable_path = driver_path)


def launchBrowser():
    s=Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get('https://www.youtube.com/watch?v=j7VZsCCnptM')
    return driver

driver = launchBrowser()

# while(True):
#     pass

# with requests.session() as s:
#     s.post(loginurl, data=payload)
#     r = s.get(secureurl)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     print(soup.prettify())
