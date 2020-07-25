from urllib.request import urlopen
import urllib.response
import urllib.request
import urllib.parse
import requests 
import urllib3 
import re
from bs4 import BeautifulSoup

class post_request:  
    url = ''

    @staticmethod
    def get_source(self,url): 
        self.url = url   
        s1 = self.open_request()
        s2 = self.openurl()
        if len(s1) > len(s2): 
            source = s1 
        else:   
            source = s2
        if not source: 
            source = requests.post(self.url)
            source = source.text
        return source
    
    def open_request(self):
        session = requests.Session()
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html'}
        try:
            resp = requests.post(self.url, headers=headers, timeout=10)
            pagesource = resp.text
            if pagesource:  
                return pagesource
            else: 
                return requests.post(self.url)
        except:
            print('\n *[Requests Failed...]* ')
            return ''

    def openurl(self):  
        headers = {}
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html'}
        try:
            req  = urllib.request.Request(self.url)
            resp = urllib.request.urlopen(req, timeout=10)
            pagesource = resp.read().decode(encoding='utf-8', errors='strict') 
            return pagesource
        except:
            print('\n *[Urrlib Failure ]*') 
            return ''

if __name__ == "__main__":
    
    print('{PostRequest}')