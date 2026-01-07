from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15) 

try:
 
    driver.get("https://employers.blueshirt.work/hr?menu=Databank&dbf=COMPLETED")
    driver.maximize_window()


    print("Looking for the Log in button...")
    login_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log in')]")))
    login_trigger.click()
    print("Log in button clicked!")

    time.sleep(2) 
    
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    email_field.send_keys("martinjorrellgaspar@gmail.com")

    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.send_keys("testing123")


    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
    submit_button.click()
    
    print("Credentials submitted!")

   
    input("Successfully logged in! Press Enter here in the terminal to close the browser...")

finally:
    driver.quit()