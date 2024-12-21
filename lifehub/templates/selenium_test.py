from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Maximize window
    # Automatically install the latest Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Extract product details from the page
def extract_product_details(driver):
    try:
        # Extract product title
        title = driver.find_element(By.ID, "productTitle").text
        
        # Extract product URL (current URL of the product page)
        url = driver.current_url
        
        # Extract product price (if available)
        try:
            price = driver.find_element(By.ID, "priceblock_ourprice").text
        except:
            price = "Price not available"
        
        # Extract product rating (if available)
        try:
            rating = driver.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text
        except:
            rating = "Rating not available"

        # Print extracted details
        print(f"Product Title: {title}")
        print(f"Product URL: {url}")
        print(f"Product Price: {price}")
        print(f"Product Rating: {rating}")

    except Exception as e:
        print(f"Error extracting product details: {e}")

# Take a screenshot and save it
def take_screenshot(driver, filename="product_page_screenshot.png"):
    driver.save_screenshot(filename)
    print(f"Screenshot saved as {filename}")

# Main automation function
def automate_search(product_name):
    # Initialize the browser
    driver = init_driver()
    
    try:
        # Open Amazon website
        driver.get("https://www.amazon.com/")
        
        # Wait for the search bar to be visible and enter product name
        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_bar.send_keys(product_name)
        search_bar.send_keys(Keys.RETURN)  # Press Enter

        # Wait for search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot")))

        # Click on the first product in the search results
        first_product = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-main-slot .s-result-item h2 a")))
        first_product.click()

        # Wait for the product page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))

        # Extract product details
        extract_product_details(driver)

        # Take a screenshot
        take_screenshot(driver)

    except Exception as e:
        print(f"Error during automation: {e}")
    
    finally:
        # Close the browser after a short delay
        time.sleep(5)
        driver.quit()

# Run the script
if __name__ == "__main__":
    product_name = "Laptop"  # Change this to any product you want to search
    automate_search(product_name)















