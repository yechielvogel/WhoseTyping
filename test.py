import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from screeninfo import get_monitors
import telegram

# Set up the WebDriver for Safari
driver = webdriver.Safari()
BOT_TOKEN = '7827627496:AAHx2vU2Top43OsizxQmy2ADT5nC2doaKgI'

def open_whatsapp():
    print("Opening WhatsApp Web on Safari...")
    driver.get("https://web.whatsapp.com")
    input("Please scan the QR code on WhatsApp Web and press Enter once logged in.")
    print("QR code scanned. Logged in.")

async def send_message(message):
    try:
        print(f"Sending message: {message}")
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=192398851, text=message)
        print(f"Message sent to Telegram: {message}")
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
            
            if direction == "down":
                driver.execute_script("window.scrollBy(0, 1000);")
                at_bottom = driver.execute_script(
                    "return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;"
                )
                if at_bottom:
                    direction = "up"
            else:
                driver.execute_script("window.scrollBy(0, -1000);")
                at_top = driver.execute_script("return window.scrollY === 0;")
                if at_top:
                    direction = "down"


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
    monitor_typing()

if __name__ == "__main__":
    main()



