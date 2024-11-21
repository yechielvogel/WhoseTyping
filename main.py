import asyncio
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from screeninfo import get_monitors
import telegram
import pyautogui
import time
import threading

# Set up the WebDriver for Safari
# driver = webdriver.Safari()

BOT_TOKEN = '7827627496:AAHx2vU2Top43OsizxQmy2ADT5nC2doaKgI'
   
chrome_options = Options()
    
# chrome_options.add_argument("--headless")  # Remove this line to run in regular mode
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36");
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x2700")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
    
    
driver = webdriver.Chrome(options=chrome_options)

# def open_whatsapp():
#     print("Opening WhatsApp Web...")
#     driver.get("https://web.whatsapp.com")
#     input("Please scan the QR code on WhatsApp Web and press Enter once logged in.")
#     print("QR code scanned. Logged in.")


def open_whatsapp():
    print("Opening WhatsApp Web on Chrome...")
    


    driver.get("https://web.whatsapp.com")
    
    try:
        # Wait for the login page to load and for the "Log in with phone number" element to appear
        log_in_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='Log in with phone number']"))
        )
        time.sleep(3)
        driver.execute_script("arguments[0].scrollIntoView(true);", log_in_div)
        driver.execute_script("arguments[0].click();", log_in_div)
        print("Clicked 'Log in with phone number' element.")
    except Exception as e:
        print(f"Error finding 'Log in with phone number' element: {e}")
        driver.quit()
        return
    country = "United Kingdom"
    # country = input("Enter your country (United Kingdom or United States): ").strip()
    if country not in ["United Kingdom", "United States"]:
        print("Invalid country. Exiting...")
        driver.quit()
        return

    try:
        # Open the country dropdown and select the country
        time.sleep(1)
        dropdown_parent = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//button[contains(@class, 'x889kno')])[2]"))
        )
        dropdown_parent.click()
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_parent)
        driver.execute_script("arguments[0].click();", dropdown_parent)
        print("Dropdown opened.")
        
        # Wait and select the country
        time.sleep(1)
        desired_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{country}')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", desired_option)
        driver.execute_script("arguments[0].click();", desired_option)
        print(f"Selected country: {country}")

    except Exception as e:
        print(f"Error selecting country: {e}")
        driver.quit()
        return

    phone_number = "7709004207"
    # phone_number = input("Enter your phone number: ").strip()
    try:
        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", phone_field)
        driver.execute_script("arguments[0].click();", phone_field)
        phone_field.send_keys(phone_number)
        print("Entered phone number.")
    except Exception as e:
        print(f"Error entering phone number: {e}")
        driver.quit()
        return

    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'x889kno') and .//div[contains(text(), 'Next')]]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        print("Clicked 'Next' button.")
    except Exception as e:
        print(f"Error clicking 'Next' button: {e}")
        driver.quit()
        return

    try:
        time.sleep(5)
        

        verification_code_element = driver.find_element(By.XPATH, "//div[@aria-details='link-device-phone-number-code-screen-instructions']")
        verification_code = verification_code_element.get_attribute("data-link-code").strip()
        asyncio.run(send_message(verification_code))
        print(f"Verification Code: {verification_code}")
        time.sleep(20)  
        # input("Please scan the QR code on WhatsApp Web and press Enter once logged in.")
    except Exception as e:
        print(f"Error extracting the verification code: {e}")
        driver.quit()
        return


    
    
def keep_window_active():
    try:
        while True:
            pyautogui.press("shift")  
            time.sleep(5)  
    except KeyboardInterrupt:
        print("Stopping keep_window_active function.")

def random_mouse_movement():
    """
    Simulates random mouse movements in the browser by executing JavaScript.
    This function runs in a separate thread.
    """
    try:
        while True:
            x = random.randint(0, 1920)  
            y = random.randint(0, 1080)  
            
            
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'screenX': {x},
                    'screenY': {y}
                }});
                document.dispatchEvent(event);
            """)
            
            print("moved mouse")
            time.sleep(random.uniform(2, 5))  
    except Exception as e:
        print(f"Error simulating mouse movement: {e}")
    

async def send_message(message):
    try:
        print(f"Sending message: {message}")
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=192398851, text=message)
        print(f"Message sent to Telegram: {message}")
        time.sleep(10)
    except Exception as e:
        print(f"Error sending message: {e}")

def set_window_full_height():
    print("Setting window size to full screen height but not full width...")
    monitor = get_monitors()[0] 
    screen_height = monitor.height
    screen_width = monitor.width
    driver.set_window_rect(width=screen_width // 2, height=screen_height, x=0, y=0) 

def zoom_out_page():
    print("Zooming out the page...")
    driver.execute_script("document.body.style.zoom='10%'")

def check_for_typing():
    """
    Function to continuously check for typing status.
    Once typing is detected, it calls the send_message function.
    """
    try:
        print("Checking for typing status...")

        typing_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'typing…')]"))
        )

        chat_container = typing_element.find_element(By.XPATH, "..//ancestor::div[contains(@class, '_ak8l')]")


        contact_name_element = chat_container.find_element(By.XPATH, ".//span[@title and @dir='auto']")
        contact_name = contact_name_element.get_attribute("title")
        print(f"{contact_name} is typing...")


       
        asyncio.run(send_message(f"{contact_name} is typing..."))


        return True

    except Exception as e:

        
        return False

def monitor_typing():
    """
    Function that keeps checking for typing status.
    It will break when typing is detected, send a message, and then resume checking.
    """
    print("Starting to monitor for typing status...")
    direction = "down"  
    try:
        while True:
            
            # if direction == "down":
            #     driver.execute_script("window.scrollBy(0, 1000);")
            #     at_bottom = driver.execute_script(
            #         "return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;"
            #     )
            #     if at_bottom:
            #         direction = "up"
            # else:
            #     driver.execute_script("window.scrollBy(0, -1000);")
            #     at_top = driver.execute_script("return window.scrollY === 0;")
            #     if at_top:
            #         direction = "down"


            typing_detected = check_for_typing()
            if typing_detected:
        
                time.sleep(1) 
                continue  

            time.sleep(10)  
    except KeyboardInterrupt:
        print("Stopped monitoring.")
    finally:
        driver.quit()


def main():
    print("Starting the script...")
    open_whatsapp()
    set_window_full_height() 
    zoom_out_page()
     # Start random mouse movement in a separate thread
    threading.Thread(target=random_mouse_movement, daemon=True).start()
    
    # Keep the window active with harmless key presses
    threading.Thread(target=keep_window_active, daemon=True).start()
    # threading.Thread(target=keep_window_active, daemon=True).start()
    monitor_typing()

if __name__ == "__main__":
    main()