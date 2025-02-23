from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import JavascriptException
import time
import logging
from datetime import datetime
import os
import re


username = "abcabc"

def setup_driver():
    try:
        chromedriver_path = r'/Users/xingzuozhou/Geek/chromedriver/chromedriver-mac-arm64/chromedriver'
        service = Service(chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        # 加载yescaptcha人机助手
        # options.add_extension(r'/Users/xingzuozhou/Geek/投票爬虫/google_pro_1.1.64.zip')
        options.add_argument('--load-extension=/Users/xingzuozhou/Geek/投票爬虫/google_pro_1.1.64')
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver 初始化成功")
        return driver
    except Exception as e:
        logging.error(f"WebDriver 初始化失败: {e}")
        return None
    
    

driver = setup_driver()



# 访问投票网站
driver.get("https://mschool.fun/vote.html")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 选择这个class，填入用户名，采用等待机制
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "votename"))
)
username_input.send_keys(username)   

# 点击投票按钮 btn vote-btn btn-info 采用等待机制
vote_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "vote-btn"))
)
vote_btn.click()

time.sleep(1000)












