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



# wingsms.inputstringname(name)
# wingsms.clickbutton()
# span  = wingsms.readspan()
# if(span)
#   if(有时间)  
#       wingsms.outputfile(投票成功)
#   else
#       wingsms.outputfile(投票失败)
# wingsms.outputfile(text,name,date,errormsg)
# else
# wingsms.readnewwindow()
# wingsms.doticket()
#if  wingsms.span() == thank you for your vote
#   wingsms.outputfile(投票成功)
# else
#   wingsms.outputfile(投票失败)

username  = "nnnnn"
date_str = datetime.now().strftime("%Y-%m-%d")


# 初始化文件，如果文件不存在，则创建文件
if not os.path.exists(f"./ticketspidernew_{date_str}.txt"):
    with open(f"./ticketspidernew_{date_str}.txt", "w") as f:
        f.write("") 
        
        

def setup_driver():
    try:
        chromedriver_path = r'/Users/xingzuozhou/Geek/chromedriver/chromedriver-mac-arm64/chromedriver'
        service = Service(chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        # options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        # 加载yescaptcha人机助手
        options.add_extension(r'/Users/xingzuozhou/Geek/投票爬虫/google_pro_1.1.64.zip')
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver 初始化成功")
        return driver
    except Exception as e:
        logging.error(f"WebDriver 初始化失败: {e}")
        return None
    
    

driver = setup_driver()



driver.get("https://wingstory.net/")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


vote_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '投票')]"))
)
vote_button.click()



pingUser = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "pingUser"))
)
pingUser.click()
pingUser.send_keys(username)


# 投票网站.点击投票按钮
supp_button = WebDriverWait(driver, 10).until(
    
    EC.presence_of_element_located((By.CLASS_NAME, "supp_button"))
)
supp_button.click()






time.sleep(2)  

# 投票网站.检查是否存在错误提示
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

# 等待页面加载（可选）
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
print("投票页面加载完成")


time.sleep(1)

vote_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "votebutton"))
)
time.sleep(3)
vote_button.click()
print("投票按钮已点击")



time.sleep(30)


captcha_status = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "captcha-status"))
)
print("captcha-status加载完成")
if captcha_status:
    p_element = captcha_status.find_elements_by_tag_name("p")[1]
    print(p_element.text)
    # 如果p_element.text 包含 thank或者thanks（不区分大小写）
    if "thank" in p_element.text.lower() or "thanks" in p_element.text.lower():
        print("自动投票成功")
        with open(f"./ticketspidernew_{date_str}.txt", "a", encoding="utf-8") as f:
            f.write(f"{username} -> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> 自动投票成功\n")
        time.sleep(20)
        driver.quit()
        exit()
    else:
        print("自动投票失败")
        with open(f"./ticketspidernew_{date_str}.txt", "a", encoding="utf-8") as f:
            f.write(f"{username} -> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> 自动投票失败\n")
        time.sleep(20)
        driver.quit()
        exit()

else:
    print("异常 ...  没有识别到投票结果span")



# iframe = WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.XPATH, "//iframe[@title='Verification challenge']"))
# )
# driver.switch_to.frame(iframe)

# print(driver.page_source)

#     # 等待并切换到内层iframe
# inner_iframe = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "game-core-frame"))
#     )
# driver.switch_to.frame(inner_iframe)

# print(driver.page_source)


time.sleep(3)

time.sleep(100000)

