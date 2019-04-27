import time
import urllib
import random
from bs4 import BeautifulSoup
import jieba
import re
import collections


def toformat(s):
    return s.replace('\n', '').replace('\r', '').replace(' ', '')

# 下载器
class Downloader(object):

    def __init__(self, url):
        self.url = url

    def download(self):
        html_content = urllib.request.urlopen(self.url).read()
        html_content = html_content.decode("utf-8")
        return html_content

# 页码管理器
class PageManager(object):

    def __init__(self, page=0):
        self.page = page

    def next(self):
        self.page += 1

    def prev(self):
        self.page = self.page -1 if self.page > 0 else 0

# 解析器
class Parser(object):

    def __init__(self, html_content):
        self.html_content = html_content

    def parse(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return self.parseNews(soup)

    def parseNews(self, soup):
        new_list = soup.find("ul", id='newsListContent').find_all('li')

        # 检查是否是最后一页
        end = False
        page_btns = soup.find_all('a', class_='page-btn')
        if len(page_btns) == 1 and page_btns[0].get_text() == "上一页":
            end = True
        news = []
        for item in new_list:
            title = item.find('p', class_='title').find('a').get_text()
            info = item.find('p', class_='info')
            if 'title' in info.attrs.keys():
                brief = info.attrs['title']
            else:
                brief = info.get_text()
            time = item.find('p', class_='time').get_text()

            title, brief, time = toformat(title), toformat(brief), toformat(time)
            dic = {'title': title, 'brief': brief, 'time': time}
            news.append(dic)
            # print(dic)    # check
        return news, end

# 统计分析器
class Analyser(object):

    def __init__(self, s):
        self.s = s

    def analyze(self):
        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
        self.s = re.sub(pattern, '', self.s)  # 将符合模式的字符去除

        # 文本分词
        cut_res = jieba.cut(self.s, cut_all=False)  # 精确模式分词
        list = []
        black_list = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。', u' ', u'、', u'中', u'在',
                      u'了', u'通常', u'如果', u'我们', u'需要', u'“', u"”", u"日", u"月", ]  # 自定义去除词库
        for word in cut_res:
            if word not in black_list and len(word) > 1:
                list.append(word)

        # # 词频统计
        word_counts = collections.Counter(list)         # 对分词做词频统计
        word_counts_top = word_counts.most_common(20)   # 获取前10最高频的词
        print(word_counts_top)  # 输出检查

# 控制器
class Controller(object):

    def __init__(self, month, day):
        self.downloader = None              # 下载器
        self.pagemanager = PageManager()    # 页面管理器
        self.parser = None                  # 解析器
        self.analyser = None
        self.month = month
        self.day = day

    def get_news(self):
        uri = "http://finance.eastmoney.com/a/cgnjj_%s.html"
        f = open('tmp/words.txt', 'w', encoding="utf-8")
        f.write('')
        s = ''
        while True:
            print("当前为page" + str(self.pagemanager.page+1))
            url = uri % self.pagemanager.page
            self.downloader = Downloader(url=url)
            html_content = self.downloader.download()
            self.parser = Parser(html_content)
            news, end = self.parser.parse()
            for new in news:
                if new['time'][0:2] == self.month and new['time'][3:5] == self.day:       # 确定是需要的日期的新闻
                    f = open('tmp/words.txt', 'a', encoding="utf-8")
                    f.write(new['brief']+';')
                    s += new['brief']+';'
            if end:
                break
            else:
                self.pagemanager.next()
                time.sleep(random.random()*2)
        self.analyser = Analyser(s=s)
        self.analyser.analyze()

if __name__ == '__main__':
    month = '04'
    day = '27'
    con = Controller(month=month, day=day)
    con.get_news()