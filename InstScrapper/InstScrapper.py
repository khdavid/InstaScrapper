from calendar import c
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

import time
# Path to your Chrome profile
chrome_profile_path = r"C:\Users\David.Khudaverdyan\AppData\Local\Google\Chrome\User Data - Copy"
url_instagram_profile = r"https://www.instagram.com/kunzhut_kunzhut/"



def take_screenshot(driver, x_min, x_max, y_min, y_max, filename):
    # Take a full-page screenshot and then crop it to the desired area
    driver.save_screenshot(filename)
    # from PIL import Image
    # image = Image.open("full_screenshot.png")
    # cropped_image = image.crop((x_min, y_min, x_max, y_max))
    # cropped_image.save(filename)

def navigate_and_capture(driver, x_min, x_max, y_min, y_max, iterations):
    # Set up the WebDriver

    for i in range(iterations):
        screenshot_filename = f"screenshot_{i}.png"
        take_screenshot(driver, x_min, x_max, y_min, y_max, screenshot_filename)
        print(f"Screenshot {i} saved.")
        
        # Navigate forward
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
        
        # Wait a bit for the page to load/update
        time.sleep(0.5)  # Adjust this delay as necessary for page load times
        
    driver.quit()
    
def create_driver():
  # Create ChromeOptions object
  chrome_options = webdriver.ChromeOptions()
  
  # Add the path to your profile directory
  chrome_options.add_argument("user-data-dir=" + chrome_profile_path)
  chrome_options.add_argument("--profile-directory=Profile 1")  # Add this line if your profile directory has a specific name
  
  
  # Initialize Chrome driver with the specified options
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def open_instagram_profile(driver):
  driver.get(url_instagram_profile)
  sleep(1)

def click_on_first_picture(driver):
  action = ActionChains(driver)
  action.move_by_offset(760, 380).perform()
  action.click().perform()
  

driver = create_driver();
open_instagram_profile(driver)
click_on_first_picture(driver)
# navigate_and_capture(driver, 100, 800, 100, 600, 5)
