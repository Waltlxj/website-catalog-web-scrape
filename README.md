# website-catalog-web-scrape

LIBRARIES (pip3 install [library]):
selenium
requests



WEB DRIVER:
By default the web driver I installed was for an m1 mac running chrome 96.0.4664.45. If you are running on a different type of computer or different version of chrome, download the correct web driver and put it in the same directory as scaper.py. edit the launch_browser method so that it will access the correct web driver.

Your chrome version: chrome://version/

Web drivers: https://chromedriver.storage.googleapis.com/index.html



CONFIG.PY:
create a file called config.py. This will contain log in information for the web scraper. You can copy-paste the format below. Create your own config.py locally with your own username and password.

username = [root username]
password = [root password]



SUMMARY:
When scraper.py is run, it will sign into Carleton Colleges WHM page and scrape domain information. While the scraper is running, it will print out some information about the domain it is currently parseing, this is just so you know the program hasn't crashed yet. When the scraper is finished running, it will place that information into a csv file for easy viewing.
