
from Common.loggerController import log
import time
from datetime import datetime
import certifi
import pymongo
from bs4 import BeautifulSoup
import urllib3
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

os.environ['NO_PROXY'] = 'stackoverflow.com'


url = 'https://www.nftdropscalendar.com/upcoming-nfts'

#列表页加载最新40条数据
def loading_latest_nfts(url):
    loading = "/html/body/div/div[2]/div[2]/div[1]/div[5]/a/div"
    chrome_options = webdriver.ChromeOptions()
    # 实现无可视化界面操作
    chrome_options = Options()
    chrome_options.add_argument('log-level=INT')
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    #chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)
    driver.find_element("xpath", loading).click()
    time.sleep(3)
    driver.find_element("xpath", loading).click()
    time.sleep(3)
    result = driver.page_source
    bs = BeautifulSoup(result, "html.parser")
    driver.close()
    return(bs)


#打开二级页面
def open_websites(url):
    http=urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()    )
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    response=http.request('GET',url,headers=headers).data
    bs= BeautifulSoup(response,"html.parser")
    return bs

#打开当页中每条项目数据
def iterate_page(bs):
    i = 1
    falsenum = 0
    for element in bs.find_all(name='a',attrs='link-block-18 w-inline-block'):
        url_temp="https://www.nftdropscalendar.com"+element['href']
        log.info(" The  "+str(i)+" element is :",url_temp)
        if falsenum < 4:
            bs_temp = open_websites(url_temp)
            nfts = get_web_content(bs_temp)
            falsenum=add_to_DB(i,nfts,falsenum)
        else:
            log.info("已经插入失败4条数据，退出执行脚本。请检查！")
            return
        i = i + 1
    return


#获取每个项目的具体参数
def get_web_content(bs_temp):
    # 赋值
    nftitem = {}
    nftitem['name'] = bs_temp.find('h1').get_text()
#project details
    mintdata= bs_temp.find(name='div', attrs='blockchain-nextdrop subtitle date nftinfocard').get_text()
    nftitem['mint_date'] = datetime.strftime(datetime.strptime(mintdata,"%B %d, %Y"), "%Y%m%d000000")
    nftitem["image_url"] = bs_temp.find(name='img', attrs={'class': 'nft-image nextdropimage nftinfocard'})['src']

    if (callable(bs_temp.find(name='div', attrs='blockchain-nextdrop subtitle nftinfocard'))):
        nftitem['belong_chain'] = bs_temp.find(name='div', attrs='blockchain-nextdrop subtitle nftinfocard').get_text()
    else:
        nftitem['belong_chain'] = ''
    pricekey = bs_temp.find(name='div', attrs={'class': 'div-next-drops-info nftinfocard'}).find('div').get_text()
    nftitem[pricekey] = bs_temp.find(name='div', attrs={'class': 'div-next-drops-info nftinfocard'}).find_all('div')[1].get_text()

    if (callable(bs_temp.find(name='div', attrs='div-next-drops-info collection nftinfocard presaledate'))):
        date_temp = bs_temp.find(name='a', attrs={'class': 'date-time presaleinfo w-inline-block'}).find('div').get_text()
        nftitem['presale_date'] = datetime.strftime(datetime.strptime(date_temp, "%B %d, %Y"), "%Y%m%d000000")
    else:
        nftitem['presale_date'] = ''

    nftitem['item_number'] = \
    bs_temp.find(name='div', attrs={'class': 'div-next-drops-info collection nftinfocard cc'}).find_all('div')[1].get_text()
    nftitem['category'] = bs_temp.find(name='div', attrs={'class': 'div-next-drops-info collection nftinfocard'}).find_all('div')[1].get_text()



    nftitem['twitter_user_name'] = \
    bs_temp.find(name='a', attrs={'class': 'div-next-drops-info collection nftinfocard w-inline-block'})['href']
    nftitem['twitter_followers'] = \
    bs_temp.find(name='a', attrs={'class': 'div-next-drops-info collection nftinfocard w-inline-block'}).find_all('div')[2].get_text()
    nftitem['discord_channel_name'] = \
    bs_temp.find_all(name='a', attrs={'class': 'div-next-drops-info collection nftinfocard w-inline-block'})[1]['href']
    nftitem['discord_member'] = \
    bs_temp.find_all(name='a', attrs={'class': 'div-next-drops-info collection nftinfocard w-inline-block'})[1].find_all('div')[2].get_text()
    nftitem['home_page'] = bs_temp.find(name='a', attrs={'class': 'link-block-6 w-inline-block'})['href']
    #nftitem['video_img']=bs_temp.find(name='div', attrs={'class': 'ytp--cuedthumbnail-overlay'})
    nftitem['description'] = bs_temp.find(name='p', attrs='nft-description nftinfocard nftinfopage').get_text()
    nftitem["is_valid"] = 'false'
    log.info("nftitem:",nftitem)
    return nftitem



#每个项目具体数据加入DB
def add_to_DB(i,nftitem,falsenum):
    myclient = pymongo.MongoClient("mongodb://192.168.0.189:27017/")
    try:
        log.info(myclient.server_info())
    except Exception:
        log.info("Unable to connect to the mongoDB server.")
    db="owl-blockchain-0613"
    collection="nft_up_coming"
    addstr=nftitem
    mydb_account = myclient[db]
    mycol = mydb_account[collection]
    try:
        x = mycol.insert_one(addstr)
        log.info("第"+str(i)+"条数据插入数据库完成！,数据库ID为："+str(x.inserted_id))
    except Exception as e:
        falsenum = falsenum+1
        log.info("第"+str(i)+"条数据插入数据库失败。已经有"+str(falsenum)+"条数据插入失败！")
        return falsenum
        #累计插入3条数据失败，则退出程序,待写

    return


if __name__ == '__main__':
    iterate_page(loading_latest_nfts(url))



