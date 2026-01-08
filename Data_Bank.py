from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import random
import pyautogui

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

def run_bulk_upload_cycle(counter):
    try:
        print(f"\n--- Starting Cycle #{counter} ---")
        
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

        # 2. NAVIGATE
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

        # 3. FILE SELECTION
        all_files = [f for f in os.listdir(CV_FOLDER_PATH) if os.path.isfile(os.path.join(CV_FOLDER_PATH, f))]
        selected_files = random.sample(all_files, 15) if len(all_files) >= 15 else all_files
        file_paths = ' '.join([f'"{os.path.join(CV_FOLDER_PATH, f)}"' for f in selected_files])

        # 4. UPLOAD ACTION
        upload_zone = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Group.cnaWcaZ")))
        upload_zone.click()
        time.sleep(2) 

        pyautogui.write(file_paths)
        pyautogui.press('enter')
        print(f"Cycle #{counter}: Successfully sent {len(selected_files)} files.")

        # 5. WAIT & LOGOUT
        time.sleep(15) # Wait for site processing
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
        
        caret_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@src, 'mdi_caret.svg')]")))
        driver.execute_script("arguments[0].click();", caret_icon)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log Out')]"))).click()
        print(f"Cycle #{counter}: Logout successful.")

    except Exception as e:
        print(f"Error in Cycle #{counter}: {e}")
        driver.save_screenshot(f"error_cycle_{counter}.png")

# --- CONTINUOUS LOOP CONTROL ---
counter = 0
try:
    while True:
        counter += 1
        run_bulk_upload_cycle(counter)
        
        print(f"--- Cycle #{counter} Complete ---")
        print("Waiting 10 seconds before starting next cycle (Press Ctrl+C to Stop)...")
        time.sleep(20) 

except KeyboardInterrupt:
    print("\n[USER STOP] Loop interrupted by Ctrl+C.")

finally:
    print("Cleaning up and closing browser...")
    driver.quit()
