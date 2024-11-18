from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# WhatsApp Web URL
link = "https://web.whatsapp.com"

print("Opening Safari and navigating to WhatsApp Web...")

# Initialize the Safari WebDriver without using the Service class
driver = webdriver.Safari()  # Make sure "Allow Remote Automation" is enabled in Safari
time.sleep(2)
driver.implicitly_wait(5)  # Set an implicit wait
driver.get(link)

# Wait for manual login
input("Press Enter after logging into WhatsApp Web and chats are visible...")

print("Monitoring for typing activity...")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

# Initialize the driver
driver = webdriver.Safari()  # Make sure "Allow Remote Automation" is enabled in Safari
driver.get("https://web.whatsapp.com")
print("Please scan the QR code to log in.")

# Wait for user to log in
time.sleep(15)

try:
    print("Starting WhatsApp chat monitor...")

    while True:
        try:
            # Locate all chats in the chat list
            chats = driver.find_elements(By.CSS_SELECTOR, "span[title]")
            print(f"Found {len(chats)} chat(s).")

            for chat in chats:
                try:
                    # Check if the chat has a "typing" or "recording audio" indicator
                    typing_indicator = chat.find_element(By.XPATH, ".//following-sibling::span[contains(text(), 'typing') or contains(text(), 'recording audio')]")
                    print(f"{chat.text} is currently typing or recording audio...")

                except NoSuchElementException:
                    # If no typing indicator is found, move to the next chat
                    continue
                except StaleElementReferenceException:
                    # If the element goes stale, retry in the next loop
                    print(f"Encountered a stale element for chat: {chat.text}")
                    continue

            # Wait for a short delay before checking again
            print("Waiting for next check...")
            time.sleep(5)

        except StaleElementReferenceException:
            print("Stale element encountered in the main loop. Retrying...")

except KeyboardInterrupt:
    print("Stopped monitoring.")
finally:
    print("Closing the browser.")
    driver.quit()




# Done! Congratulations on your new bot. You will find it at t.me/WhoseTypingBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

# Use this token to access the HTTP API:
# 7827627496:AAHx2vU2Top43OsizxQmy2ADT5nC2doaKgI
# Keep your token secure and store it safely, it can be used by anyone to control your bot.

# For a description of the Bot API, see this page: https://core.telegram.org/bots/api