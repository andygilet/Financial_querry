from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from webdriver_manager.firefox import GeckoDriverManager
from stock_database.Stocks import Ticker, verify_ticker
import time
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

def access_marketstacks(url : str, driver : webdriver.Firefox):
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        
def get_datas_from_page(driver : webdriver.Firefox) -> list:
    try:
        list_symbols = driver.find_elements(By.CLASS_NAME, "ticker_id")
        list_names = driver.find_elements(By.CLASS_NAME, "ticker_name")
        list_stock_exchanges = driver.find_elements(By.CLASS_NAME, "ticker_exchange")
        list_stock_exchange_symbols = driver.find_elements(By.CLASS_NAME, "ticker_exchange_id")
        list_countries = driver.find_elements(By.CLASS_NAME, "ticker_country")
        for i in range(len(list_symbols)):
            list_symbols[i] = list_symbols[i].text
            list_names[i] = list_names[i].text
            list_stock_exchanges[i] = list_stock_exchanges[i].text
            list_stock_exchange_symbols[i] = list_stock_exchange_symbols[i].text
            list_countries[i] = list_countries[i].text
        return [list_symbols, list_names, list_stock_exchanges, list_stock_exchange_symbols, list_countries]
    except Exception as e:
        print(e)
        return []
    
def find_next_button(driver : webdriver.Firefox) -> bool:
    try:
        driver.find_element(By.XPATH, "/html/body/div/section[2]/div/div[2]/a[2]")
        return True
    except:
        return False
    
def push_next_page_button(driver : webdriver.Firefox):
    driver.find_element(By.XPATH, "/html/body/div/section[2]/div/div[2]/a[2]").click()
    
def send_data_to_database(data : list) -> int:
    nbr_entries = 0
    engine = create_engine("sqlite:///stock_database/db.db")
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    for i in range(len(data[0])):
        if(verify_ticker(data[0][i], session)):
            print(f"{data[0][i]}, {data[1][i]}, {data[2][i]}, {data[3][i]}, {data[4][i]}")
            nbr_entries += 1
            #update value in database
        else:
            print(f"{data[0][i]}, {data[1][i]}, {data[2][i]}, {data[3][i]}, {data[4][i]}")
            nbr_entries += 1
            #add value in database
    session.close()
    return nbr_entries

def scrap_symbols():
    nbr_entries = 0
    url = "https://marketstack.com/search"
    executable_path = GeckoDriverManager().install()
    driver = webdriver.Firefox(executable_path=executable_path)
    driver.implicitly_wait(1)
    access_marketstacks(url, driver)
    data = get_datas_from_page(driver)
    nbr_entries += send_data_to_database(data)
    print(nbr_entries)
    while(find_next_button(driver)):
        push_next_page_button(driver)
        data = get_datas_from_page(driver)
        nbr_entries += send_data_to_database(data)
        print(nbr_entries)
    
scrap_symbols()