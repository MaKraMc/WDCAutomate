from loadFirefox import loadFirefox
from login import login
from quantify import quantify
from init import init

def main():
    platform = init()
    #Print info without new line
    print("Loading Firefox...", end='', flush=True)
    driver = loadFirefox()
    print("Done")
    
    #Try three times to login
    logins = 0
    isLoggedin = False
    while not isLoggedin:
        isLoggedin = login(driver, platform)
        logins += 1
        if logins == 3:
            driver.quit()
            exit("Could not login after 3 tries. Exiting...")
    
    #Do the quantification
    quantify(driver, platform)


if __name__ == "__main__":
    main()