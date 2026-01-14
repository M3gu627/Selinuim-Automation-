from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import pyautogui

# ---------------- CONFIG ----------------
CV_FOLDER_PATH = "C:\\Users\\ADMIN'\\Documents\\cv testing bulk\\CVTESTING"

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 25)

# ---------------- HELPERS ----------------
def wait_for_loading():
    """Wait for loading screen to disappear"""
    try:
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "greyout")))
    except:
        pass
    time.sleep(1)

def safe_click(el):
    """Safe click with scroll into view"""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.4)
    try:
        el.click()
    except:
        driver.execute_script("arguments[0].click();", el)

# ---------------- MAIN ----------------
def login():
    """Perform initial login - only called once"""
    driver.get("https://employers.blueshirt.work/hr?menu=Applicant%20Welfare&signup_step=Welcome&verif=")
    driver.maximize_window()
    wait_for_loading()

    print("Logging in...")
    login_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log in')]")))
    safe_click(login_trigger)

    # Fill Credentials
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    email_field.clear()
    email_field.send_keys("martinjorrellgaspar@gmail.com")
    
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.clear()
    password_field.send_keys("testing123")
    
    # Submit Login
    wait_for_loading()
    driver.find_element(By.ID, "login-btn").click()
    wait.until(EC.url_contains("menu=Home"))
    print("✅ Login successful")

def navigate_to_databank():
    """Navigate to Databank page"""
    print("Navigating to Databank...")
    wait_for_loading()
    
    # Try to expand sidebar - it might already be open
    try:
        sidebar_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Icon.cnaMaJy")))
        safe_click(sidebar_toggle)
        time.sleep(1)
    except:
        print("  Sidebar already open or not found, continuing...")
        time.sleep(0.5)

    # Click MY DATA BANK menu
    try:
        data_bank_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='MY DATA BANK']")))
        safe_click(data_bank_menu)
        time.sleep(1)
    except:
        print("  MY DATA BANK already expanded, continuing...")
        time.sleep(0.5)
    
    # Click Databank
    try:
        databank_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Databank']")))
        safe_click(databank_link)
        time.sleep(2)
    except:
        print("  Already on Databank page, continuing...")
        time.sleep(1)
    
    wait_for_loading()
    print("✅ Navigation complete")

def bulk_upload_cvs():
    """Perform bulk CV upload"""
    
    # Reset page state - close any open dropdowns
    print("Resetting page state...")
    pyautogui.press('escape')
    time.sleep(0.5)
    pyautogui.press('escape')
    time.sleep(1)
    wait_for_loading()

    # ============ OPEN BULK UPLOAD MODAL ============
    print("Opening Bulk Upload modal...")
    
    # Click Add Jobseeker dropdown
    add_jobseeker_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Add Jobseeker')]")))
    safe_click(add_jobseeker_btn)
    time.sleep(2)  # Wait for dropdown to appear
    
    # Click Bulk Upload option (target the clickable Group container)
    bulk_upload_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'Group') and contains(@class, 'clickable-element')]//div[text()='Bulk Upload']/ancestor::div[contains(@class, 'clickable-element')][1]")))
    safe_click(bulk_upload_option)
    time.sleep(2)  # Wait for upload modal
    print("✅ Bulk Upload modal opened")

    # ============ SCAN PDF FILES ============
    print("Scanning folder for PDF files...")
    all_pdfs = [f for f in os.listdir(CV_FOLDER_PATH) if f.lower().endswith('.pdf')]
    
    if not all_pdfs:
        print("❌ No PDF files found! Skipping this cycle.")
        return False

    print(f"✅ Found {len(all_pdfs)} PDF files")
    file_paths = ' '.join([f'"{os.path.join(CV_FOLDER_PATH, f)}"' for f in all_pdfs])

    # ============ TRIGGER UPLOAD ============
    print("Clicking upload zone...")
    upload_zone = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Group.cnaWcaZ")))
    upload_zone.click()
    
    # Wait for Windows file dialog
    time.sleep(2) 

    # Paste file paths and submit
    print("Pasting file paths and submitting...")
    pyautogui.write(file_paths)
    pyautogui.press('enter')
    print(f"✅ Successfully sent {len(all_pdfs)} files to browser")

    # ============ WAIT FOR PROCESSING ============
    print("⏳ Waiting 30 seconds for processing...")
    time.sleep(30)
    wait_for_loading()
    
    print(f"\n{'='*50}")
    print(f"✅ BULK UPLOAD COMPLETED")
    print(f"{'='*50}")
    print(f"   - Files uploaded: {len(all_pdfs)}")
    print(f"{'='*50}\n")
    
    return True

# ---------------- RUN LOOP ----------------
if __name__ == "__main__":
    counter = 0
    try:
        # ============ INITIAL LOGIN (Only Once) ============
        print("\n" + "="*60)
        print("PERFORMING INITIAL LOGIN")
        print("="*60 + "\n")
        login()
        
        # ============ BULK UPLOAD LOOP ============
        while True:
            counter += 1
            print(f"\n{'='*60}")
            print(f"STARTING BULK UPLOAD CYCLE #{counter}")
            print(f"{'='*60}\n")
            
            try:
                # Navigate to databank and perform upload
                navigate_to_databank()
                success = bulk_upload_cvs()
                
                if success:
                    print(f"\n⏳ Waiting 10 seconds before next cycle...")
                    print(">>> Press CTRL + C to STOP <<<\n")
                    time.sleep(10)
                else:
                    print(f"\n⚠️ No files to upload, waiting 30 seconds...")
                    time.sleep(30)
                    
            except Exception as e:
                print(f"\n✗ ERROR in Cycle #{counter}: {e}")
                driver.save_screenshot(f"error_cycle_{counter}.png")
                
                # Try to recover
                try:
                    print("⚠️ Attempting recovery...")
                    pyautogui.press('escape')
                    time.sleep(1)
                    pyautogui.press('escape')
                    time.sleep(2)
                    print("✅ Recovery successful, continuing to next cycle...")
                except:
                    print("✗ Recovery failed, but will try next cycle...")
                
                time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[STOPPED] Loop terminated by user.")
    finally:
        print("Closing browser...")
        driver.quit()
