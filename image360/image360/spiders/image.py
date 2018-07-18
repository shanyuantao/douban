# -*- coding: utf-8 -*-
from json import loads
from urllib.parse import urlencode
from image360.items import BeautyItem
import scrapy

# 爬虫
class ImageSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'image'
    # 允许访问的域名
    allowed_domains = ['image.so.com']

    # 初始 请求
    def start_requests(self):
        """
        360图片都是后天异步加载的， 所以要爬加载图片时访问的url,这个可以在后台的network下的XHR，向下滚动图片页面
        然后会发现加载出来url,url的样式：http://image.so.com/zj?ch=beauty&sn=120&listtype=new&temp=1
        一页是30条，当向下滚动加载图片时，只有参数 sn 在变化，分别是30 60 90 120......
        我们可以粘贴上面的url打开，会看到访问时加载的html内容，不过不好看，可以使用菜鸟里的工具，json在线格式，转换成
        json格式查看
        """
        # 基础url, 供下面拼接时使用
        base_url = 'http://image.so.com/zj?'
        # 基础 url 后面传入的参数
        param = {'ch': 'beauty', 'listtype': 'new', 'temp': 1}
        # 一页是30条数据，我们定义爬取10页内容
        for page in range(10):
            # 把sn参数传入上面的字典,?后面的参数 是and 关系，所以只要参数齐全就可以，谁先谁后无所谓
            param['sn'] = page * 30
            # urlencode可以把字典的键值对，变成'ch=beautiful&listtype=new&temp=1&sn=30' 这个样式
            # 这个是可以在下面的python交互式环境中测试
            full_url = base_url + urlencode(param)
            # 这里是返回10个值给函数，以便于解析， return 执行一次函数就停止执行了，所以返回给函数多次值时可以用生成器 yield
            # 请求 url 这里是循环一次， 返回一个GET请求，并且回调解析函数，如果使用return的话，循环一次就停止了
            yield scrapy.Request(url=full_url, callback=self.parse)

    # 页面解析
    def parse(self, response):
        # 把页面的内容，变为json格式，也就是变成了一个字典(使用菜鸟教程json在线解析之后 可以清晰的看到页面页面中的内容)
        model_dict = loads(response.text)
        # 要拿取的内容在list键对应的以列表作为值的容器中， model_dict['list'] 根据键取出值
        # 循环出 列表中的内容  依然是个字典 取出内容放到item字段中
        for elem in model_dict['list']:
            # 创建item对象
            item = BeautyItem()
            item['title'] = elem['group_title']
            item['tag'] = elem['tag']
            item['width'] = elem['cover_width']
            item['height'] = elem['cover_height']
            item['url'] = elem['qhimg_url']
            yield item
