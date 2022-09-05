from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import time
import datetime
import requests
import os
options = Options()
options.add_argument("--headless")  # 隱藏視窗
options.add_argument("window-size=1200,700")
driver = webdriver.Chrome(chrome_options=options)
driver.get(
    "http://192.168.10.5/map.php?PHPSESSID=35ba17e43048f9c31f9cf246886fcc0e&mapFull")
driver.set_window_size(1100, 900)
size = driver.get_window_size()
#print("Window size: width = {}px, height = {}px".format(   size["width"], size["height"]))
sleep(2)
element = driver.find_element(
    "id", "senMarker1_text")   # 通過id定位
element1 = driver.find_element(
    "id", "senMarker2_text")
element_1 = str(element.text[3:5])   # 通過element元素為第4~6的值(濕度)
element1_1 = str(element1.text[3:7])   # 通過element元素為第3~7的值(溫度)
sleep(2)
notify = "濕度異常:" + element.text
notify1 = "溫度異常:" + element1.text
# LINE Notify 權杖 (NAC 異常通知群組)
token = 'vNV3UPGuglClosci3x8zXztYXkveRMimu3KFIVWstsV'
file_name = "./b.png"

if os.path.exists(file_name):
    os.remove(file_name)
    print('成功删除文件:', file_name)
else:
    print('未找到此文件:', file_name)
if element_1 > '80' or element_1 < '35':  # 濕度低35 高80警告
    headers = {"Authorization": "Bearer " + token}
    data = {'message': notify}
    driver.get_screenshot_as_file('./b.png')
    image = open('./b.png', 'rb')
    files = {'imageFile': image}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, files=files)
    driver .quit()
elif element1_1 > '28' or element1_1 < '15':  # 溫度低15 高28警告
    headers = {"Authorization": "Bearer " + token}
    data = {'message': notify1}
    driver.get_screenshot_as_file('./b.png')
    image = open('./b.png', 'rb')
    files = {'imageFile': image}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, files=files)
    driver .quit()
else:
    print("Success!")
    driver .quit()
