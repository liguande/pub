#coding:utf-8
import sys
from urllib import request
sys.path.append('../')
import re
from iPlugin import Plugin
import chardet
import uuid
import pymongo
from lxml import etree

__all__ = ["SecondPlugin"]

class SecondPlugin(Plugin):
   
    name = "sencondPlugin"
    version = '0.0.1'
    client = None
    db = None
    collection = None

    def __init__(self):
        Plugin.__init__(self)
        uri = 'mongodb://bjl:123456@127.0.0.1/Taxation?authMechanism=SCRAM-SHA-1'
        self.client = pymongo.MongoClient(uri)

        self.db = self.client['Taxation']

        self.collection = self.db["newsText"]

    def getResult(self, jsonData):
        for i in range(1,2):
            print('begin deal with page ',i)

            url ="http://roll.news.sina.com.cn/s/channel.php?ch=01#col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page=" + str(i)
            response = request.urlopen(url)
            html = response.read()
            html = html.decode(chardet.detect(html)['encoding'])

            page = etree.HTML(html)
            hrefs = page.xpath('//div[@id="d_list"]//ul//li//span/a/@href')

            for href in hrefs:
                self.dealContent(href)

    def dealContent(self, href):

        print('begin download ',href)
        id = uuid.uuid4();

        respone = request.urlopen(href)
        contentHtml = respone.read()

        contentHtml = contentHtml.decode(chardet.detect(contentHtml)['encoding'])

        treeContent = etree.HTML(contentHtml)
        contents = treeContent.xpath('//div[@id="artibody"]/div//text()')

        body = ''
        for content in contents:
            if content.strip() == '':
                continue
            body = body + str(content)

        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filterdata = re.findall(pattern, body)
        cleaned_body = ''.join(filterdata)

        doc = {'_id':str(id),'content':cleaned_body}

        print('doc:  ',doc)

        self.collection.insert(doc)

if __name__ == '__main__':
    obj = SecondPlugin()
    obj.getResult({"testkey":"testValue"})