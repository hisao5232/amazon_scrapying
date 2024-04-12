from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd

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
#wait = WebDriverWait(driver=driver, timeout=60)
 #検索窓 
Word = "キーボード"
driver.find_element(By.ID, "twotabsearchtextbox").send_keys(Word)
sleep(1)
driver.find_element(By.ID,"nav-search-submit-button").click()
 #商品URLの取得 
URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")

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
    # img
    img = driver.find_element(By.XPATH, '//div[@id="imgTagWrapperId"]/img').get_attribute("src")
    print("[INFO]  img :", img)

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
df_concat.to_excel("amazon_keybord.xlsx")
    