import requests
import json
import time
import os
import cv2
import tesserocr
import base64
import argparse
from PIL import Image
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def remakeImg():            #影像處理用
    img = Image.open("input.png")
    (w, h) = img.size
    print('w=%d, h=%d', w, h)

    new_img = img.resize((int(w*4), int(h*4)))
    new_img.save("input.png")

    img = cv2.imread('input.png',cv2.IMREAD_GRAYSCALE) 
    _,img_bin= cv2.threshold(img,170,255,cv2.THRESH_BINARY) 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
    img_dilate = cv2.dilate(img_bin,kernel,iterations=1) 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
    img_erode = cv2.erode(img_dilate,kernel,iterations=1) 
    cv2.imwrite("output.png",img_erode )

def imageToText():
    image = Image.open('output.png')
    result = tesserocr.image_to_text(image)
    result = result.replace(" ",'')
    result = result.replace(".",'')
    result = result.replace("-",'')
    result = result.replace("O",'0')
    result = result.replace("B",'8')
    result = result.replace("b",'6')
    return result

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://nsa.ntue.edu.tw/',
}

user_agent = UserAgent()
random_user_agent = user_agent.random

options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={random_user_agent}')
#options.add_argument('--headless') #使瀏覽器在後台運行
# options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1920,1080")
# options.add_argument('--start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-infobars')
options.add_argument('--disable-popup-blocking')

download_path = "C:\\vscode\python\.VScode\hi"  # 請指定下載路徑
prefs = {"download.default_directory":download_path}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-account",
    type=str,
    default="None",
    help='user\'s acconut'
)
parser.add_argument(
    "-password",
    type=str,
    default="None",
    help='user\'s password'
)
args = parser.parse_args()

if args.account == "None" or args.password == "None":
    print("none")
else:
    driver = webdriver.Chrome(options=options)
    driver.get("https://nsa.ntue.edu.tw/") # 更改網址以前往不同網頁
    driver.implicitly_wait(10)
    correct_password = True
    while True:
        # 點擊 account
        account = driver.find_element(By.ID, "account")
        account.send_keys(args.account)

        # 點擊 Password
        password = driver.find_element(By.ID, "password")
        password.send_keys(args.password)


        img_base64 = driver.execute_script("""
            var ele = arguments[0];
            var cnv = document.createElement('canvas');
            cnv.width = 160 ; cnv.height = 46;
            cnv.getContext('2d').drawImage(ele, 0, 0);
            return cnv.toDataURL('image/jpeg').substring(22);    
            """, driver.find_element(By.ID,"ImgCaptcha"))
        with open("input.png", 'wb') as image:
            image.write(base64.b64decode(img_base64))
        remakeImg()
        print(driver.current_url)
        # 點擊 captcha
        captcha= driver.find_element(By.XPATH,"/html/body/div[3]/div/div[3]/div[2]/form/div[3]/input")
        captcha.send_keys(imageToText())
        try:
            text = driver.find_element(By.XPATH,'//*[@id="swal2-content"]')
            if len(text.text) == 33 :
                print("密碼錯誤")
                correct_password = False
                break
        except:
            print("密碼正確")
        time.sleep(1)
        if  driver.current_url== "https://nsa.ntue.edu.tw/home":
            break
        driver.get("https://nsa.ntue.edu.tw/") 

    if correct_password == True:
        # 前往目標網址
        driver.get("https://nsa.ntue.edu.tw/b04/b04250")

        f = open("output.txt", 'w')
        f2 = open("new_json.json", 'w')

        # 更改至當學年度
        semester="下學期"
        menu = driver.find_element(By.XPATH ,'//*[@id="nav-tabContent"]/div[1]/div[1]/div/div[1]/div[2]/div/button')
        menu.click()
        input_menu= driver.find_element(By.XPATH,'//*[@id="nav-tabContent"]/div[1]/div[1]/div/div[1]/div[2]/div/div/div[1]/input')
        input_menu.send_keys("111")
        input_menu.send_keys(Keys.ENTER)
        menu2 = driver.find_element(By.XPATH,'//*[@id="nav-tabContent"]/div[1]/div[1]/div/div[2]/div[2]/div/button')
        time.sleep(1)
        menu2.click()
        if semester=="上學期":
            input_menu= driver.find_element(By.XPATH,'//*[@id="nav-tabContent"]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/ul/li[1]/a')
            input_menu.click()
        else :
            input_menu= driver.find_element(By.XPATH,'//*[@id="nav-tabContent"]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/ul/li[2]/a')
            input_menu.click()
        # 點擊「科目」的下拉式選單
        i=0
        while True:
            try:
                a = '//*[@id="row_'+str(i)+'"]/td[4]'
                lesson = driver.find_element(By.XPATH ,a)
                i += 1
            except Exception as e:
                break
        st ="big5"
        st2 = "utf-8"
        time.sleep(1)
        for j in range(i):
            a = '//*[@id="row_'+str(j)+'"]/td[4]'
            lesson = driver.find_element(By.XPATH ,a)
            lessonText = lesson.text.encode(st)
            f.write(lessonText.decode(st)+" ")

            a = '//*[@id="row_'+str(j)+'"]/td[8]'
            teacher = driver.find_element(By.XPATH ,a)
            teacherText = teacher.text.encode(st)
            f.write(teacherText.decode(st)+" ")

            a = '//*[@id="row_'+str(j)+'"]/td[9]'
            lessonTime = driver.find_element(By.XPATH ,a)
            lessonTimeText = lessonTime.text.encode(st)
            f.write(lessonTimeText.decode(st)+" ")

            a = '//*[@id="row_'+str(j)+'"]/td[10]'
            lessonClass = driver.find_element(By.XPATH ,a)
            lessonClassText = lessonClass.text
            f.write(lessonClassText+"\n")
            a = {
                "lesson": lessonText.decode(st),
                "teacher": teacherText.decode(st),
                "lessonTime": lessonTimeText.decode(st),
                "lessonClass": lessonClassText
            }
            b = json.dumps(a, ensure_ascii=False).encode(st2)  # 加上 ensure_ascii=False 避免中文字出現亂碼，轉換為 UTF-8 格式的 bytes
            f2.write(b.decode() + "\n")  # 寫入前再轉回 str
        f2.close()
        f.close()