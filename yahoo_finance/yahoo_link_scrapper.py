from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from webdriver_manager.firefox import GeckoDriverManager
import time

def go_next_page(driver : webdriver.Firefox):
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[2]/button[3]').click()
    except:
        print("go_next_page : Last page found !")

def try_find_next_button(driver : webdriver.Firefox) -> bool:
    try:
        test = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[2]/button[3]')
        if test != None:
            return True
        else:
            return False
    except:
        return False
def try_cookie(driver : webdriver.Firefox):
    try:
        coockie_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div[2]/div[2]/button[1]')
        coockie_button.click()
    except:
        pass
    
def change_filter(driver : webdriver.Firefox):
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/header/button').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/button').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/button').click()
        time.sleep(2)
        inputVolume = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/input")
        inputVolume.clear()
        inputVolume.send_keys('0')
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[3]/button[1]").click()
    except:
        print("Change filter : Unable to change the filter !")
        
def get_urls(driver : webdriver.Firefox) -> list:
    urls = []
    try:
        for i in range(25):
            article = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[1]/table/tbody/tr[{i + 1}]/td[1]/a")
            url = article.get_attribute("href")
            if url not in urls:
                urls.append(url)
    except:
        print("get_urls : Unable to get urls !")
    return urls
    
def yahoo_link_scrapper():
    enterprise_link = []
    driver = webdriver.Firefox(executable_path= GeckoDriverManager().install())
    driver.implicitly_wait(0.5)
    driver.get(f"https://finance.yahoo.com/screener/predefined/most_actives?offset=0&count=100")
    try_cookie(driver)
    change_filter(driver)
    enterprise_link += get_urls(driver)
    while try_find_next_button(driver):
        go_next_page(driver)
        enterprise_link += get_urls(driver)
    
yahoo_link_scrapper()