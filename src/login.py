#.env loading
from os import getenv
from time import sleep
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from captcha import solveCaptcha

def login(driver):
    
    #Load the login page
    print("Loading WDCVIP.top...", end='', flush=True)

    try:
        driver.get('https://wdcvip.top/index.html/pc.html#/login')
    except:
        print("Error\nCould not load the page. Retrying...")
        return False
    
    print("Done")
    #Load the environment variables

    WDCUsername=getenv("WDCUsername")
    WDCPassword=getenv("WDCPassword")

    if WDCUsername == None or WDCPassword == None:
        print("Could not get the username and password.")
        print("Please provide the values in docker (compose) config/Arguments!")
        driver.quit()
        exit()

    #Wait for the elements to load
    print("Waiting for the whole webpage to load...", end='', flush=True)
    HTMLUsername = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][name="userName"]')))
    print("Done")

    print("Logging in...")
    print("===== Credentials =====")
    print(f"Username: {WDCUsername}")
    #Obfuscate the password
    print(f"Password: {WDCPassword[:3] + '*' * (len(WDCPassword) - 3)}")

    #Paste the username
    HTMLUsername.send_keys(WDCUsername)

    #Paste the password
    HTMLPassword = driver.find_element(By.CSS_SELECTOR, 'input[type="password"][name="password"]')
    HTMLPassword.send_keys(WDCPassword)

    #Solve the captcha
    #We will try to solve the using tessaract OCR. This has a success rate of about 85%.
    #If it fails, we will retry the captcha 4 times.
    HTMLCaptchaImage = driver.find_element(By.CSS_SELECTOR, 'img.vcode-img')
    PNGCaptchaImage = HTMLCaptchaImage.screenshot_as_png
    
    captcha = solveCaptcha(PNGCaptchaImage)
    
    i = 1

    while len(captcha) != 4:
        if i == 5:
            print("Could not solve the captcha after 5 times. Resetting login!")
            return False
        print("Did not recognize captcha. Retrying...")
        #Request a new captcha by clicking the image
        HTMLCaptchaImage.click()
        #Wait for the new image to load
        sleep(3)
        PNGCaptchaImage = HTMLCaptchaImage.screenshot_as_png
        #Get the new captcha
        captcha = solveCaptcha(PNGCaptchaImage)
        i += 1


    #Paste the captcha
    HTMLCaptcha = driver.find_element(By.CSS_SELECTOR, 'input[type="text"][name="vcode"]')
    HTMLCaptcha.send_keys(captcha)

    #Wait 3 Seconds. Otherwise we might be too fast ¯\_(ツ)_/¯
    sleep(3)
    print("Sending login...", end='', flush=True)

    #Click the login button
    HTMLCaptcha.submit()

    #Wait another 3 and check if login was successful
    sleep(3)
    print("Done")

    #Check if we got redirected. If not, we failed to login
    if re.search(r'login', driver.current_url):
        #Maybe there is hope if we manually navigate to the quantify page
        driver.get('https://wdcvip.top/index.html/pc.html#/basic')
        sleep(3)
        if re.search(r'login', driver.current_url):
            print("Login failed. Retrying...")
            #Refresh the page to clear the login form
            driver.refresh()
            print(f"Current URL: {driver.current_url}")
            return False

    print("Logged in successfully!")
    return True