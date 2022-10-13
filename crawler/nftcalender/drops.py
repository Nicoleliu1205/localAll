import http
import logging

import pymongo
from bs4 import BeautifulSoup
from requests import session

import egbs4
import requests
import urllib3
import re
import os

os.environ['NO_PROXY'] = 'stackoverflow.com'


url = 'https://www.nftdropscalendar.com/upcoming-nfts'


def open_websites(url):
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    requests.adapters.DEAFAULT_RETRIES = 5
    response=requests.get(url,headers=headers,verify=False).text
    bs= BeautifulSoup(response,"html.parser")
    return bs

def iterate_page(bs):
    i = 1
    for element in bs.find_all(name='a',attrs='link-block-18 w-inline-block'):
        url_temp="https://www.nftdropscalendar.com"+element['href']
        print(" The  "+str(i)+" element is :",url_temp)
        bs_temp = BeautifulSoup(requests.get(url_temp).text,"html.parser")
        nfts = get_web_content(bs_temp)
        add_to_DB(nfts)
        i = i + 1
    return


def get_web_content(bs_temp):
    # 赋值
    nftitem = {}
    nftitem['name'] = bs_temp.find('h1').get_text()
#project details
    nftitem['mint_date'] = bs_temp.find(name='div', attrs='blockchain-nextdrop subtitle date nftinfocard').get_text()
    if (callable(bs_temp.find(name='div', attrs='blockchain-nextdrop subtitle nftinfocard'))):
        nftitem['belong_chain'] = bs_temp.find(name='div', attrs='blockchain-nextdrop subtitle nftinfocard').get_text()
    else:
        nftitem['belong_chain'] = ''
    pricekey = bs_temp.find(name='div', attrs={'class': 'div-next-drops-info nftinfocard'}).find('div').get_text()
    nftitem[pricekey] = bs_temp.find(name='div', attrs={'class': 'div-next-drops-info nftinfocard'}).find_all('div')[1].get_text()

    nftitem['item_number'] = \
    bs_temp.find(name='div', attrs={'class': 'div-next-drops-info collection nftinfocard cc'}).find_all('div')[1].get_text()
    nftitem['category'] = bs_temp.find(name='div', attrs={'class': 'div-next-drops-info collection nftinfocard'}).find_all('div')[1].get_text()
    nftitem['presale_date'] = bs_temp.find(name='a', attrs={'class': 'date-time presaleinfo w-inline-block'}).find('div').get_text()
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
    print("nftitem:",nftitem)
    return nftitem


def add_to_DB(nftitem):
    myclient = pymongo.MongoClient("mongodb://192.168.0.189:27017/")
    try:
        print(myclient.server_info())
    except Exception:
        print("Unable to connect to the mongoDB server.")
    db="owl-blockchain-0613"
    collection="nft_up_coming"
    addstr=nftitem
    mydb_account = myclient[db]
    mycol = mydb_account[collection]
    x = mycol.insert_one(addstr)
    print("插入数据库完成")
    return x.inserted_id

if __name__ == '__main__':
    bs=iterate_page(open_websites(url))



