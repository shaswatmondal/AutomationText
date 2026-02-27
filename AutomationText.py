import os
import re
import time
import logging
from datetime import datetime, timedelta
from collections import deque
from dotenv import load_dotenv
import pywhatkit
import pyautogui 

load_dotenv()


class Config:
    WAIT_TIME = int(os.getenv("WAIT_TIME", 50))
    TAB_CLOSE = True
    TIMEOUT = int(os.getenv("TIMEOUT", 51))

    MIN_DELAY_BETWEEN_MSG = int(os.getenv("MIN_DELAY_BETWEEN_MSG", 10))
    HOURLY_LIMIT = int(os.getenv("HOURLY_LIMIT", 20))
    DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", 100))

    LOG_FILE = os.getenv("LOG_FILE", "whatsapp_sender.log")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)


class RateLimiter:
    def __init__(self):
        self.last_sent_time = None
        self.hourly_messages = deque()
        self.daily_messages = deque()

    def check_limits(self):
        now = datetime.now()

        while self.hourly_messages and self.hourly_messages[0] < now - timedelta(hours=1):
            self.hourly_messages.popleft()

        while self.daily_messages and self.daily_messages[0] < now - timedelta(days=1):
            self.daily_messages.popleft()

        if len(self.hourly_messages) >= Config.HOURLY_LIMIT:
            raise Exception("Hourly message limit reached.")

        if len(self.daily_messages) >= Config.DAILY_LIMIT:
            raise Exception("Daily message limit reached.")

        if self.last_sent_time:
            elapsed = (now - self.last_sent_time).total_seconds()
            if elapsed < Config.MIN_DELAY_BETWEEN_MSG:
                delay = Config.MIN_DELAY_BETWEEN_MSG - elapsed
                logging.info(f"Rate limiting: Waiting {delay:.1f} seconds...")
                time.sleep(delay)

    def record_send(self):
        now = datetime.now()
        self.last_sent_time = now
        self.hourly_messages.append(now)
        self.daily_messages.append(now)


class WhatsAppSender:
    PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

    def __init__(self):
        self.rate_limiter = RateLimiter()

    def validate_input(self, message, phone):
        if not self.PHONE_REGEX.match(phone):
            raise ValueError("Invalid phone number format. Use +<countrycode><number>")

        if not (1 <= len(message) <= 4096):
            raise ValueError("Message must be between 1 and 4096 characters.")

    def send_text(self, message, phone):
        try:
            self.validate_input(message, phone)
            self.rate_limiter.check_limits()

            logging.info(f"Opening WhatsApp chat for {phone}")

            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=Config.WAIT_TIME,
                tab_close=Config.TAB_CLOSE
            )

            time.sleep(10)

            pyautogui.click()
            time.sleep(1)
            pyautogui.press("enter")

            self.rate_limiter.record_send()

            logging.info(f"Message send attempt completed for {phone}")
            print("Message send successfully.")

        except ValueError as ve:
            logging.warning(f"Validation error: {ve}")
            print(f"Input Error: {ve}")

        except Exception:
            logging.exception("Unexpected error occurred")
            print("Failed to send message. Check logs.")


if __name__ == "__main__":
    prompt = input("Enter Text prompt: ")
    phone = input("Enter phone number (+91xxxxxxxxxx): ")

    sender = WhatsAppSender()
    sender.send_text(prompt, phone)