import config
import requests
import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# lauches the webdriver. if using different diver change in line 15.
def launch_browser():
    s=Service('./chromedriver')
    driver = webdriver.Chrome(service=s)
    return driver


# Gets the subdomains of a particular c panel
def get_sub_domains(driver):
    domain_counter = 0
    # goes to domains page under cpanel
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'item_domains')))
    finally:
        driver.find_element(By.ID, 'item_domains').click()

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


#gets the applications of a domain
def get_apps(driver):
    app_string = ''
    app_count = 0
    # goes to myApps page
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'item_myapps')))
    finally:
        driver.find_element(By.ID, 'item_myapps').click()

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
    #does not return to cpanel menu since get_back_up function, which is called next uses same page
    return app_string
    # print(app_string)


# gets the number of backups
def get_backups(driver):
    backup_count = driver.find_element(By.ID, 'i_header_tab_backups_num').text
    return backup_count

#gets href of a cell in the list of accounts page
def get_value_href(driver, path):
    value = ''
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
    finally:
        value = driver.find_element(By.XPATH, path).get_attribute('href')
    return value
    # print(value)

#gets value of a cell in the list of accounts page
def get_value(driver, path):
    value = ''
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))
    finally:
        value = driver.find_element(By.XPATH, path).text
    return value
    # print(value)



#main function
def main():
    # launches browser and sets this tab as parent
    driver = launch_browser()
    driver.get('https://carleton.reclaimhosting.com:2087/')
    driver.maximize_window()
    parent = driver.window_handles[0]

    # global variables used to write to cs file
    domain_data = []
    filename = 'domain_data.csv'

    # logs in
    driver.find_element(By.ID,'user').send_keys(config.username)
    driver.find_element(By.ID,'pass').send_keys(config.password)
    driver.find_element(By.ID,'login_submit').click()
    # nagivate to accounts page and display all accounts
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
    # main_table represents the table of accounts
    main_table = []
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'listaccts')))
    finally:
        main_table = driver.find_element(By.ID, 'listaccts')

    main_row_counter = 0
    for row in main_table.find_elements(By.CSS_SELECTOR, 'tr'):
        domain_url = ''
        username = ''
        email = ''
        quota = ''
        disk = ''
        domain_count = ''
        subdomain_string = ''
        app_count = ''
        app_string = ''
        backup_count = ''

        main_cell_counter = 0

        for cell in row.find_elements(By.TAG_NAME, 'td'):
            if main_cell_counter == 1:
                domain_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[2]/a'
                domain_url = get_value_href(driver, domain_xpath)

            elif main_cell_counter == 4:
                username_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[5]'
                username = get_value(driver, username_xpath)

            elif main_cell_counter == 5:
                email_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[6]/a'
                email = get_value(driver, email_xpath)

            elif main_cell_counter == 8:
                quota_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[9]/span[2]'
                quota = get_value(driver, quota_xpath)

            elif main_cell_counter == 9:
                disk_xpath = '//*[@id="listaccts"]/tbody/tr[' + str(main_row_counter) + ']/td[10]/span[2]'
                disk = get_value(driver, disk_xpath)

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
                    subdomain_string = get_sub_domains(driver)
                    domain_count = subdomain_string[0: subdomain_string.find('     ')]
                    subdomain_string = subdomain_string[subdomain_string.find('     '):].strip(' ')

                    #get list of applications
                    app_string = get_apps(driver)
                    app_count = app_string[0: app_string.find('     ')]
                    app_string = app_string[app_string.find('     '):].strip(' ')

                    #gets number of backups
                    backup_count = get_backups(driver)

                    #closes current window to prep to open next cpanel
                    driver.close()
                    driver.switch_to.window(parent)

            main_cell_counter += 1
        main_row_counter += 1
        curr_row_data = [domain_url, username, email, quota, disk, domain_count, subdomain_string, app_count, app_string, backup_count]
        print(curr_row_data)
        domain_data.append(curr_row_data)


    driver.quit()

    #first row of domain_data is blank so it is removed and lable row is added
    domain_data.pop(0)
    label_row = ['domain url', 'username', 'email', 'quota', 'disk space', 'sub domain count', 'sub domain(s)', 'app count', 'app(s)', 'backup count']
    domain_data.insert(0, label_row)

    #writes to csv file
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(domain_data)


if __name__ == '__main__':
    main()
