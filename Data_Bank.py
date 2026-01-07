from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import random
import pyautogui # Required to interact with the Windows File Dialog

# --- CONFIGURATION ---
CV_FOLDER_PATH = "C:\\Users\\ADMIN'\\Documents\\cv testing bulk\\CVTESTING"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 25)

def run_bulk_upload_cycle():
    try:
        # 1. LOGIN
        driver.get("https://employers.blueshirt.work/hr?menu=Applicant%20Welfare&signup_step=Welcome&verif=")
        driver.maximize_window()
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))

        login_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log in')]")))
        login_trigger.click()

        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_field.clear()
        email_field.send_keys("martinjorrellgaspar@gmail.com")
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.clear()
        password_field.send_keys("testing123")
        
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
        driver.find_element(By.ID, "login-btn").click()

        # 2. NAVIGATE TO BULK UPLOAD
        wait.until(EC.url_contains("menu=Home"))
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
        
        # Expand Sidebar
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Icon.cnaMaJy"))).click()
        time.sleep(1)

        # Go to Databank
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='MY DATA BANK']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Databank']"))).click()
        
        # Add Jobseeker -> Bulk Upload
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Add Jobseeker')]"))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Bulk Upload')]"))).click()

        # 3. SELECT RANDOM CVS
        print("Selecting 15 random CVs from folder...")
        all_files = [f for f in os.listdir(CV_FOLDER_PATH) if os.path.isfile(os.path.join(CV_FOLDER_PATH, f))]
        
        if len(all_files) < 15:
            print(f"Warning: Only {len(all_files)} files found. Uploading all of them.")
            selected_files = all_files
        else:
            selected_files = random.sample(all_files, 15)

        # Create the full path string for Windows (files separated by spaces/quotes)
        file_paths = ' '.join([f'"{os.path.join(CV_FOLDER_PATH, f)}"' for f in selected_files])

        # 4. TRIGGER UPLOAD DIALOG
        print("Opening upload dialog...")
        upload_zone = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Group.cnaWcaZ")))
        upload_zone.click()
        
        # Give the Windows Dialog a moment to pop up
        time.sleep(2) 

        # 5. USE PYAUTOGUI TO TYPE PATHS AND PRESS ENTER
        pyautogui.write(file_paths)
        pyautogui.press('enter')
        print(f"Sent {len(selected_files)} files to the browser.")

        # 6. WAIT FOR LOAD & LOGOUT
        print("Waiting for upload to process...")
        time.sleep(10) # Adjust based on how long the site takes to process 15 CVs
        
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
        caret_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@src, 'mdi_caret.svg')]")))
        driver.execute_script("arguments[0].click();", caret_icon)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log Out')]"))).click()
        print("Cycle finished successfully.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

# --- MAIN LOOP ---
try:
    while True:
        run_bulk_upload_cycle()
        print("\n" + "="*30)
        choice = input("Press [ENTER] to run again or type 'exit' to quit: ").lower()
        if choice == 'exit':
            break
finally:
    driver.quit()