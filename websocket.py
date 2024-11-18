import time
from selenium import webdriver
from mitmproxy import http
from mitmproxy import ctx
from mitmproxy.tools.main import mitmdump
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global list to hold WebSocket URLs
websocket_urls = []

def websocket_listener():
    # Start Mitmproxy in reverse mode for capturing traffic
    # Make sure mitmdump is running separately or use mitmproxy as a proxy
    mitmproxy_command = [
        "mitmdump", "--mode", "reverse:https://web.whatsapp.com", 
        "--listen-port", "8080", "--ssl-insecure"
    ]
    
    # Start Mitmproxy in a separate thread
    from subprocess import Popen
    mitmproxy_process = Popen(mitmproxy_command)

    # Set up Selenium to use Mitmproxy as a proxy
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=http://127.0.0.1:8080')
    options.add_argument('--incognito')  # Optionally start in incognito mode
    driver = webdriver.Chrome(options=options)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")

    # Wait for the QR code to be visible (indicates that WhatsApp Web is ready)
    print("Waiting for QR code to load...")
    try:
        WebDriverWait(driver, 600).until(  # Wait up to 10 minutes for the QR code
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-ref]"))
        )
        print("QR code is visible. Please scan the QR code on your phone.")
        input("Press Enter after scanning the QR code...")
    except Exception as e:
        print(f"Error while waiting for QR code: {e}")
        driver.quit()
        return

    print("QR code scanned successfully. Listening for WebSocket traffic...")

    try:
        # Mitmproxy listens for WebSocket requests and logs them
        while True:
            if websocket_urls:
                for url in websocket_urls:
                    print(f"WebSocket detected: {url}")
                websocket_urls.clear()
            time.sleep(1)  # Sleep to reduce CPU usage in the loop
    except KeyboardInterrupt:
        print("Stopping listener...")
    finally:
        driver.quit()
        mitmproxy_process.terminate()  # Stop Mitmproxy process

# Mitmproxy event handler to capture WebSocket requests
class WebSocketHandler:
    def websocket_message(self, flow):
        if "wss://" in flow.request.pretty_url:
            websocket_urls.append(flow.request.pretty_url)

    def request(self, flow: http.HTTPFlow):
        # Intercept WebSocket request traffic
        if "wss://" in flow.request.pretty_url:
            websocket_urls.append(flow.request.pretty_url)

    def response(self, flow: http.HTTPFlow):
        # Handle responses (if necessary)
        pass

# Register the WebSocketHandler with Mitmproxy
def start_mitmproxy():
    addon = WebSocketHandler()
    mitmproxy_command = [
        "mitmdump", "--mode", "reverse:https://web.whatsapp.com", 
        "--listen-port", "8080", "--ssl-insecure", "--set", "content_view=plain"
    ]
    mitmdump.main(mitmproxy_command)  # Start Mitmproxy to capture traffic

if __name__ == "__main__":
    websocket_listener()

