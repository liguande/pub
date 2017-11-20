#! usr/bin/env python3

from iPlugin import Plugin
from urllib import request
import urllib.parse
import chardet
import uuid
from lxml import etree
import Tools


__all__ = ["wechatPlugin"]

class wechatPlugin(Plugin):
    name = "wechatPlugin"
    version = '0.0.1'

    def __init__(self,mongo):
        Plugin.__init__(self)
        self.mongo = mongo

    def getResult(self, jsonData):
        key = jsonData['key']

        for page in range(1, 10):
            try:
                url = 'http://weixin.sogou.com/weixin?query=' + urllib.parse.quote(key)\
                        +'&_sug_type_=&s_from=input&_sug_=n&type=2&page=' + str(page) + '&ie=utf8'

                response = request.urlopen(url)
                html = response.read()
                html = html.decode(chardet.detect(html)['encoding'])
                page = etree.HTML(html)
                hrefs = page.xpath('//ul[@class="news-list"]//li/div[@class="txt-box"]/h3/a/@href')
                for href in hrefs:
                    try:
                        self.dealContent(href)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    def dealContent(self,href):
        print('begin download ', href)
        doc= {}
        doc['_id'] = uuid.uuid4();

        respone = request.urlopen(href)
        contentHtml = respone.read()
        contentHtml = contentHtml.decode(chardet.detect(contentHtml)['encoding'])

        treeContent = etree.HTML(contentHtml)

        title = treeContent.xpath('//h2[@class="rich_media_title"]//text()')
        postDate = treeContent.xpath('//em[@id="post-date"]//text()')
        source = treeContent.xpath('//a[@id="post-user"]//text()')
        contents = treeContent.xpath('//div[@class="rich_media_content "]//text()')

        cleaned_body = Tools.clearContent(contents)

        doc['title'] = title[0].strip()
        doc['postDate'] = postDate[0].strip()
        doc['mediaType'] = '微信'
        doc['source'] = source[0].strip()
        doc['context'] = cleaned_body
        self.mongo.saveDoc(doc)

if __name__ == '__main__':
    mongo = Tools.MongoUtils("Taxation", "wechatSearchContext")
    obj = wechatPlugin(mongo)
    obj.getResult({"key":"双一流"})
