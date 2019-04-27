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