# eastmoney-yaowen-keyword
Python抓取东方财富要闻的热点词

## **下载**
- 直接下载`.zip`文件
- `git clone git@github.com:CatsJuice/eastmoney-yaowen-keyword.git`

## **使用前提**
- Python 3.x
- 第三方库支持
    - `urllib`
    - `BeautifulSoup`
    - `jieba`

## **使用**
自定义`main`中的参数， 参数说明如下

No | param | meaning
:--:|:--:|:--:
1 | `month` | 需要抓取的月份
2 | `day` |  需要抓取的日期
3 | `count` | 需要获取前几个热词

**运行**后将打印前`count`个热词

## **局限性**

中文分词并不是特别准， 很多实时热点词汇都无法识别或者被拆分；使用的是精确模式， 如果需要更改，更改如下代码即可：
```
    ...
    ...

    def analyze(self, n):
        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
        self.s = re.sub(pattern, '', self.s)  # 将符合模式的字符去除

        # 文本分词
        # cut_res = jieba.cut(self.s, cut_all=False)  # 精确模式分词
        cut_res = jieba.cut(self.s, cut_all=True)   # 修改成全模式

        ...
        ...
```