import numpy as np
import gspread 
import pandas as pd
from google.oauth2.service_account import Credentials
import os
import selenium
from selenium import webdriver
import time
import io
import requests
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from gspread_dataframe import set_with_dataframe
from selenium.webdriver.firefox.options import Options


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file(
    'C:/Users/wrath/gsheets_testing/keys.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/12nZmdZar3ThXa9OwJNHhvw2wpv_8UvviX2mV-DG4raI/edit#gid=0')
df = pd.DataFrame(sh.sheet1.get_all_records())

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\wrath\Downloads\Compressed\geckodriver-v0.29.1-win64\geckodriver.exe')
print ("Headless Firefox Initialized")

records = len(df)
url_col = 5
tel_col = 6
check = 0
r = 0
url_list = {}
tel_list = {}
tel = None
while r < records:
    url_list[r] = df.iloc[r][url_col]
    tel_list[r] = df.iloc[r][tel_col]
    driver.get(url_list[r])
    try:
        contact = driver.find_element_by_css_selector("[data-tooltip = 'Copy phone number']")
        print(contact.text)
        tel = contact.text
    except:
        print("Couldn't extract")

    if tel != None:
        tel = ''.join(e for e in tel if e.isalnum())

    if df.iloc[r][tel_col]==tel:
        df.iloc[r][check]= True
        print('correct')
    else:
        df.iloc[r][check]= False
        print('incorrect')
    r = r+1

set_with_dataframe(sh.sheet1, df)