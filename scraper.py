import config
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from bs4 import BeautifulSoup



def launch_browser():
    s=Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    return driver



def get_sub_domains(driver):
    domain_counter = 0
    # goes to domains page under cpanel
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="domains-body"]/div/div[2]')))
    finally:
        driver.find_element(By.XPATH, '//*[@id="domains-body"]/div/div[2]').click()

    # gets table of domains
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'domainItemLister_items_table')))
    finally:
        domain_table = driver.find_element(By.ID, 'domainItemLister_items_table')

    subdomain_string = ''
    # filters through table pulling out domain urls
    for domain_row in domain_table.find_elements(By.CSS_SELECTOR, 'tr'):

        domain_cell_counter = 0
        for domain_cell in domain_row.find_elements(By.TAG_NAME, 'td'):
            # prevents main domain from being in this list
            if domain_cell_counter == 1 and 'Main Domain' not in domain_cell.text:
                subdomain_string = subdomain_string + '     ' + domain_cell.text
                domain_counter += 1
            domain_cell_counter += 1

    subdomain_string = subdomain_string.strip()

    if not subdomain_string:
        subdomain_string = 'None'
    subdomain_string = str(domain_counter) + '     ' + subdomain_string
    # return to cpanel page for next function
    driver.execute_script("window.history.go(-1)")
    return subdomain_string



def get_apps(driver):
    app_string = ''
    app_count = 0
    # goes to myApps page
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="item_myapps"]')))
    finally:
        driver.find_element(By.XPATH, '//*[@id="item_myapps"]').click()

    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'i_header_tab_installs_num')))
    finally:
        app_count = driver.find_element(By.ID, 'i_header_tab_installs_num').text
    # if apps exist
    if app_count != 0:
        app_table = driver.find_elements(By.CLASS_NAME, 'i_details')
        app_counter = 0
        # pulls app urls
        for app in app_table:
            url = driver.find_elements(By.CSS_SELECTOR, 'div.i_nortl > a')[app_counter].get_attribute('href')
            app_name = driver.find_elements(By.CLASS_NAME, 'i_icon > a')[app_counter].get_attribute('data-descr')
            app_string = app_string + '     ' + app_name + ':' + url
            app_counter += 1

    app_string = app_string.strip()
    if not app_string:
        app_string = 'None'
    app_string = str(app_count) + '     ' + app_string
    return app_string
    # print(app_string)



def get_backups(driver):
    backup_count = driver.find_element(By.ID, 'i_header_tab_backups_num').text
    # if backup_count != 0:
    #     driver.find_element(By.ID, 'i_header_tab_backups').click
    #     backup_table = driver.find_elements(By.)
    return backup_count


def main():
    driver = launch_browser()
    driver.get('https://carleton.reclaimhosting.com:2087/')
    driver.maximize_window()
    parent = driver.window_handles[0]

    # driver.findElement(By.id('user'));
    driver.find_element(By.ID,'user').send_keys(config.username)
    driver.find_element(By.ID,'pass').send_keys(config.password)
    driver.find_element(By.ID,'login_submit').click()
    #driver.findElement(By.linkText("List Accounts")).click();
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sectionManageAccounts"]/ul/li[2]/a')))
    finally:
        driver.find_element(By.XPATH, '//*[@id="sectionManageAccounts"]/ul/li[2]/a').click()
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="contentContainer"]/div[2]/div[4]/div[9]/a')))
    finally:
        driver.find_element(By.XPATH, '//*[@id="contentContainer"]/div[2]/div[4]/div[9]/a').click()
    main_table = []
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'listaccts')))
    finally:
        main_table = driver.find_element(By.ID, 'listaccts')

    main_row_counter = 0
    for row in main_table.find_elements(By.CSS_SELECTOR, 'tr'):
        main_cell_counter = 0
        for cell in row.find_elements(By.TAG_NAME, 'td'):
            if main_cell_counter == 1:
                domain_url = ''
                domain_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[2]/a'
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, domain_xpath)))
                finally:
                    domain_url = driver.find_element(By.XPATH, domain_xpath).get_attribute('href')
                # print(domain_url)

            elif main_cell_counter == 4:
                username = ''
                username_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[5]'
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, username_xpath)))
                finally:
                    username = driver.find_element(By.XPATH, username_xpath).text
                # print(username)

            elif main_cell_counter == 5:
                email = ''
                email_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[6]/a'
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, email_xpath)))
                finally:
                    email = driver.find_element(By.XPATH, email_xpath).text
                # print(email)

            elif main_cell_counter == 8:
                quota = ''
                quota_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[9]/span[2]'
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, quota_xpath)))
                finally:
                    quota = driver.find_element(By.XPATH, quota_xpath).text
                # print(quota)

            elif main_cell_counter == 9:
                disk = ''
                disk_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[10]/span[2]'
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, disk_xpath)))
                finally:
                    disk = driver.find_element(By.XPATH, disk_xpath).text
                # print(disk)

            elif main_cell_counter == 2:
                cpanel_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[3]/form'
                try:
                    element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, cpanel_xpath)))
                finally:
                    driver.find_element(By.XPATH, cpanel_xpath).click()

                    child = driver.window_handles[1]
                    driver.switch_to.window(child)

                # actions in cell go here! 89

                # Gets list of sub domains of a given domain


                    # subdomain_string = get_sub_domains(driver)
                    # print('sub domains: ', subdomain_string)
                    #
                    # app_string = get_apps(driver)
                    # print('apps: ', app_string)
                    #
                    # backup_count = get_backups(driver)
                    # print('backup: ' , backup_count)

                    driver.close()
                    driver.switch_to.window(parent)


            main_cell_counter += 1
        main_row_counter += 1

    #driver.quit()

if __name__ == '__main__':
    main()
