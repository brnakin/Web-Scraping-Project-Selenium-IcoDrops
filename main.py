from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.chrome.options import Options

import time

# Setup Chrome options
chrome_options = Options()

# Headless chrome for less overhead and faster
chrome_options.add_argument("--headless")

# Path to chromedriver
chromedriver_path = "/usr/local/bin/chromedriver"

# Setup the Service
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with Service and Chrome options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set window size
driver.set_window_size(1920, 1080)

try:
    # Navigate to the page
    ico_link = "https://icodrops.com/category/ended-ico/"
    driver.get(ico_link)

    # Wait and click 'Agree' button
    try:
        consent_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(text(), 'Agree') or contains(text(), 'Accept')]",
                )
            )
        )
        consent_button.click()
    except TimeoutException:
        print("Consent button not found or not clickable")

    time.sleep(5)

    # Repeatedly click 'Show more' button
    while True:
        try:
            # Wait up to 30 seconds for the 'Show more' button to be present and visible
            show_more_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(), 'Show more')]")
                )
            )

            try:
                # Attempt to click the button and wait for 5 seconds
                show_more_button.click()
                time.sleep(5)
            except ElementNotInteractableException:
                # If the button is found but not clickable, break the loop
                print("Finished loading content.")
                break

        except TimeoutException:
            # If the button is not found within 30 seconds, assume content is fully loaded
            print("No more 'Show more' button found.")
            break

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:

    # Initialize a dictionary to store all ICO data
    ico_data = {
        "project_name": [],
        "project_ticker": [],
        "project_link": [],
        "round": [],
        "total_raised": [],
        "pre_valuation": [],
        "investors": [],
        "ecosystem": [],
        "categories": [],
        "roi": [],
        "date": [],
    }

    # Find all ICO links to determine the length
    ico_links = driver.find_elements("xpath", '//*[@id="table-list"]/li/div[2]/div/a')

    print(f"Total ICOs found: {len(ico_links)}")

    # Extract information for each ICO
    for i in range(len(ico_links)):
        # We use i+1 for the XPath index since XPath indices start at 1
        index = str(i + 1)

        try:
            project_name = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[2]/div/a/p[1]'
            ).text
        except NoSuchElementException:
            project_name = None
        ico_data["project_name"].append(project_name)

        try:
            project_ticker = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[2]/div/a/p[2]'
            ).text
        except NoSuchElementException:
            project_ticker = None
        ico_data["project_ticker"].append(project_ticker)

        try:
            project_link = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[2]/div/a'
            ).get_attribute("href")
        except NoSuchElementException:
            project_link = None
        ico_data["project_link"].append(project_link)

        try:
            round = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[3]/p'
            ).text
        except NoSuchElementException:
            round = None
        ico_data["round"].append(round)

        try:
            total_raised = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[4]/p'
            ).text
        except NoSuchElementException:
            total_raised = None
        ico_data["total_raised"].append(total_raised)

        try:
            pre_valuation = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[5]/p[1]'
            ).text
        except NoSuchElementException:
            pre_valuation = None
        ico_data["pre_valuation"].append(pre_valuation)

        """
        try:
            investors = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[8]/p'
            ).text
        except NoSuchElementException:
            investors = None
            ico_data["investors"].append(investors)
        """

        try:
            ecosystem = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[7]/ul/li/img'
            ).get_attribute("alt")
        except NoSuchElementException:
            ecosystem = None
            ico_data["ecosystem"].append(ecosystem)

        try:
            categories = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[8]/p'
            ).text
        except NoSuchElementException:
            categories = None
        ico_data["categories"].append(categories)

        try:
            roi = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[9]/p[1]'
            ).text
        except NoSuchElementException:
            roi = None
        ico_data["roi"].append(roi)

        try:
            date = driver.find_element(
                "xpath", f'//*[@id="table-list"]/li[{index}]/div[10]/time'
            ).text
        except NoSuchElementException:
            date = None
        ico_data["date"].append(date)

        print(
            f"Added data for project: #{index} {project_name, project_ticker, project_link, round, total_raised, pre_valuation, categories, roi, date}"
        )

    driver.quit()
