# 导入相关包（网页数据爬取处理）
import requests
from bs4 import BeautifulSoup
import re
# 导入相关包（词云）
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from matplotlib.image import imread
import matplotlib.pyplot as plt
import jieba.analyse

# 处理函数
def get_title(html_title_url):
    title = []
    for news in html_title_url:
        a = news.select('a')
        title.append(a[0]['title'])
    return title


def get_url(html_title_url):
    url = []
    for news in html_title_url:
        a = news.select('a')
        url.append('https://news.fudan.edu.cn/'+a[0]['href'])
    return url

def get_time(html_time):
    time = []
    for news in html_time:
        string = str(news)
        news_time = re.findall(r'\d{1,4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}',string)
        time.append(news_time)
    return time

def get_views(html_views):
    views = []
    for news in html_views:
        string = str(news)
        news_views = re.findall(r'\d{1,9}',string)
        views.append(news_views[3])
    return views

# 处理过程
def process(url,i):
    # 得到html数据
    r = requests.get(url)
    strhtml = str(r.content,'utf-8')
    # print(strhtml)

    # 预处理
    soup = BeautifulSoup(strhtml, 'html.parser')
    html_title_url = soup.select('.news_title')
    html_time = soup.select('.times')
    html_views = soup.select('.wp_listVisitCount')

    # 得到相关数据
    title = get_title(html_title_url)
    url = get_url(html_title_url)
    time = get_time(html_time)
    views = get_views(html_views)

    # 写入数据
    with open('D:\\大三上\\python程序设计\\final-pj\\FudanNews.txt', 'a') as file_obj:
        for id in range(1, len(time)+1):
            news = {
                'id': id + 30 * i,
                'title': title[id-1],
                'url': url[id-1],
                'time': time[id-1],
                'views': views[id-1]
            }
            file_obj.write(str(news)+'\n')

    # 词云相关数据
    with open('D:\\大三上\\python程序设计\\final-pj\\news.txt', 'a') as file_obj:
        for id in range(1, len(time)+1):
            news = [title]
            file_obj.write(str(news)+'\n')

def news_wordcloud():
    back_img = imread("bg1.jpg")
    img_colors = ImageColorGenerator(back_img)

    with open("news.txt", encoding="gbk") as file:
        jieba.analyse.set_stop_words('stop.txt')  # 设置止词列表
        tags = jieba.analyse.extract_tags(file.read(), 1000, withWeight=True)
        data = {item[0]: item[1] for item in tags}

        word_cloud = WordCloud(font_path="c:\windows\Fonts\simhei.ttf",
                               background_color="white",
                               max_words=500,
                               max_font_size=200,
                               width=4096,
                               mask=back_img,
                               height=2160).generate_from_frequencies(data)

        word_cloud.recolor(color_func=img_colors)  # 替换默认的字体颜色
        plt.figure()  # 创建一个图形实例
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")  # 不显示坐标尺寸
        plt.show()


if __name__ == '__main__':
    url = 'https://news.fudan.edu.cn/pbl/list1.htm'
    Maxpage = 10    # 最大页数
    for i in range(Maxpage):
        url = re.sub('\d{1,2}',str(i+1),url)
        process(url, i)
    news_wordcloud()