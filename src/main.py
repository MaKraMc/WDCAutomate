from loadFirefox import loadFirefox
from login import login
from quantify import quantify
from init import init

def main():
    init()
    #Print info without new line
    print("Loading Firefox...", end='', flush=True)
    driver = loadFirefox()
    print("Done")
    
    #Try three times to login
    logins = 1
    isLoggedin = login(driver)
    while not isLoggedin:
        isLoggedin = login(driver)
        logins += 1
        if logins == 3:
            driver.quit()
            exit("Could not login after 3 tries. Exiting...")
    
    #Do the quantification
    quantify(driver)


if __name__ == "__main__":
    main()