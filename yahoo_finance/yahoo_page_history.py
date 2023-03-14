from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time

def try_cookie(driver : webdriver.Firefox):
    try:
        coockie_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div[2]/div[2]/button[1]')
        coockie_button.click()
    except:
        pass

def try_pass_member(driver : webdriver.Firefox):
    try:
        pass_member_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[2]")
        pass_member_button.click()
    except:
        pass
    
def get_data_from_url(url : str, driver : webdriver.Firefox):
    try:
        driver.get(url)
        try_cookie(driver)
        time.sleep(2)
        try_pass_member(driver)
    except Exception as e:
        print(e)
        return None
    rows = driver.find_elements(By.CLASS_NAME, "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)")
    print(rows)

def get_data():
    url = "https://finance.yahoo.com/quote/TSLA/history?p=TSLA"
    driver = webdriver.Firefox(executable_path= GeckoDriverManager().install())
    driver.implicitly_wait(0.5)
    get_data_from_url(url, driver)
    
get_data()