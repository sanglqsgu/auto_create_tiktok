import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('C:/Users/PC/project/alphabot/auto_create_acc/chromedriver-win64/chromedriver.exe')  # Optional argument, if not specified will search path.

driver.get('https://www.tiktok.com/signup/phone-or-email/email')

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/form/div[5]/div/input")

search_box.send_keys('abc@gmail.com')

time.sleep(5) # Let the user actually see something!

driver.quit()