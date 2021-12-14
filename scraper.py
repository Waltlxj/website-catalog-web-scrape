import config
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# payload = {
#     'user': config.username,
#     'pass': config.password,
# }


def launchBrowser():
    s=Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    return driver

driver = launchBrowser()
driver.get('https://carleton.reclaimhosting.com:2087/')
driver.maximize_window()
parent = driver.window_handles[0]

# driver.findElement(By.id('user'));
driver.find_element(By.ID,'user').send_keys(config.username)
driver.find_element(By.ID,'pass').send_keys(config.password)
driver.find_element(By.ID,'login_submit').click()
#driver.findElement(By.linkText("List Accounts")).click();
driver.implicitly_wait(2)
driver.find_element(By.XPATH, '//*[@id="sectionManageAccounts"]/ul/li[2]/a').click()
driver.find_element(By.XPATH, '//*[@id="contentContainer"]/div[2]/div[4]/div[9]/a').click()

main_table = driver.find_element(By.ID, 'listaccts')
main_row_counter = 0
for row in main_table.find_elements(By.CSS_SELECTOR, 'tr'):
    main_cell_counter = 0
    for cell in row.find_elements(By.TAG_NAME, 'td'):
        if main_cell_counter == 2:

            curr_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[3]/form'
            driver.find_element(By.XPATH, curr_xpath).click()

            child = driver.window_handles[1]
            driver.switch_to.window(child)
            # REMOVE FOR TESTING PURPOSES
            # driver.implicitly_wait(2)

            # actions in cell go here!

            # Gets list of sub domains of a given domain
            driver.find_element(By.XPATH, '//*[@id="icon-domains"]').click()
            domain_table = driver.find_element(By.ID, 'domainItemLister_items_table')
            for domain_row in domain_table.find_elements(By.CSS_SELECTOR, 'tr'):
                domain_counter = 0
                subdomain_string = ''
                for domain_cell in domain_row.find_elements(By.TAG_NAME, 'td'):
                    # print(domain_cell.text, domain_counter)
                    if domain_counter == 1 and 'Main Domain' not in domain_cell.text:
                        subdomain_string = subdomain_string + domain_cell.text + '   '
                    domain_counter += 1
                subdomain_string = subdomain_string.strip()
                if not subdomain_string:
                    subdomain_string = 'None'
                print(subdomain_string)






            driver.close()
            driver.switch_to.window(parent)


        main_cell_counter += 1
    main_row_counter += 1





#driver.quit()
