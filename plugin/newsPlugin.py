#! usr/bin/env python3
from iPlugin import Plugin
from urllib import request
import chardet
from xml.etree import ElementTree
from lxml import etree
import threading
import Tools
import uuid

__all__ = ["newsPlugin"]

class newsPlugin(Plugin):
    name = "newsPlugin"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)
        self.mongo = Tools.MongoUtils("Taxation","Context")

    def downloade(self,url):
        response = request.urlopen(url)
        html = response.read()
        html = html.decode(chardet.detect(html)['encoding'])
        return html

    def dealOneSite(self,url,listXpath,titleXpath,postDataXpath,source,contextXpath,page):
        if(page=='page=1'):
            for page in range(1, 256):
                listContext = self.downloade(url + str(page))
                listPage = etree.HTML(listContext)
                hrefs = listPage.xpath(listXpath)
                postDates = listPage.xpath(postDataXpath)

                for (href,postDate) in zip(hrefs,postDates):
                    try:
                        self.dealContent(href, titleXpath, postDate, source, contextXpath)
                    except Exception as e:
                        print(e)

    def dealContent(self,contentUrl,titleXpath,postDate,source,contextXpath):
        print("download:   ",contentUrl)
        doc = {}
        doc['_id'] = uuid.uuid4();

        context = self.downloade(contentUrl)
        page = etree.HTML(context)
        title = page.xpath(titleXpath)
        source = source
        contents = page.xpath(contextXpath)
        contextClean = Tools.clearContent(contents)

        doc['title'] = title[0].strip()
        doc['postdate'] = postDate
        doc['mediaType'] = '新闻'
        doc['source'] = source
        doc['context'] = contextClean

        self.mongo.saveDoc(doc)

    def getResult(self):
        root = ElementTree.parse("../newsConf.xml")
        nodes = root.getiterator("node")
        threads = []
        for node in nodes:
            try:
                url = node.find('url').text
                listXpath = node.find('listUrl').text
                titleXpath = node.find('title').text
                postDataXpath = node.find('postDate').text
                source = node.find('source').text
                contextXpath = node.find('content').text
                page = node.find('page').text

                t = threading.Thread(target=self.dealOneSite,args=(url,listXpath,titleXpath,postDataXpath,source,contextXpath,page))
                threads.append(t)
            except Exception as e:
                print(e)

        for t in threads:
            t.setDaemon(True)
            t.start()

        t.join()

if __name__ == '__main__':
    obj = newsPlugin()
    obj.getResult()