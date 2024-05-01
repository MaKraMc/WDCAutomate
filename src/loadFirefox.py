#selenium loading
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from webdriver_manager.firefox import GeckoDriverManager


#Load the browser
def loadFirefox():
    options = Options()
    options.add_argument("--headless")
    
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()),
    options=options)
