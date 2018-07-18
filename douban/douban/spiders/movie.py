# -*- coding: utf-8 -*-
import scrapy

from douban.items import MovieItem

# 启动项目命令 scrapy crawl movie(爬虫的名字） -o result.json
# -o result.json 会把定义的爬取到的定义的字段的内容存放到 项目下的result.json文件中， 该文件是自动生成的


class MovieSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'movie'
    # 允许访问的域名
    allowed_domains = ['movie.douban.com']
    # 页面时静态加载时，爬取该页面内容的url
    start_urls = ['https://movie.douban.com/top250']
    # 解析页面  response是自动生成的 response <200 https://movie.douban.com/top250?start=0&filter=>
    # 后面参数代表翻页， 一页25条内容 filter没有值， start =  0, 25,50,75.....
    def parse(self, response):
        # 使用XPATH语法拿到页面中的li标签，一个li写了一部电影的描述
        li_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        # 循环取出li标签
        for li in li_list:
            # 字段使用字典得到形式表示的。给字典的健赋值
            # 该字段定义的是要爬取的内容选项，我只定义类三个，只想爬取电影的标题和电影的评分以及电影下面的描述
            # text()意思是取出span[1]下的内容，extract_first()抽取第一个内容
            item = MovieItem()
            item['title'] = li.xpath('div/div[2]/div[1]/a/span[1]/text()').extract_first()
            item['score'] = li.xpath('div/div[2]/div[2]/div/span[2]/text()').extract_first()
            item['motto'] = li.xpath('div/div[2]/div[2]/p[2]/span/text()').extract_first()
            # 生成一个一个字典，不过生成器是可以迭代的，当返回多次值时，又不影响程序的执行，使用yield
            yield item
            print('11111111111111111111111111111')
            # {'motto': '平民励志片。 ', 'score': '8.9', 'title': '当幸福来敲门'}
            print(item)

            print('22222222222222222222222222222')
        # 取出带有href属性的a标签的href属性的内容并且该内容要满足后面的正则表达式，形如？start=任意字符的字符串
        # 该给标签是下面的分页号码链接，可以到页面底部，找到翻页点击检查， 即可查看到， 这里是取出所有的页码
        href_list = response.css('a[href]::attr("href")').re('\?start=.*')
        # 循环取出href的内容
        for href in href_list:
            # 拼接 response的 url 和 href ，href会把url中相同部分的字符串给替换掉
            url = response.urljoin(href)
            print('------------00000000000000000000------------------')
            # ?start=25&filter=
            print(href)
            # https://movie.douban.com/top250?start=25&filter=
            print(url)
            # <200 https://movie.douban.com/top250?start=0&filter=>
            print(response)

            print('------------00000000000000000000------------------')
            # 抓取url中的内容， 放到生成器中， 并且调用解析函数，解析url, 就是执行上面的步骤
            # 上面取出了所有的页码 ， 得到一个url就解析一次，并放到生成器中
            # 请求访问的url
            yield scrapy.Request(url=url, callback=self.parse)

# json格式就是列表中放字典，但是字典中可以一个键可以对应多个值，多个值又可以使用列表存放，如果一个值又是一个键的话，那么又可以在
# 列表中定义一个字典