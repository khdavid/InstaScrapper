from calendar import c
from re import T
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime
import time
import os
import shutil

chrome_profile_path = r"C:\Users\David.Khudaverdyan\AppData\Local\Google\Chrome\User Data - Copy"
working_dir = r"D:/temp/inst/"
temp_screenshot_file_name = "full_screenshot.png"
instagram_profile_name = r"kunzhut_kunzhut"
url_instagram = r"https://www.instagram.com/" 

# unmutable constants
first_picture_coords = [760, 380]
cropping_bbox = [376, 25, 1521, 754]
max_iterations = 20000
sleep_after_next_picture_sec = 1
date_class_name = "x1p4m5qa"
date_attribute = "datetime"
next_picture_from_same_set_class_name = "_9zm2"

def take_screenshot(driver, file_path):
    temp_screenshot_path = working_dir + temp_screenshot_file_name
    driver.save_screenshot(temp_screenshot_path)
    from PIL import Image
    image = Image.open(temp_screenshot_path)
    cropped_image = image.crop((cropping_bbox[0], cropping_bbox[1], cropping_bbox[2], cropping_bbox[3]))
    if cropped_image.mode == 'RGBA':
      cropped_image = cropped_image.convert('RGB')    
    
      cropped_image.save(file_path, 'jpeg', quality = 95)
    
def force_create_empty_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory) 

    os.makedirs(directory)

def generate_unique_file_path(file_path_candidate):
    base, ext = os.path.splitext(file_path_candidate)
    ind = 0
    while True:
        result = f"{base}_{ind}{ext}"
        if not os.path.exists(result):
            return result 
        
        ind += 1

def generate_screenshot_file_path(date_time_str, index):
    filename = ''
    if date_time_str:
        filename = f"{date_time_str}.jpg"
    else:
        filename = f"screenshot_{index}.jpg"

    return generate_unique_file_path(
       os.path.join(working_dir, instagram_profile_name, filename))  
        
def go_to_next_picture(driver):
    elements = driver.find_elements(By.CLASS_NAME, next_picture_from_same_set_class_name)
    current_url = driver.current_url
    right_arrow_pressed = False
    if len(elements) > 0:
      elements[0].click() 
    else:
      right_arrow_pressed = True
      driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)

    time.sleep(sleep_after_next_picture_sec)
    
    # this weird logic is needed, since sometimes current_link 
    # is not updated when next picture in set is clicked
    if not right_arrow_pressed:
       return True
    
    return current_url != driver.current_url  
    
def create_log_file_path():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{instagram_profile_name}_{current_time}.log"
    return os.path.join(working_dir, log_filename)
    
def log(full_path, text):
    with open(full_path, 'a') as file:
        file.write(text + "\n")

def navigate_and_capture(driver):
    log_file_path = create_log_file_path()
    log(log_file_path, f"Number of iterations = {max_iterations}");
    force_create_empty_dir(working_dir + instagram_profile_name)
    for index in range(max_iterations):
        date_time_str = extract_datetime(driver)
        screenshot_file_path = generate_screenshot_file_path(date_time_str, index)
        take_screenshot(driver, screenshot_file_path)
        log(log_file_path, f"{index}: path: {screenshot_file_path} url: {driver.current_url}");
        if not go_to_next_picture(driver):
          return;
            
def create_driver():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("user-data-dir=" + chrome_profile_path)
  chrome_options.add_argument("--profile-directory=Profile 1")
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def open_instagram_profile(driver):
  driver.get(url_instagram + instagram_profile_name)
  sleep(1)

def click_on_first_picture(driver):
  action = ActionChains(driver)
  action.move_by_offset(first_picture_coords[0], first_picture_coords[1]).perform()
  action.click().perform()
  
def extract_datetime(driver):
  elements = driver.find_elements(By.CLASS_NAME, date_class_name)
  for element in elements:
    if element.get_attribute(date_attribute):
        datetime_str = element.get_attribute(date_attribute)
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        formatted_date = dt.strftime('%Y-%m-%d_%H-%M-%S')
        return formatted_date
  
  return None

driver = create_driver();
open_instagram_profile(driver)
click_on_first_picture(driver)
navigate_and_capture(driver)
