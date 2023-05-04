import datetime
import time

import requests
from numpy.distutils.fcompiler import none

#抓取数据
from pandas.io import json


def get_data(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        html = requests.get(url, headers=headers)
        if html.status_code ==200:
            return html.content
        else:
            return none
#解析json
def parse_data(html):
    json_data = json.loads(html)['cmts']
    comments = []
    try:
        for item in json_data:
            comment = {
                'nickName': item['nickName'],
                'cityName': item['cityName'] if 'cityName' in item else '',
                'content': item['content'].strip().replace('\n', ''),
                'score': item['score'],
                'startTime': item['startTime']
            }
            comments.append(comment)
        return comments
    except Exception as e:
        print(e)

#保存内容到本地
def save():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time = '2018-11-09 00:00:00'
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset=15&startTime=' + start_time.replace(
            ' ', '%20')
        html = None
        try:
            html = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)
        comments =parse_data(html)
        start_time = comments[14]['startTime']
        print(start_time)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=-1)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
        for item in comments:
            print(item)
            with open('files/comments.txt', 'a', encoding='utf-8')as f:
                f.write(item['nickName']+','+item['cityName'] +','+item['content']+','+str(item['score'])+ item['startTime'] + '\n')
'''
#数据可视化
#数据可视化采用了pyecharts，按照地理位置制作了毒液观众群的分布图。部分代码如下：
def dataview():
    geo = Geo('《毒液》观众位置分布', '数据来源：猫眼-Ryan采集', **style.init_style)
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 1000],
            visual_text_color='#fff', symbol_size=15,
            is_visualmap=True, is_piecewise=False, visual_split_number=10)
    geo.render('观众位置分布-地理坐标图.html')

    data_top20 = Counter(cities).most_common(20)
    bar = Bar('《毒液》观众来源排行TOP20', '数据来源：猫眼-Ryan采集', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top20)
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render('观众来源排行-柱状图.html')

#词云图
#最后通过wordcloud制作词云，作为大众对该电影的综合评价。
comments = []
    with open('files/comments.txt', 'r', encoding='utf-8')as f:
        rows = f.readlines()
        try:
            for row in rows:
                comment = row.split(',')[2]
                if comment != '':
                   comments.append(comment)
                # print(city)
        except Exception as e:
            print(e)
    comment_after_split = jieba.cut(str(comments), cut_all=False)
    words = ' '.join(comment_after_split)
    #多虑没用的停止词
    stopwords = STOPWORDS.copy()
    stopwords.add('电影')
    stopwords.add('一部')
    stopwords.add('一个')
    stopwords.add('没有')
    stopwords.add('什么')
    stopwords.add('有点')
    stopwords.add('感觉')
    stopwords.add('毒液')
    stopwords.add('就是')
    stopwords.add('觉得')
    bg_image = plt.imread('venmo1.jpg')
    wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
                   stopwords=stopwords, max_font_size=400, random_state=50)
    wc.generate_from_text(words)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
'''
if __name__ == '__main__':
    url = 'http://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset=15&startTime=2018-11-19%2019%3A36%3A43'
    html = get_data(url)
    reusults = parse_data(html)
    save()