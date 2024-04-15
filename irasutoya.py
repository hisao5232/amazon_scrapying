from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib

# 最新のchromeドライバーをインストールして、インストール先のローカルパスを取得
driver_path = ChromeDriverManager().install()
# chromeドライバーのあるパスを指定して、起動
driver = webdriver.Chrome(service=Service(executable_path=driver_path))

url = "https://www.irasutoya.com/search/label/%E8%81%B7%E6%A5%AD"
driver.get(url=url)

# コピーしたXPathを使って画像のWeb要素を取得
xpath = "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[5]/div/div/div/div[1]/a/img"
element = driver.find_element(by=By.XPATH, value=xpath)

# Web上の画像URLを取得
img_url = element.get_attribute("src")
print(img_url)

# urllibライブラリを使って画像URLからバイナリ読み込む
with urllib.request.urlopen(img_url)as rf:
    img_data = rf.read()

# with open()構文を使ってバイナリデータをpng形式で書き出す
with open("irasutoya.png", mode="wb")as wf:
    wf.write(img_data)

# Webドライバーの終了
driver.quit()