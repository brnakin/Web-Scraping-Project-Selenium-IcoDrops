from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
import pandas as pd
import time


def wait_and_click(driver, xpath, timeout=10):
    print(f"Attempting to click element with xpath: {xpath}")
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    print(f"Element found, clicking on it: {xpath}")
    element.click()


def load_all_content(driver):
    print("Loading all content (showing more items)...")
    while True:
        try:
            wait_and_click(driver, "//button[contains(text(), 'Show more')]", timeout=5)
            time.sleep(3)
        except TimeoutException:
            print("No more 'Show more' button found, in given time.")
            break
        except ElementNotInteractableException:
            print("No more 'Show more' button found, all content loaded.")
            break
        except ElementClickInterceptedException:
            print("Element is not clickable at the moment, waiting...")
            time.sleep(5)


def extract_ico_data(driver, index):
    data = {}
    try:
        base_xpath = f'//*[@id="table-list"]/li[{index}]'
        xpaths = {
            "project_name": f"{base_xpath}/div[2]/div/a/p[1]",
            "project_ticker": f"{base_xpath}/div[2]/div/a/p[2]",
            "project_link": f"{base_xpath}/div[2]/div/a",
            "project_round": f"{base_xpath}/div[3]/p",
            "project_total_raised": f"{base_xpath}/div[4]/p",
            "project_pre_valuation": f"{base_xpath}/div[5]/p[1]",
            "project_categories": f"{base_xpath}/div[8]/p",
            "project_roi": f"{base_xpath}/div[9]/p[1]",
            "project_date": f"{base_xpath}/div[10]/time",
        }

        for key, xpath in xpaths.items():
            try:
                if key == "project_link":
                    data[key] = driver.find_element(By.XPATH, xpath).get_attribute(
                        "href"
                    )
                else:
                    data[key] = driver.find_element(By.XPATH, xpath).text
                print(f"Extracted {key}: {data[key]}")
            except NoSuchElementException:
                data[key] = None
                print(f"{key} not found.")

        investors_count = 0
        try:
            for i in range(1, 4):
                try:
                    driver.find_element(By.XPATH, f"{base_xpath}/div[6]/ul/li[{i}]/img")
                    investors_count += 1
                except NoSuchElementException:
                    break

            try:
                additional = driver.find_element(
                    By.XPATH, f"{base_xpath}/div[6]/ul/li[4]/span"
                ).text
                investors_count += int(additional.replace("+", ""))
            except NoSuchElementException:
                pass
        except Exception:
            pass

        data["project_total_investors"] = (
            investors_count if investors_count > 0 else None
        )

        print(f"Extracted project_total_investors: {investors_count}")

    except Exception as e:
        print(f"Error extracting data: {e}")

    return data


def main():
    print("Starting the web scraping process...")
    chrome_options = Options()
    
    # For faster scraping, we can use headless mode (no GUI) and disable GPU and sandbox mode for Chrome browser.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)

    try:
        print("Navigating to the ICO Drops page...")
        driver.get("https://icodrops.com/category/ended-ico/")

        try:
            wait_and_click(driver, "//button[contains(text(), 'Agree')]")
        except TimeoutException:
            print("Consent button not found or already agreed.")

        time.sleep(3)
        load_all_content(driver)

        ico_count = len(driver.find_elements(By.XPATH, '//*[@id="table-list"]/li'))
        print(f"Found {ico_count} ICOs on the page.")
        all_data = []

        for i in range(1, ico_count + 1):
            print(f"\nProcessing ICO {i}/{ico_count}")
            if i % 5 == 0:
                element = driver.find_element(
                    By.XPATH, f'//*[@id="table-list"]/li[{i}]'
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)

            data = extract_ico_data(driver, i)
            all_data.append(data)

        print("Converting data to DataFrame...")
        df_ico = pd.DataFrame(all_data)
        print(f"Saving data to CSV file (icodrops.csv)...")
        df_ico.to_csv("icodrops.csv", index=False)

    finally:
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    main()
