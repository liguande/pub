#! usr/bin/env python3
from urllib import request
import chardet
import re #正则表达式
import pymongo

def download(url):
    response = request.urlopen(url)
    html = response.read()
    html = html.decode(chardet.detect(html)['encoding'])
    return html

def clearContent(contents):
    body = ''
    for content in contents:
        if content.strip() == '':
            continue
        body = body + str(content)

    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, body)
    cleaned_body = ''.join(filterdata)
    return cleaned_body

class MongoUtils:
    def __init__(self,databasesName,collectionName):
        uri = 'mongodb://bjl:123456@192.168.1.108/Taxation?authMechanism=SCRAM-SHA-1'
        self.client = pymongo.MongoClient(uri)

        self.db = self.client[databasesName]

        self.collection = self.db[collectionName]

    def saveDoc(self,doc):
        try:
            self.collection.insert(doc)
        except Exception as e:
            print(e)

    def close(self):
        self.client.close()