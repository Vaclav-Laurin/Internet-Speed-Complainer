import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


CHROME_DRIVER_PATH = "C:\\Development\\chromedriver.exe"
#Must-be Internet speed:
GUARANTEED_UP = 500
GUARANTEED_DOWN = 250
PROVIDER_NAME = "TheProvider"
SPEED_TEST_URL = "https://www.speedtest.net/"
TWITTER_EMAIL = "zaz_1102@ukr.net"
TWITTER_PASSWORD = "Tavria_1987"
TWITTER_URL = "https://twitter.com/login/"
TWITTER_USER_NAME = "SpeedTester9"
WAIT_TIME = 120

#XPATHs for speedtest.net:
XPATH_SPEEDTEST = {
    "accept_button": '//*[@id="onetrust-button-group"]/div',
    "boring_notification": '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[1]/div/div/div/a',
    "launch_button": '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a',
    "link": '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[1]/div/div/div[2]/div[2]/a',
    "down": '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span',
    "up": '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span'
}

#XPATHs for twitter.com:
XPATH_TWITTER = {
    "ad_permission_button": '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[2]/div',
    "cookies_button": '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div',
    "email_input": '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input',
    "login_input": '/html/body/div[1]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div',
    "pass_input": '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
    "tag_xpath": '//*[@id="typeaheadFocus-0.45471431225789916"]/div/div/div',
    "twit_input": '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div',
    "username_input": '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
}


class InternetSpeedtweetterBot:

    def __init__(self):
        self.service = Service(CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service)
        self.wait = WebDriverWait(self.driver, WAIT_TIME)
        self.driver.maximize_window()
        self.down = 0
        self.up = 0
        self.link = ""

    #Make some measurements    
    def get_internet_speed(self):
        #Go to the web
        self.driver.get(SPEED_TEST_URL)
        
        #Acceept terms
        accept_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SPEEDTEST["accept_button"])))
        accept_button.click()
        
        #Get rid off some notifications
        boring_stuff = self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SPEEDTEST["boring_notification"])))
        boring_stuff.click()
        
        #Start measuring
        launch_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SPEEDTEST["launch_button"])))
        launch_button.click()
        
        #Grab and process data
        link = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SPEEDTEST["link"])))
        down_speed = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SPEEDTEST["down"])))
        up_speed = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_SPEEDTEST["up"])))

        self.link = link.text
        self.down = float(down_speed.text)
        self.up = float(up_speed.text)


    #Post some complains on the web in a form of a twit
    def twit_at_provider(self):
        self.driver.get(TWITTER_URL)
        
        email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_TWITTER["email_input"])))
        #Just instead of boring clicking on a button
        email_input.send_keys(TWITTER_EMAIL, Keys.ENTER)

        #Just in case Twitter will be suspicious about us...
        try:
            username_input = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_TWITTER["username_input"])))
            username_input.send_keys(TWITTER_USER_NAME, Keys.ENTER)
        except:
            print("There were way many tries...")
        
        pass_input = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_TWITTER["pass_input"])))
        pass_input.send_keys(TWITTER_PASSWORD, Keys.ENTER)
               
        try:
            add_permission_button = self.wait.until(EC.presence_of_element_located((By.XPATH, XPATH_TWITTER["add_permission_button"])))
            add_permission_button.click()
        except:
            pass
        
        try:
            cookies_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_TWITTER["cookies_button"])))
            cookies_button.click()
        except:
            pass
        
        twit_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_TWITTER["twit_input"])))    
        twit_input.send_keys(f"Why the actual internet speed is {self.down}down/{self.up}up, when {GUARANTEED_DOWN}down/{GUARANTEED_UP}up is guaranteed?\n@{PROVIDER_NAME}\nhttps://www.speedtest.net/result/{self.link}")
        twit_input.send_keys(Keys.CONTROL, Keys.ENTER)

        #Give some time to check the result
        time.sleep(20)
        
        self.driver.close()


bot = InternetSpeedtweetterBot()

bot.get_internet_speed()

if bot.down < GUARANTEED_DOWN:
    bot.twit_at_provider()
    
bot.driver.quit()