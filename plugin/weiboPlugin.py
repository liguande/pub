#! usr/bin/env python3
from iPlugin import Plugin
from urllib import request
import urllib.parse
import json
import chardet
import Tools
import re #正则表达式
from lxml import etree

__all__ = ["sinaOpinion"]

class sinaOpinion(Plugin):
    name = "sinaOpinion"
    version = '0.0.1'

    def __init__(self,mongo):
        Plugin.__init__(self)
        self.mongo = mongo

    def getResult(self,searKey):
        try:

            response = request.urlopen('http://s.weibo.com/weibo/' + urllib.parse.quote(searKey) + '&Refer=STopic_box')
            html = response.read()
            html = html.decode(chardet.detect(html)['encoding'])
            # html = html.decode('unicode_escape')
            pl_weibo_direct = re.findall(r'{"pid":"pl_weibo_direct"(.+?)}',html,re.S)
            data =  '{"pid":"pl_weibo_direct"' + pl_weibo_direct[0] + '}'
            text = json.loads(data)
            xml = text['html']
            treeContent = etree.HTML(xml)

            nickName = treeContent.xpath('//div[@class="search_feed"]//div[@class="content clearfix"]//div[@class="feed_content wbcon"]/a[@class="W_texta W_fb"]//text()')
            contents = treeContent.xpath('//div[@class="search_feed"]//div[@class="content clearfix"]//div[@class="feed_content wbcon"]/p[@class="comment_txt"]//text()')

            print(nickName)
            print(contents)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    mongo = Tools.MongoUtils("Taxation", "weiboSearchContext")
    obj = sinaOpinion(mongo)
    obj.getResult('双一流')