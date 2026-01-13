from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains  # For double-click
import time
import random
import string

# ---------------- CONFIG ----------------
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

JOB_TYPES = ["ACTIVE", "PENDING", "DRAFT", "CLOSED"]
POSITION_TITLES = [
    "Software Developer", "Senior Engineer", "Project Manager",
    "Data Analyst", "UX Designer", "DevOps Engineer",
    "QA Tester", "Business Analyst", "Product Manager",
    "Marketing Specialist", "HR Coordinator", "Sales Representative"
]

# ---------------- HELPERS ----------------
def get_random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def wait_for_loading():
    time.sleep(2)

def safe_click(el):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.4)
    try:
        el.click()
    except:
        driver.execute_script("arguments[0].click();", el)

def safe_send_keys(el, text):
    el.send_keys(Keys.CONTROL + "a")
    el.send_keys(Keys.BACKSPACE)
    time.sleep(0.2)
    el.send_keys(text)

def react_text_input(element, text):
    """React-compatible text input handler"""
    driver.execute_script("""
        const input = arguments[0];
        const text = arguments[1];
        input.focus();
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        for (let char of text) {
            input.value += char;
            input.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, key: char }));
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('blur', { bubbles: true }));
    """, element, text)

def react_int_input(element, value: int):
    """Enhanced React/Bubble integer input handler"""
    val_str = str(int(value))
    driver.execute_script("""
        const el = arguments[0];
        el.focus();
        el.value = arguments[1];
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));
    """, element, val_str)
    time.sleep(0.5)

# ---------------- MAIN ----------------
def login():
    """Perform initial login - only called once"""
    driver.get("https://employers.blueshirt.work/hr")
    driver.maximize_window()
    wait_for_loading()

    print("Logging in...")
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log in')]")))
    safe_click(login_btn)
    
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    safe_send_keys(email_field, "martinjorrellgaspar@gmail.com")
    
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    safe_send_keys(password_field, "testing123")
    
    login_submit = driver.find_element(By.ID, "login-btn")
    safe_click(login_submit)
    wait.until(EC.url_contains("Home"))
    print("✅ Login successful")

def navigate_to_job_order():
    """Navigate to Job Order page and click Add Job Order"""
    print("Navigating to Job Order...")
    
    # Try to click sidebar toggle - it might already be open on subsequent runs
    try:
        sidebar_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Icon.cnaMaJy")))
        safe_click(sidebar_toggle)
        time.sleep(1)
    except:
        print("  Sidebar already open or not found, continuing...")
        time.sleep(0.5)
    
    # Click JOB ORDER menu
    try:
        job_order_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'JOB ORDER')]")))
        safe_click(job_order_menu)
        time.sleep(2)
    except:
        print("  Already on Job Order page, continuing...")
        time.sleep(1)
    
    # Click Add Job Order button
    add_job_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Job Order')]")))
    safe_click(add_job_btn)
    time.sleep(3)
    print("✅ Navigation complete")

def create_job_order():

    # ============ CLIENT SELECTION (Double-Click) ============
    print("Opening Client Search...")
    client_trigger = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bubble-element.Text.cnaMaQb")))
    ActionChains(driver).double_click(client_trigger).perform()
    
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.cnaMaOl")))
    safe_send_keys(search_input, "testing")
    time.sleep(1.5)
    
    client_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cnaMaOe')]//div[text()='testing']")))
    safe_click(client_option)
    print("✅ Client 'testing' selected")
    time.sleep(1)

    # ============ FORM FILLING ============
    print("Filling job order form...")
    
    # Job Order Name
    job_name = f"JO_{get_random_string()}"
    job_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Job Order')]/following::input[1]")))
    safe_send_keys(job_name_field, job_name)
    print(f"  Job Name: {job_name}")

    # Type Dropdown
    type_dropdown = driver.find_element(By.XPATH, "//*[contains(text(),'Type')]/following::input[1]")
    safe_click(type_dropdown)
    selected_type = random.choice(JOB_TYPES)
    type_dropdown.send_keys(selected_type)
    type_dropdown.send_keys(Keys.ENTER)
    time.sleep(0.5)
    print(f"  Type: {selected_type}")

    # Position Title
    selected_position = random.choice(POSITION_TITLES)
    pos_title = driver.find_element(By.XPATH, "//input[@placeholder='Position']")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pos_title)
    time.sleep(0.5)
    react_text_input(pos_title, selected_position)
    time.sleep(0.5)
    print(f"  Position: {selected_position}")

    # Position Quantity
    qty_value = random.randint(1, 10)
    pos_qty = driver.find_element(By.XPATH, "//input[@placeholder='Quantity']")
    safe_send_keys(pos_qty, str(qty_value))
    pos_qty.send_keys(Keys.TAB)
    time.sleep(0.5)
    print(f"  Quantity: {qty_value}")

    # Position Amount
    amount_value = random.randint(1000, 50000)
    pos_amt = driver.find_element(By.CSS_SELECTOR, ".cnaQaZr0")
    safe_send_keys(pos_amt, str(amount_value))
    time.sleep(0.5)
    print(f"  Amount: {amount_value}")

    # Add Position to list
    add_btn = driver.find_element(By.CSS_SELECTOR, "button.cnaQaaB0")
    safe_click(add_btn)
    time.sleep(2)
    print("  ✅ Position added")

    # Status Dropdown
    status_field = driver.find_element(By.XPATH, "//*[contains(text(),'Status')]/following::input[1]")
    safe_click(status_field)
    selected_status = random.choice(JOB_TYPES)
    status_field.send_keys(selected_status)
    status_field.send_keys(Keys.ENTER)
    time.sleep(0.5)
    print(f"  Status: {selected_status}")

    # ============ CALENDAR SELECTION ============
    print("Selecting a random future date...")
    date_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.date_div.picker__input")))
    safe_click(date_input)
    time.sleep(1)
    
    # Select infocus days that are NOT disabled
    available_days = driver.find_elements(By.CSS_SELECTOR, ".picker__day--infocus:not(.picker__day--disabled)")
    if available_days:
        target_day = random.choice(available_days)
        safe_click(target_day)
        print("✅ Random date selected")
    else:
        driver.find_element(By.CSS_SELECTOR, ".picker__button--today").click()
        print("✅ Today's date selected")
    time.sleep(1)

    # ============ TOTAL DEPLOYMENT (The State Fix) ============
    print("Setting Deployment Quantity...")
    deployment_value = random.randint(1, 20)
    deploy_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[inputmode='numeric'].cnaPfaP")))
    react_int_input(deploy_field, deployment_value)
    print(f"  Deployment: {deployment_value}")

    # ============ SELECT ALL ============
    print("Clicking Select All...")
    select_all_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Select All')]")))
    safe_click(select_all_btn)
    time.sleep(1)
    print("  ✅ Select All clicked")

    # ============ SAVE BUTTON ============
    print("Waiting for Save button to be enabled...")
    # Wait for the Save button to be clickable (not grayed out)
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')]")))
    
    # Additional check to ensure it's not disabled via opacity or background color
    max_attempts = 10
    for attempt in range(max_attempts):
        opacity = save_btn.value_of_css_property("opacity")
        bg_color = save_btn.value_of_css_property("background-color")
        
        # Check if button is enabled (opacity should be 1, not grayed out)
        if opacity == "1" or float(opacity) >= 0.9:
            print("  Save button is enabled, clicking...")
            safe_click(save_btn)
            time.sleep(2)
            print("  ✅ Save button clicked")
            break
        else:
            print(f"  Attempt {attempt + 1}/{max_attempts}: Button not ready (opacity: {opacity}), waiting...")
            time.sleep(0.5)
    else:
        print("  ⚠️ Warning: Save button may not be fully enabled, but proceeding...")
        safe_click(save_btn)
        time.sleep(2)

    print(f"\n{'='*50}")
    print(f"✅ JOB ORDER CREATED: {job_name}")
    print(f"{'='*50}")
    print(f"   - Client: testing")
    print(f"   - Type: {selected_type}")
    print(f"   - Position: {selected_position}")
    print(f"   - Quantity: {qty_value}")
    print(f"   - Amount: {amount_value}")
    print(f"   - Status: {selected_status}")
    print(f"   - Deployment: {deployment_value}")
    print(f"{'='*50}\n")

# ---------------- RUN LOOP ----------------
if __name__ == "__main__":
    counter = 0
    try:
        # ============ INITIAL LOGIN (Only Once) ============
        print("\n" + "="*60)
        print("PERFORMING INITIAL LOGIN")
        print("="*60 + "\n")
        login()
        
        # ============ JOB ORDER CREATION LOOP ============
        while True:
            counter += 1
            print(f"\n{'='*60}")
            print(f"STARTING JOB ORDER CYCLE #{counter}")
            print(f"{'='*60}\n")
            
            # Navigate to job order and create
            navigate_to_job_order()
            create_job_order()
            
            print(f"\n⏳ Waiting 5 seconds before next cycle...")
            print(">>> Press CTRL + C to STOP <<<\n")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[STOPPED] Loop terminated by user.")
    finally:
        print("Closing browser...")
        driver.quit()