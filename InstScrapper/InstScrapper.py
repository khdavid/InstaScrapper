from calendar import c
from re import T
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
import os

chrome_profile_path = r"C:\Users\David.Khudaverdyan\AppData\Local\Google\Chrome\User Data - Copy"
working_dir = r"D:/temp/inst/"
temp_screenshot_file_name = "full_screenshot.png"
instagram_profile_name = r"kunzhut_kunzhut"
url_instagram = r"https://www.instagram.com/" 
first_picture_coords = [760, 380]
cropping_bbox = [376, 21, 1521, 754]
max_iteratinos = 50


def take_screenshot(driver, filename):
    temp_screenshot_path = working_dir + temp_screenshot_file_name
    driver.save_screenshot(temp_screenshot_path)
    from PIL import Image
    image = Image.open(temp_screenshot_path)
    cropped_image = image.crop((cropping_bbox[0], cropping_bbox[1], cropping_bbox[2], cropping_bbox[3]))
    cropped_image.save(os.path.join(working_dir, instagram_profile_name, filename))
    
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        

def navigate_and_capture(driver, iterations):
    create_directory_if_not_exists(working_dir + instagram_profile_name)
    for i in range(iterations):
        screenshot_filename = f"screenshot_{i}.png"
        take_screenshot(driver, screenshot_filename)
        current_url = driver.current_url
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
        time.sleep(0.5)
    
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
  driver.get(url_instagram + instagram_profile_name)
  sleep(1)

def click_on_first_picture(driver):
  action = ActionChains(driver)
  action.move_by_offset(first_picture_coords[0], first_picture_coords[1]).perform()
  action.click().perform()
  

driver = create_driver();
open_instagram_profile(driver)
click_on_first_picture(driver)
navigate_and_capture(driver, max_iteratinos)
