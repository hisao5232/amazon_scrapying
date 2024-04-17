from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# WebDriverのオプションを設定
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")  # セキュリティ上の制限を回避
options.add_argument("--lang=ja")     # 言語設定を日本語に

# ChromeDriverを使用してWebDriverのインスタンスを作成
driver = webdriver.Chrome(options=options)

HREFS = []
d_list = []

# URL開く
driver.get("https://www.amazon.co.jp/ref=nav_logo")
# 待機処理
# driver.implicitly_wait(10)
sleep(10)
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

#sleep(10)
#while True:
    #待機処理
wait.until(EC.presence_of_all_elements_located)

    #商品URLの取得
#counter = 10
while counter > 0:
    URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")
    for URL in URLS:
        URL = URL.get_attribute("href")
        print("[INFO] URL :", URL)
        HREFS.append(URL)
    wait.until(EC.presence_of_all_elements_located)
    driver.find_element(By.CSS_SELECTOR,"#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(78) > div > div > span > a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator").click()
    sleep(5)
    counter = counter - 1  # counter -= 1 でも同等    
print("Finish!!")

"""URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")

for URL in URLS:
    URL = URL.get_attribute("href")
    print("[INFO] URL :", URL)
    HREFS.append(URL)
    #商品詳細の取得 

for HREF in HREFS:
    driver.get(HREF)
    # title
    title = driver.find_element(By.ID, "productTitle").text
    print("[INFO]  title :", title)
    # price 
    price = driver.find_element(By.CSS_SELECTOR, 'div.aok-align-center > span > span > span.a-price-whole').text
    print("[INFO]  price :", price)
    # 複数画像取得
    images_btn = driver.find_elements(By.CSS_SELECTOR, "li.a-spacing-small.item.imageThumbnail.a-declarative > span > span > span > input")
    for index, image_btn in enumerate(images_btn, start=1):
        # input要素を一つずつクリック
        image_btn.click()
        sleep(5)
        wait.until(EC.presence_of_all_elements_located)
        try:
            img = driver.find_element(By.XPATH, f'(//div[@class="imgTagWrapper"]/img)[{index}]').get_attribute("src")
            print("[INFO]  img :", img)
        except NoSuchElementException:
            pass
    
    # img
    #img = driver.find_element(By.XPATH, '//div[@id="imgTagWrapperId"]/img').get_attribute("src")
    #print("[INFO]  img :", img)

    d={
        'title':title,
        'price':price,
        'img':img,      
        }
    d_list.append(d)

df=pd.DataFrame(d_list)
print(df)
df_URL = pd.DataFrame({'URL':HREFS})
print(df_URL)
df_concat= pd.concat([df, df_URL], axis=1)
print(df_concat)
df_concat.to_excel("amazon_keybord.xlsx")"""
    