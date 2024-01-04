import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Google form to update the results in list form, you can request the form or create your own or use logging
# to see results

LINK = os.environ.get('F_KEY')

# Fake zillow website to be scrapped, link in description
URL = os.environ.get('U')

response = requests.get(URL)
zillow_html = response.text

soup = BeautifulSoup(zillow_html, 'html.parser')
rentals_addresses = soup.select('a address')
rentals_prices = soup.select('span.PropertyCardWrapper__StyledPriceLine')
rentals_links = soup.select('li a.StyledPropertyCardDataArea-anchor')
listings_addresses = []
listings_prices = []
listings_links = []

for address in rentals_addresses:
    listings_addresses.append(address.getText().replace(" | ", " ").strip())
for price in rentals_prices:
    listings_prices.append(price.getText().replace("/mo", "").split("+")[0])
for link in rentals_links:
    listings_links.append(link.get('href'))

# There are 44 records, if the code is to run to the length of the records found.

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

time.sleep(5)

for index in range(10):
    driver.get(LINK)
    time.sleep(2)

    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                        '1]/div/div[1]/input')
    address.send_keys(listings_addresses[index])

    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                      '1]/div/div[1]/input')
    price.send_keys(listings_prices[index])

    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                     '1]/div/div[1]/input')
    link.send_keys(listings_links[index])

    time.sleep(3)

    # logging if you need to adjust sleep time based on webpage loading time and browser responsiveness
    print('will click')

    submit = driver.find_element(by=By.CSS_SELECTOR,
                                 value='#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > '
                                       'div.lRwqcd > div')
    time.sleep(1)
    submit.click()
    print('clicked submit')
    time.sleep(4)

    another_response = driver.find_element(by=By.CSS_SELECTOR, value='div.c2gzEf > a')
    time.sleep(1)
    another_response.click()
    print('clicked another response')
    time.sleep(3)

    print(f'done with iteration: {index + 1}')

print('done all!')
