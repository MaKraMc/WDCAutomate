#.env loading
from os import getenv
from time import sleep
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from captcha import solveCaptcha

def login(driver, platform):
    
    #Load the login page
    print(f"Loading {platform}...", end='', flush=True)

    try:
        driver.get(f'https://{platform}/index.html/pc.html#/login')
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
    print("Waiting for the login page...", end='', flush=True)

    #Wait for the loading spinner to disappear
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.van-toast.van-toast--loading[style*="display: none"]')))

    try:
        #Wait for the login form to load
        HTMLUsername = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][name="userName"]')))
        HTMLPassword = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"][name="password"]')))
        HTMLCaptchaImage = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.vcode-img')))
        
    except:
        print("Error\nCould not find the login interface.")
        driver.quit()
        exit("Maybe you used the wrong platform URL? Exiting...")
    
    print("Done")

    print("Logging in...")
    print("===== Credentials =====")
    print(f"Username: {WDCUsername}")
    #Obfuscate the password
    print(f"Password: {WDCPassword[:3] + '*' * (len(WDCPassword) - 3)}")

    #Paste the username
    HTMLUsername.send_keys(WDCUsername)

    #Paste the password
    HTMLPassword.send_keys(WDCPassword)

    #Solve the captcha
    #We will try to solve the using tessaract OCR. This has a success rate of about 85%.
    #If it fails, we will retry the captcha 4 times.
    PNGCaptchaImage = HTMLCaptchaImage.screenshot_as_png
    
    captcha = solveCaptcha(PNGCaptchaImage)
    
    i = 1

    while len(captcha) != 4:
        if i == 5:
            print("Could not solve the captcha after 5 times. Resetting login!")
            return False
        print("Did not recognize captcha. Retrying...")
        #Request a new captcha by clicking the image
        try:
            HTMLCaptchaImage.click()
        except:
            print("Could not request a new captcha. This can happen if there is a dialog blocking the captcha.\nRetrying...")
            return False
        #Wait for the new image to load
        sleep(3)
        PNGCaptchaImage = HTMLCaptchaImage.screenshot_as_png
        #Get the new captcha
        captcha = solveCaptcha(PNGCaptchaImage)
        i += 1

    print(f"Got captcha: {captcha}")

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
        #In some weird cases, login seems to fail while still generating a valid session
        #We have to go to the login page and then to the personal page
        print("Checking login")
        driver.get(f'https://{platform}/index.html')
        sleep(3)
        driver.get(f'https://{platform}/index.html/pc.html#/basic')
        sleep(3)
        if re.search(r'login', driver.current_url):
            print("Login failed. Retrying...")
            #Refresh the page to clear the login form
            driver.refresh()
            print(f"Current URL: {driver.current_url}")
            return False

    print("Logged in successfully!")
    return True