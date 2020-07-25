
import pandas as pd
from bs4 import BeautifulSoup
from WebRequest import web_request
from PostRequest import post_request


class post_params:
    def get_source(self,link):
        Web = web_request(link, 'get')
        return Web.get_source()

    def find_post_forms(self, source):
        post_forms = []
        Soup = BeautifulSoup(source, features="lxml")
        # post_forms = Soup.find_all('form', attrs = {'method' : r'[pP}[oO][sS][tT]' })
        post_forms += Soup.find_all('form', attrs = {'method' : 'post' })
        post_forms += Soup.find_all('form', attrs = {'method' : 'POST' })
        if post_forms:
            return True
        return False

def read_excel(excel_filename):
    df = pd.read_excel(excel_filename)
    links = df['websites']
    return links

    
if __name__ == "__main__":
    post = post_params()
    links = list()
    links += ['https://www.earthsunmoon.com/']  # 200
    links += ['https://scau.edu.cn/']

    links = read_excel('data.xlsx')
    post_links = []
    for link in links:
        source = post.get_source(link)
        if source:
            if post.find_post_forms(source): 
                post_links.append(link)
                print(link)

 
    