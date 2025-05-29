from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time

# Global Constants
URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(url=URL)
soup = BeautifulSoup(response.text, features="html.parser")

# Getting address and links
Property_details = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
Property_address = []
Property_links = []
for details in Property_details:
    Property_links.append(details.get("href"))
    Property_address.append(details.getText().strip().replace("|", " "))

# Getting prices
Property_info = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
Property_prices = []
for price in Property_info:
    Property_prices.append(price.getText().replace("/mo", "").replace("1 bd", "").replace("+", ""))

# Google Form automation
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


for n in range(len(Property_links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdQE34uSwJoPhUXVsILlQY2qSvlxCcpjL2gLSL2sjk7-Q7PaA/viewform?usp=header")
    time.sleep(5)

    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    links = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address.send_keys(Property_address[n])
    price.send_keys(Property_prices[n])
    links.send_keys(Property_links[n])

    # Fixed submit button using XPath with visible text
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(2)  # Allow form to process before next iteration
