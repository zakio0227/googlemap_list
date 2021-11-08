import time
import csv
import os
import sys
from typing import Text                            # スリープを使うために必要
from selenium import webdriver         # Webブラウザを自動操作する（python -m pip install selenium)
import pyautogui as pag
import chromedriver_binary  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


driver = webdriver.Chrome()          
# GoogleMapを開く
driver.get('https://www.google.co.jp/maps')  


# 県名
kenmei = sys.argv[1]


# 検索ワードを送信・実行
search = driver.find_element_by_name("q")   
search.send_keys("キャンプ　"+ kenmei +"")  
search.send_keys(Keys.ENTER)                             

time.sleep(13)

# 取得したキャンプ場名とURLを突っ込む辞書
CampgroundNameAndURL = {}

# 「次のページ」ボタンが見えなくなるまでループ
while True:
    #「広告」の数
    advertisement = driver.find_elements_by_class_name("ARktye-badge")

    # 左下のボックス数と何ボックスまでか
    countBox = driver.find_elements_by_css_selector("span.Jl2AFb > span")
    countBegin = countBox[0].text
    countEnd = countBox[1].text
    
    # ボックスの数
    scrollCount = int(countEnd) - int(countBegin) + 1
    # ボックスの数＋広告の数
    scrollCount += len(advertisement)

    # スクロールできなくなるまでループ
    for num in range(scrollCount):
        targetBox = driver.find_elements_by_class_name("a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
         # 「キャンプ場」と「URL」を取得
        CampgroundName = targetBox[num].get_attribute('aria-label')
        url = targetBox[num].get_attribute('href')

        if len(advertisement) >= 0 and num >= len(advertisement):
            CampgroundNameAndURL[url] = CampgroundName
            
        # スクロール
        pag.moveTo(217,516)
        pag.vscroll(-5)
        time.sleep(1)

    nextPageButton = driver.find_element_by_id("ppdPk-Ej1Yeb-LgbsSe-tJiF1e")
    disable_new = nextPageButton.get_attribute('disabled')
    # 「次のページ」が表示されているかどうか
    if disable_new == "true":
        break
    #「次のページ」ボタンを押す
    nextPageButton.send_keys(Keys.ENTER)
    time.sleep(10)

time.sleep(2)

# キャンプ場名・住所・電話番号・URLを追加する配列
arr = []

# 取得したURLを開く
for openURL in CampgroundNameAndURL.keys():
    # URLにアクセス
    driver.get(openURL)
    time.sleep(5)
    # キャンプ場名
    CampgroundName = driver.find_elements_by_css_selector("div.x3AX1-LfntMc-header-title-ij8cu > div > h1 > span")
    if len(CampgroundName) == 0:
        CampgroundName = ""
    else:
        CampgroundName = CampgroundName[0].text

    # 住所
    CampgroundAdress = driver.find_elements_by_css_selector('button[aria-label^="住所:"]')
    if len(CampgroundAdress) == 0:
        CampgroundAdress = ""
    else:
        CampgroundAdress = CampgroundAdress[0].text

    # 電話番号
    CampgroundPhoneNum = driver.find_elements_by_css_selector('button[aria-label^="電話番号:"]')
    if len(CampgroundPhoneNum) == 0:
        CampgroundPhoneNum = ""
    else:
        CampgroundPhoneNum = CampgroundPhoneNum[0].text

    # URL
    CampgroundURL = driver.find_elements_by_css_selector('button[aria-label^="ウェブサイト:"]')
    if len(CampgroundURL) == 0:
        CampgroundURL = ""
    else:
        CampgroundURL = CampgroundURL[0].text

    arr.append([CampgroundName,CampgroundAdress, CampgroundPhoneNum, CampgroundURL])

# CSVのbodyにキャンプ場名〜URLを追加
csvBody = arr
# CSVファイル名
csvFileName = kenmei + ".csv"
# CSVファイルの保存先
saveFoldr = '/Volumes/GoogleDrive/マイドライブ/Eniciate企画/キャンプ場リスト'

# 指定のフォルダにCSVを作成、書き出しする関数
def save_file_at_dir(dir_path, filename, file_content, mode='w'):
    header = ['キャンプ場名', '住所','電話番号','URL']
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, filename), mode) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(file_content)
    f.close()

# CSVファイル新規作成・書き出し実行
save_file_at_dir(saveFoldr,csvFileName,csvBody,mode='w')
        
driver.quit()   

