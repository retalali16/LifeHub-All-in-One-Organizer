from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    driver.get("http://127.0.0.1:5000/")
    print("Opened LifeHub App")

    # Add Task
    driver.find_element(By.LINK_TEXT, "Add Todo").click()
    print("Clicked Add Todo")
    time.sleep(2)  # Wait longer to visualize
    
    driver.find_element(By.NAME, "name").send_keys("Test Task")
    driver.find_element(By.NAME, "description").send_keys("Test Description")
    driver.find_element(By.NAME, "due_date").send_keys("2024-12-31")
    driver.find_element(By.NAME, "priority").send_keys("High")
    print("Filled Task Form")
    time.sleep(2)
    
    driver.find_element(By.NAME, "submit").click()
    print("Submitted Task")
    time.sleep(3)  # Wait longer to visualize submission
    
    # Handle SweetAlert (Wait for it and Accept)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'swal2-container')))
        print("Alert Appeared")
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[text()="OK"]').click()
        print("Clicked OK on Alert")
        WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'swal2-container')))
        time.sleep(2)
    except Exception as e:
        print("No alert appeared, continuing...")

    # Edit Task
    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Edit")]'))
    )
    edit_button.click()
    print("Clicked Edit Task")
    time.sleep(3)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "description")))
    
    desc_field = driver.find_element(By.NAME, "description")
    desc_field.clear()
    desc_field.send_keys("Updated Description")
    print("Updated Description Field")
    time.sleep(2)
    
    driver.find_element(By.NAME, "submit").click()
    print("Submitted Edit")
    time.sleep(3)

    # Handle Alert After Edit
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'swal2-container')))
        print("Alert After Edit Appeared")
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[text()="OK"]').click()
        print("Dismissed Edit Alert")
        WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'swal2-container')))
        time.sleep(2)
    except Exception as e:
        print("No alert appeared after edit, continuing...")

    # Delete Task
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Delete")]'))
    )
    delete_button.click()
    print("Clicked Delete Task")
    time.sleep(3)
    
    # Confirm Delete Alert
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    print("Confirmed Delete Alert")
    time.sleep(3)
    
    # Confirm Redirect to Main Page
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:5000/"))
    print("Redirected to Home Page")

    print("Test Passed: Task Added, Edited, and Deleted Successfully!")

except Exception as e:
    print("Test Failed:", e)

finally:
    driver.quit()
