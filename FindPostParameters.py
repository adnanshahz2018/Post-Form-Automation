
import pandas as pd
import requests
from bs4 import BeautifulSoup
from WebRequest import web_request
from PostRequest import post_request

class post_params:
    original_url = ''
    complete_link = ''
    username = 'xyzuser'
    email = 'user@xyz.com'
    password = 'xyzpassword'

    def get_source(self,link):
        self.original_url = self.complete_link = link
        Web = web_request(link, 'get')
        return Web.get_source()

    def post_forms(self, source):
        post_forms = []
        Soup = BeautifulSoup(source, features="lxml")
        # post_forms = Soup.find_all('form', attrs = {'method' : r'[pP}[oO][sS][tT]' })
        post_forms += Soup.find_all('form', attrs = {'method' : 'post' })
        post_forms += Soup.find_all('form', attrs = {'method' : 'POST' })
        if post_forms:
            return True, post_forms
        return False, None


    def post_links(self,post_forms):
        print('Number of POST Forms [', len(post_forms), ']')
        post_links = []
        for form in post_forms:                 # retrieviing all the input fields of a form
            # print(form, '\n')
            fields = form.find_all('input')
            other_inputs = ['submit', 'checkbox', 'radiobox']

            formdata = {}
            for field in fields:
                if field.get('type') not in other_inputs:
                    formdata[field.get('name')] = field.get('value')
            try:
                if 'email' in formdata:         formdata['email'] = self.email
                if 'user' in formdata:          formdata['user']  = self.username
                if 'username' in formdata:      formdata['username']  = self.username
                if 'user_name' in formdata:     formdata['user_name']  = self.username
                if 'pass' in formdata:          formdata['pass'] = self.password
                if 'passw' in formdata:         formdata['passw'] = self.password
                if 'password' in formdata:      formdata['password'] = self.password
            except Exception :
                print("Exception Occured")

            for f in formdata:
                if f and f.__contains__('name'):      formdata[f] = self.username 
                if f and f.__contains__('Name'):      formdata[f] = self.username 
                if f and f.__contains__('email'):     formdata[f] = self.email
                if f and f.__contains__('Email'):     formdata[f] = self.email
                if f and f.__contains__('password'):  formdata[f] = self.password

            # print('formdata: \n', formdata)
            if form.get('action'):
                url = self.make_link(form.get('action'))
                if url:
                    data = self.merge(form.get('action'), formdata)
                    # print('URL: ', url)
                    post_url = url + data
                    post_links.append(post_url)

        return post_links     

    def make_link(self,form_action):
        if not len(form_action) > 0 or not len(self.complete_link) > 0: 
            return None
        self.complete_link = self.original_url
        form_action = form_action.strip()

        if      self.if_complete_link(form_action):  self.complete_link = form_action
        elif    self.complete_link[-1] == '/' and form_action[0] == '/': self.complete_link = self.complete_link[:-1] + form_action
        elif    self.complete_link[-1] != '/' and form_action[0] == '/': self.complete_link = self.complete_link + form_action
        elif    self.complete_link[-1] != '/' and form_action[0] != '/': self.complete_link = self.complete_link + '/' + form_action
        else:   self.complete_link = self.complete_link + form_action
        
        if self.complete_link[0] == '/' and self.complete_link[1] == '/': self.complete_link = 'https:' + self.complete_link
        return self.complete_link

    def merge(self, action, formdata):
        data = '?'
        if action.__contains__('?'):    data = '&'
        for f in formdata:
            if formdata[f] and f:
                data += f + '=' + formdata[f] + '&' 
            elif f:
                data += f + '=' + '' + '&'
        form_data = data[:-1]
        return form_data

    def if_complete_link(self,action):
        if(action.__contains__('https') or action.__contains__('www') ):
            return True
        return False 
   

def read_excel(excel_filename):
    df = pd.read_excel(excel_filename)
    links = df['websites']
    return links

def driver():
    links = read_excel('data.xlsx')
    post_links = []
    for link in links:
        source = post.get_source(link)
        if source:
            if post.find_post_forms(source): 
                post_links.append(link)
                print(link)

    
if __name__ == "__main__":
    print('{FindPostParameters}')
    post = post_params()
    link = 'https://www.claytex.com/'
    links = read_excel('post.xlsx')

    for link in links:
        postlinks = []
        print('\nWebsite = ', link)
        source = post.get_source(link)
        flag, post_forms = post.post_forms(source)
        if flag:    postlinks = post.post_links(post_forms)
        for link in postlinks:  
            print('Post-Url:  \n', link)
            try:
                response = requests.post(link)
            except: 
                continue
            data = str(response.text)
            reflection = False
            if( data.__contains__(post.username) or 
                data.__contains__(post.email)  ):   
                reflection = True
            postlink = [link, response, reflection]
            with open('data.txt', 'a') as f: f.write( str(link) + '\t' + str(response) + '\t' + str(reflection) + '\n')   

    

    