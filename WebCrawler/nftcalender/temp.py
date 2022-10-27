import sys
import os

from Common.loggerController import log


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

log.info("已经插入失败4条数据，退出执行脚本。请检查！")
import re
mystr='https://discord.gg/MogulProductions'
#print(mystr[20:])
my=os.path.split(mystr)
print(my[1])
mystr2="3.7 K"
#print(float(mystr2[0:-2])*1000)

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



#nftitem['video_img']=bs_temp.find(name='div', attrs={'class':'ytp-cued-thumbnail-overlay-image'})

#pricekey2 = bs_temp.find_all(name='div', attrs={'class': 'div-next-drops-info nftinfocard'})[1].find('div').get_text()
#nftitem[pricekey2] = bs_temp.find_all(name='div', attrs={'class': 'div-next-drops-info nftinfocard'})[1].find_all('div')[1].get_text()

#print("nftitem:",nftitem)

