# website-catalog-web-scrape
This code is to get Reclaim cPanel and Site Ownership Information.

## Author
Jared Chen 2023, Walt Li 2023  
For: Em Palencia


## Summary
When scraper.py is run, it will sign into Carleton Colleges WHM page and scrape domain information. While the scraper is running, it will print out some information about the domain it is currently parsing, this is just so you know the program hasn't crashed yet. When the scraper is finished running, it will place that information into a csv file for easy viewing.

## How to run the program
### 1. Make sure you have Python on your machine

### 2. Install the two LIBRARIES below by executing the two commands
 `pip3 install selenium`\
 `pip3 install requests`

### 3. Download this repo (Code > Download ZIP)

### 4. WEB DRIVER
You need to find the webdriver that matches your Chrome version. Check your chrome version and download the matching Chrome driver here.

Web drivers: https://chromedriver.storage.googleapis.com/index.html 

Replace the webdriver in this folder with the webdriver you just downloaded. 

### 5. Create CONFIG.PY
create a file called `config.py`. This will contain log in information for cPanel. You can copy-paste the format below into config.py, and replace your_username and your_password with the actual thing, please keep the `''`.
```
username = 'your_username'
password = 'your password'
```

### 6. Run the program
Navigate your command/terminal to the folder where you have the code. Use the following command the run the program. 
```
python3 scraper.py
```
