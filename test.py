"""
Scrapes the upcoming ICO drops data 
Written by: Michael Judd
"""

from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


# Path to chromedriver
chromedriver_path = (
    "/usr/local/bin/chromedriver"  # Update this with the actual path to chromedriver
)

# Setup the Service
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with Service and Chrome options
driver = webdriver.Chrome(service=service)

# Set window size
driver.set_window_size(1320, 550)

exchange_link = "https://icodrops.com/category/upcoming-ico/"  # could easily be changed for previous ico with this link
driver.get(exchange_link)

wait = WebDriverWait(driver, 30)
ico_links = driver.find_element(
    "xpath", '//*[@id="ajaxc"]/div/div/div[*]/a'
)  # get all ico page links

# Reading through the sheets api i think this is how its data is formatted (list of lists)
ico_data = [
    ["name"],
    ["description"],
    ["category"],
    ["ico_drops_interest"],
    ["hardcap"],
    ["ico_date"],
    ["telegram_link"],
    ["telegram_members"],
    ["twitter_link"],
    ["twitter_followers"],
    ["medium_link"],
]

# iterate through all of the ICO links
for i in range(len(ico_links) - 1):
    i = str(i + 1)  # we have to use an index due to moving between pages
    ico_link = driver.find_element_by_xpath('//*[@id="ajaxc"]/div/div/div[' + i + "]/a")
    name = driver.find_element_by_xpath(
        '//*[@id="ajaxc"]/div/div/div[' + i + "]/a/div/div[1]/div[2]/h3/a"
    ).text

    interest = driver.find_element_by_xpath(
        '//*[@id="ajaxc"]/div/div/div[' + i + "]/a/div/div[2]"
    ).text
    fundraising_goal = driver.find_element_by_xpath(
        '//*[@id="ajaxc"]/div/div/div[' + i + "]/a/div/div[4]"
    ).text
    ico_date = driver.find_element_by_xpath(
        '//*[@id="ajaxc"]/div/div/div[' + i + "]/a/div/div[5]"
    ).text

    # go to the icos page
    ico_link.click()
    description = driver.find_element_by_class_name("ico-description").text
    category = driver.find_element_by_class_name("ico-category-name").text
    ico_start_date = driver.find_element_by_class_name("sale-date").get_attribute(
        "data-date"
    )
    # TODO: figure out intelligent way of scraping and structuring additional relevant data that they have..
    #       The simple way would be to just grab all the text in the <li> elements and put it in an "extra_data" field

    # Get related social media links
    try:
        telegram_link = driver.find_element_by_css_selector(
            '.soc_links a[href^="https://t.me"]'
        ).get_attribute("href")
    except:
        telegram_link = ""
    try:
        twitter_link = driver.find_element_by_css_selector(
            '.soc_links a[href^="https://twitter"]'
        ).get_attribute("href")
    except:
        twitter_link = ""
    try:
        medium_link = driver.find_element_by_css_selector(
            '.soc_links a[href^="https://medium"]'
        )
    except:
        medium_link = ""

    # Check how many telegram users
    num_telegram_members = ""
    if telegram_link:
        driver.get(telegram_link)
        num_telegram_members = driver.find_element_by_class_name("tgme_page_extra").text
        print("TELEGRAMS:", num_telegram_members)

    # get twitter followers from twitter link
    num_twitter_followers = ""
    if twitter_link:
        driver.get(twitter_link)
        num_twitter_followers = driver.find_element_by_xpath(
            '//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/ul/li[3]/a/span[3]'
        ).text

    # add to each relevant list element
    ico_data[0].append(name)
    ico_data[1].append(description)
    ico_data[2].append(category)
    ico_data[3].append(interest)
    ico_data[4].append(fundraising_goal)
    ico_data[5].append(ico_start_date)
    ico_data[6].append(telegram_link)
    ico_data[7].append(num_telegram_members)
    ico_data[8].append(twitter_link)
    ico_data[9].append(num_twitter_followers)
    ico_data[10].append(medium_link)

    driver.get(exchange_link)

# TODO: figure out how to append the data rows to google sheets api
# For appending data: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
body = {"values": ico_data}
