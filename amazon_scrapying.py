from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import urllib
from time import sleep
import time
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

options = webdriver.ChromeOptions()
#options.add_argument("--headless")

HREFS = []
d_list = []
d_img_list=[]
d_img={}

# URL開く
driver.get("https://www.amazon.co.jp/ref=nav_logo")
# 待機処理
# driver.implicitly_wait(10)
sleep(2)
wait = WebDriverWait(driver=driver, timeout=60)
 #検索窓 
Word = "外付けハードディスク"
#例外処理　検索窓のIDの違い
try:
    driver.find_element(By.ID, "twotabsearchtextbox").send_keys(Word)
except:
    driver.find_element(By.ID,"nav-bb-search").send_keys(Word)

sleep(1)
driver.find_element(By.ID,"nav-search-submit-button").click()

sleep(2)
#while True:
    #待機処理
#wait.until(EC.presence_of_all_elements_located)

    #商品URLの取得
counter = 1
while counter < 2:
    URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")
    print("エレメント取得")
    for URL in URLS:
        URL = URL.get_attribute("href")
        #print("[INFO] URL :", URL)
        HREFS.append(URL)
    wait.until(EC.presence_of_all_elements_located)
    print(f"URL取得{counter}")
    next=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[68]/div/div/span/a[3]")
    print("next取得")
    next_URL = next.get_attribute("href")
    driver.get(next_URL)
    sleep(2)
    counter = counter + 1  
print("Finish!!")

for HREF in HREFS[0:3]:
    driver.get(HREF)
    sleep(1)
    # title
    title = driver.find_element(By.ID, "productTitle").text
    print("[INFO]  title :", title)
    # price 
    price = driver.find_element(By.ID, 'corePriceDisplay_desktop_feature_div').text
    print("[INFO]  price :", price)
    d={
        'title':title,
        'price':price,      
        }
    d_list.append(d)

    # 複数画像取得
    images_btn = driver.find_elements(By.CSS_SELECTOR, "li.a-spacing-small.item.imageThumbnail.a-declarative > span > span > span > input")
    for index, image_btn in enumerate(images_btn, start=1):
        # input要素を一つずつクリック
        image_btn.click()
        sleep(2)
        wait.until(EC.presence_of_all_elements_located)
        try:
            img = driver.find_element(By.XPATH, f'(//div[@class="imgTagWrapper"]/img)[{index}]').get_attribute("src")
            d_img[f'picture_{index}']=img
            print(d_img)
            
        except:
            pass
    
    try:
        picture_1 = d_img.pop("picture_1")
        picture_2 = d_img.pop("picture_2")
        picture_3 = d_img.pop("picture_3")
        picture_4 = d_img.pop("picture_4")
        picture_5 = d_img.pop("picture_5")
        picture_6 = d_img.pop("picture_6")
    except:
        pass
    
    d_img_d={
             'picture_1':picture_1,
             'picture_2':picture_2,
             'picture_3':picture_3,
             'picture_4':picture_4,
             'picture_5':picture_5,
             'picture_6':picture_6,
             }
    d_img_list.append(d_img_d)

df=pd.DataFrame(d_list)
df_URL = pd.DataFrame({'URL':HREFS[0:3]})
df_img=pd.DataFrame(d_img_list)
df_concat= pd.concat([df, df_URL], axis=1)
df_concat_2=pd.concat([df_concat,df_img], axis=1)
df_concat_2.to_excel("amazon_deta.xlsx")
