from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument(
    "--headless"
)  # headless chrome for less overhead and faster

# Path to chromedriver
chromedriver_path = (
    "/usr/local/bin/chromedriver"  # Update this with the actual path to chromedriver
)

# Setup the Service
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with Service and Chrome options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set window size
driver.set_window_size(1320, 550)

# Navigate to the page
ico_link = "https://icodrops.com/category/ended-ico/"
driver.get(ico_link)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/button"))
)

show_more = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/button")
show_more.click()


# Always remember to close the driver when you're done
driver.quit()
