import time
import urllib
from datetime import datetime

import certifi
import requests
import urllib3
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 规避检测
from selenium.webdriver import ChromeOptions



'''
#本地页面
path='./AiDragonsNFT Minting Oct 14, 2022.htm'
htmlfile=open(path,'r',encoding='Utf-8')
htmlhandle=htmlfile.read()
bs_temp = BeautifulSoup(htmlhandle,"html.parser")

url="https://www.nftdropscalendar.com/nft-drops/origin-heroes"
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
result=http.request(
    'GET',
    url=url,
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
).data

#使用Chrome浏览器
driver=webdriver.Chrome(ChromeDriverManager().install())
#隐藏指纹
with open('/Users/kingname/test_pyppeteer/stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": js
})
'''
url="https://www.nftdropscalendar.com/upcoming-nfts"
loading="/html/body/div/div[2]/div[2]/div[1]/div[5]/a/div"
chrome_options=webdriver.ChromeOptions()
#实现无可视化界面操作
chrome_options = Options()
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
#option=webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver=webdriver.Chrome(options=chrome_options)

driver.get(url)
time.sleep(3)
driver.find_element("xpath",loading).click()
time.sleep(3)
driver.find_element("xpath",loading).click()
time.sleep(3)
result=driver.page_source
bs= BeautifulSoup(result,"html.parser")
driver.close()
i = 1
for element in bs.find_all(name='a',attrs='link-block-18 w-inline-block'):
    url_temp="https://www.nftdropscalendar.com"+element['href']
    print(" The  "+str(i)+" element is :",url_temp)
    i = i + 1



#nftitem['video_img']=bs_temp.find(name='div', attrs={'class':'ytp-cued-thumbnail-overlay-image'})

#pricekey2 = bs_temp.find_all(name='div', attrs={'class': 'div-next-drops-info nftinfocard'})[1].find('div').get_text()
#nftitem[pricekey2] = bs_temp.find_all(name='div', attrs={'class': 'div-next-drops-info nftinfocard'})[1].find_all('div')[1].get_text()

#print("nftitem:",nftitem)

