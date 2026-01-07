from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
chrome_options.add_experimental_option("detach", True)

# Set up the driver outside the loop if you want to reuse the same window
# Or inside the loop if you want a fresh browser every time
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

counter = 0

try:
    while True: 
        counter += 1
        print(f"\n--- Starting Cycle #{counter} ---")

        try:
            # 1. OPEN WEBSITE
            driver.get("https://employers.blueshirt.work/hr?menu=Applicant%20Welfare&signup_step=Welcome&verif=")
            driver.maximize_window()

            # Wait for overlays
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))

            # 2. TRIGGER LOGIN
            login_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log in')]")))
            login_trigger.click()

            # 3. FILL CREDENTIALS
            email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            email_field.clear()
            email_field.send_keys("martinjorrellgaspar@gmail.com")

            password_field = driver.find_element(By.XPATH, "//input[@type='password']")
            password_field.clear()
            password_field.send_keys("testing123")
            
            # 4. SUBMIT
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
            submit_button.click()

            # 5. WAIT FOR HOME & LOGOUT
            wait.until(EC.url_contains("menu=Home"))
            print(f"Cycle #{counter}: Login successful. Waiting to log out...")
            time.sleep(5) 

            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
            caret_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@src, 'mdi_caret.svg')]")))
            caret_icon.click()

            logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log Out')]")))
            logout_btn.click()
            
            print(f"Cycle #{counter}: Logout successful!")

        except Exception as e:
            print(f"Error in Cycle #{counter}: {e}")
            driver.save_screenshot(f"error_cycle_{counter}.png")
            # If an error happens, we go back to the start of the loop

        # --- LOOP CONTROL ---
        print("Waiting 10 seconds before starting next cycle...")
        time.sleep(10) 

except KeyboardInterrupt:
    print("\nLoop stopped by user.") #ctrl + C to stop the loop or just exit the script

finally:
    driver.quit()
