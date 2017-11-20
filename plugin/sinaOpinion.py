#! usr/bin/env python3
from iPlugin import Plugin
import urllib.request
import chardet

__all__ = ["sinaOpinion"]

class sinaOpinion(Plugin):
    name = "sinaOpinion"
    version = '0.0.1'

    def __init__(self):
        Plugin.__init__(self)

    def download(self,url,body):
        data = urllib.parse.urlencode(body)
        data = data.encode('utf-8')
        request = urllib.request.Request(url)

        response = urllib.request.urlopen(request, data)

        html = response.read()
        html = html.decode(chardet.detect(html)['encoding'])
        return html

    def getResult(self,searKey):
        key = 'string:' + urllib.parse.quote(searKey)
        body = {'callCount':'1','c0-scriptName':'EChartsDwr','c0-methodName':'getHotTableAndLine4',
                'c0-id':'6554_1510998660007','c0-param0':key,'c0-param1':'string:','c0-param2':'string:24',
                'c0-param3':key,'c0-param4':'string:','c0-param5':'string:2017-11-17%2017%3A50%3A59',
                'c0-param6':'string:','c0-param7':'number:4','c0-param8':'string:2',
                'xml':'true'}
        result = self.download('http://wyq.sina.com/dwr/exec/EChartsDwr.getHotTableAndLine4.dwr',body)

        print(result)

if __name__ == '__main__':
    obj = sinaOpinion()
    obj.getResult('双一流')