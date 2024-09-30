from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.chrome.options import Options as ChromeOptions

class WebDriverManager:
    @staticmethod
    def create_driver(headless: bool = False):
        if headless == True:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(service=Service(ChromeService(chrome_options=chrome_options)))
            return driver
        driver = webdriver.Chrome()
        return driver
