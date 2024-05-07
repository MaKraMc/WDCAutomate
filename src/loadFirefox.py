#selenium loading
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


#Load the browser
def loadFirefox():
    options = Options()
    options.add_argument("--headless")
    
    return webdriver.Firefox(service=Service("/app/geckodriver"), options=options)

if __name__ == "__main__":
    driver = loadFirefox()
    driver.get("https://example.com")
    print(driver.title)
    driver.quit()