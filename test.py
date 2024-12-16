from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import time

# Path to chromedriver
chromedriver_path = "/usr/local/bin/chromedriver"

# Setup the Service
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with Service and Chrome options
driver = webdriver.Chrome(service=service)

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
                print(
                    "Finished loading content."
                )
                break

        except TimeoutException:
            # If the button is not found within 30 seconds, assume content is fully loaded
            print("No more 'Show more' button found.")
            break

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Always close the driver
    driver.quit()
