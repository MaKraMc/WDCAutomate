from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

import re

def quantify(driver, platform):
    print("Loading the quantify page...", end='', flush=True)
    j = 0
    #Navigate to the "quantify" page. Sometimes we need to try multiple times
    while not driver.current_url == f'https://{platform}/index.html/pc.html#/basic':
        driver.get(f'https://{platform}/index.html/pc.html#/basic')
        sleep(1)
        j += 1
        if j == 5:
            driver.quit()
            exit("Could not load the quantify page after 5 times. Exiting...")

    #Sometimes we need to wait a bit
    sleep(1)

    #Find the "quantify" button
    quantify_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.buy-btn.van-button')))
    print("Done")

    #Check if we can quantify again
    if not quantify_button.is_enabled():
        #Check if limit is exhausted
        if re.search(r'Exhausted', quantify_button.get_attribute("innerHTML")):
            print("Cannot quantify. Limit reached.")
            print("Check your time variables. Maybe it is not time to quantify yet.")
            print("Closing Firefox...")
            driver.quit()
            exit("Cannot quantify. Limit reached.")

    #Start quantifying
    #We check if the button is enabled every 30 seconds for 20 minutes
    #If the button is enabled, we click it and wait 30 seconds
    #If the button is not enabled, we wait 30 seconds, since we are probaply currently quantifying

    #Get the current available quantitive frequency
    try:
        max_quantify = driver.find_element(By.CSS_SELECTOR, 'div.vip-card>div.grid-wrap>span:nth-child(4)').get_attribute("innerHTML")
        max_quantify = int(re.search(r'\d+', max_quantify).group(0))
        print(f"Available quantify amount: {max_quantify}")
    except:
        max_quantify = 5

    quantifys = 0
    i = 0
    while i < 40:
        if quantify_button.is_enabled():
            quantifys += 1
            print(f"[{quantifys}/{max_quantify}] Quantifying...")
            #We use Javascript to click the button, since the button may be obscured by a dialog
            driver.execute_script("arguments[0].click();", quantify_button)
            #quantify_button.click()
        else:
            if re.search(r'Exhausted', quantify_button.get_attribute("innerHTML")):
                driver.quit()
                print("Limit reached. See you again tomorrow!")
                exit(0)
        sleep(30)
        i += 1
