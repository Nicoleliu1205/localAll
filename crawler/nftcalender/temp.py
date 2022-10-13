import requests
from bs4 import BeautifulSoup

path='./AiDragonsNFT Minting Oct 14, 2022.htm'
htmlfile=open(path,'r',encoding='Utf-8')
htmlhandle=htmlfile.read()
bs_temp = BeautifulSoup(htmlhandle,"html.parser")


nftitem = {}

nftitem['name'] = bs_temp.find('h1').get_text()

#nftitem['img']=bs_temp.find(name='div', attrs={'class':'nft-image nextdropimage nftinfocard'})['src']




#nftitem['video_img']=bs_temp.find(name='div', attrs={'class':'ytp-cued-thumbnail-overlay-image'})

#pricekey2 = bs_temp.find_all(name='div', attrs={'class': 'div-next-drops-info nftinfocard'})[1].find('div').get_text()
#nftitem[pricekey2] = bs_temp.find_all(name='div', attrs={'class': 'div-next-drops-info nftinfocard'})[1].find_all('div')[1].get_text()

print("nftitem:",nftitem)









