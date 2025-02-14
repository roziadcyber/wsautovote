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


# wingsms.inputstringname(name)
# wingsms.clickbutton()
# span  = wingsms.readspan()
# if(span)
# wingsms.outputfile(text,name,date,errormsg)
# else
# wingsms.readnewwindow()
# wingsms.
# 
# 
# 
# 
# 
# 
# 
# 
# 



username  = "huaan"
date_str = datetime.now().strftime("%Y-%m-%d")


# 初始化文件，如果文件不存在，则创建文件
if not os.path.exists(f"./ticketspidernew_{date_str}.txt"):
    with open(f"./ticketspidernew_{date_str}.txt", "w") as f:
        f.write("") 
        
        
        

def setup_driver():
    try:
        chromedriver_path = 'C:\\爬虫\\chromedriver\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
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
        options.add_extension('c:\\爬虫\\captchapro\\option.zip')
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver 初始化成功")
        return driver
    except Exception as e:
        logging.error(f"WebDriver 初始化失败: {e}")
        return None
    
    
# def switch_to_window_by_url(driver, url_contains, timeout=10):
    """
    切换到 URL 包含指定字符串的窗口。

    Args:
        driver: WebDriver 实例。
        url_contains: URL 中应包含的字符串。
        timeout: 等待超时时间（秒）。

    Returns:
        如果找到并切换到目标窗口，返回 True；否则返回 False。
    """
    original_window = driver.current_window_handle
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: any(url_contains in d.window_handles[i] or  #注意这里
                          url_contains in d.switch_to.window(d.window_handles[i]).current_url
                          for i in range(len(d.window_handles)))
        )

        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                if url_contains in driver.current_url:
                    return True  # 找到并切换成功

        return False #没有找到

    except:  # 可以更具体地捕获 TimeoutException
        return False
    finally:
        driver.switch_to.window(original_window)  # 确保切换回原始窗口
    
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


# 点击投票按钮
supp_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "supp_button"))
)
supp_button.click()






time.sleep(2)  

# 检查是否存在错误提示
span_elements = driver.find_elements(By.CSS_SELECTOR, "label[for='pingUser'] span")
if span_elements and span_elements[0].is_displayed():
    # 存在span元素，说明投票失败
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
iframe = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//iframe[@title='Verification challenge']"))
)
driver.switch_to.frame(iframe)

print(driver.page_source)

    # 等待并切换到内层iframe
inner_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "game-core-frame"))
    )
driver.switch_to.frame(inner_iframe)

print(driver.page_source)


#     # 在iframe中查找并点击"开始答题"按钮
# start_quiz_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//button[@data-theme='home.verifyButton'][contains(text(), '开始答题')]"))
#     )
# start_quiz_button.click()
# print("已点击'开始答题'按钮")







time.sleep(3)

time.sleep(100000)



    
# # 访问指定的URL
# url = "https://gtop100.com/MapleStory/MapleSchool-101860"
# driver = setup_driver()
# driver.get(url)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# # 等待页面加载（可选）
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# # 打印页面标题以确认页面加载成功
# print(driver.title)

# try:
    
#     wait = WebDriverWait(driver, 10)
#     wait.until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
#     print("投票页面加载完成")
    
    
#     time.sleep(1)
    
#     vote_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.ID, "votebutton"))
#     )
#     time.sleep(3)
#     vote_button.click()

#     print("投票按钮已点击")
    
#     time.sleep(1000)
# except Exception as e:
#     print(e)
#     driver.quit()
    
