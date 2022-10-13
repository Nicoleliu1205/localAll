'''
抓取新笔趣阁https://www.xbiquge6.com/单个小说
爬虫线路： requests - bs4 - txt
Python版本： 3.7
OS： windows 10
'''
import requests
import time
import sys
import os
import queue
from bs4 import BeautifulSoup
# 用一个队列保存url
q = queue.Queue()
# 首先我们写好抓取网页的函数
def get_content(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }

        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        content = r.text
        return content
    except:
        s = sys.exc_info()
        print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
        return " ERROR "


    links=sp.find_all('a')
    for link in links:
        print(link.name,link['herf'],link.get_text())
    post_list=sp.find(name="div",class_= "product-detail").text
# 解析内容
def praseContent(content):
    soup = BeautifulSoup(content,'html.parser')
    chapter = soup.find(name='div',class_="bookname").h1.text
    content = soup.find(name='div',id="content").text
    save(chapter, content)
    next1 = soup.find(name='div',class_="bottem1").find_all('a')[2].get('href')
    # 如果存在下一个章节的链接，则将链接加入队列
    if next1 != '/0_638/':
        q.put(base_url+next1)
    print(next1)
# 保存数据到txt
def save(chapter, content):
    filename = "修罗武神.txt"
    f =open(filename, "a+",encoding='utf-8')
    f.write("".join(chapter)+'\n')
    f.write("".join(content.split())+'\n')
    f.close

# 主程序
def main():
    start_time = time.time()
    q.put(first_url)
    # 如果队列为空，则继续
    while not q.empty():
        content = get_content(q.get())
        praseContent(content)
    end_time = time.time()
    project_time = end_time - start_time
    print('程序用时', project_time)

# 接口地址
base_url = 'https://www.xbiquge6.com'
first_url = 'https://www.xbiquge6.com/0_638/1124120.html'
if __name__ == '__main__':
    main()
