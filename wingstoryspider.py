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


username  = "huaan"
date_str = datetime.now().strftime("%Y-%m-%d")

# 初始化文件，如果文件不存在，则创建文件
if not os.path.exists(f"./ticketspidernew_{date_str}.txt"):
    with open(f"./ticketspidernew_{date_str}.txt", "w") as f:
        f.write("") 
        
        

def setup_driver():
    try:

        # chromedriver_path = r'/Users/xingzuozhou/Geek/chromedriver/chromedriver-mac-arm64/chromedriver'
        chromedriver_path = r'D:\Happy Hacking\chromedriver\chromedriver-win64\chromedriver.exe'
        service = Service(chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--load-extension=/Users/xingzuozhou/Geek/投票爬虫/google_pro_1.1.64')
        options.add_argument('--load-extension=D:\Happy Hacking\yescaptchadriver')
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver 初始化成功")
        return driver
    except Exception as e:
        logging.error(f"WebDriver 初始化失败: {e}")
        return None
driver = setup_driver()

# 访问投票网站
driver.get("https://wingstory.net/")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 点击投票标签
vote_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '投票')]"))
)
vote_button.click()

# 输入用户名，点击投票按钮
pingUser = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "pingUser"))
)
pingUser.click()
pingUser.send_keys(username)

supp_button = WebDriverWait(driver, 10).until(
    
    EC.presence_of_element_located((By.CLASS_NAME, "supp_button"))
)
supp_button.click()



time.sleep(2)  

# 检测是否存在提示
span_elements = driver.find_elements(By.CSS_SELECTOR, "label[for='pingUser'] span")
if span_elements and span_elements[0].is_displayed():
    # 如果包含yyyy-mm-dd格式，则说明投票成功
    if re.search(r'\d{4}-\d{2}-\d{2}', span_elements[0].text):
        print("投票成功 ->  ->  ->", span_elements[0].text)
        with open(f"./ticketspidernew_{date_str}.txt", "a", encoding="utf-8") as f:
            f.write(f"{username} -> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> 投票成功 , {span_elements[0].text}\n")
        time.sleep(20)
        driver.quit()
        exit()
    else:
        print("暂时无法投票 ->  ->  ->", span_elements[0].text)
        with open(f"./ticketspidernew_{date_str}.txt", "a", encoding="utf-8") as f:
            f.write(f"{username} -> {span_elements[0].text} -> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    time.sleep(20)
    driver.quit()
    exit()

# 如果没有错误提示，说明投票成功，继续处理验证码
print("准备处理验证码...")
driver.switch_to.window(driver.window_handles[-1])


vote_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "votebutton"))
)
time.sleep(3)
vote_button.click()
print("投票按钮已点击")

time.sleep(2)
# 验证投票结果
flag = 0
while flag == 0:
        captcha_status = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "captcha-status"))
        )
        print("captcha-status 已加载")
        print("captcha-status 内容:", captcha_status.get_attribute("innerHTML"))
        
        try:
            # 只检测p标签
            # p_element = captcha_status.find_element(By.TAG_NAME, "p")
        #     p_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "#captcha-status p"))
        # )
            p_text=captcha_status.find_element(By.XPATH, ".//p[@align='center']")
            if p_text:
                status_message = p_text.text
                print(f"验证结果: {status_message}")
                # 精确匹配 "Thank you for voting!" 文本
                if "Thank you for voting!" in status_message:
                    print("自动投票成功")
                    with open(f"./ticketspidernew_{date_str}.txt", "a", encoding="utf-8") as f:
                        f.write(f"{username} -> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> 自动投票成功\n")
                else:
                    print("自动投票失败")
                    with open(f"./ticketspidernew_{date_str}.txt", "a", encoding="utf-8") as f:
                        f.write(f"{username} -> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> 自动投票失败: {status_message}\n")
                flag = 1  # 有结果后退出循环
            else:
                print("未检测到p标签，继续等待...")
                time.sleep(0.5)
        except:
            print("未检测到p标签，继续等待...")
            time.sleep(0.5)
            
# 完成后退出
time.sleep(10)
driver.quit()

