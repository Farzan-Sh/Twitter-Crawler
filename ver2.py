#--------- imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2 , urllib
from bs4 import BeautifulSoup
import threading
import sys
import time

#---------- global vars
tokenfile = open('token.txt','r')
value = tokenfile.read()
tokenfile.close()
keywordsfile = open('keywords.txt','r')
keywords = keywordsfile.read().split()
keywordsfile.close()
followings = ['Sh_Farzan']
lvl1_passed_users = []
sources_for_user_extract = []
mainpage_sources_with_user = []
G = {}
Compiled_Users = []
#---------- main functions
def add_user_page_source(user):
    global value
    global sources_for_user_extract
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
    login_html = opener.open('https://twitter.com/%s/following'%user)
    txt = login_html.read()
    sources_for_user_extract.append(  (user,txt) )
    return

def user_extract(user_and_source_txt):
    relation_list = []
    global G
    global followings
    global sources_for_user_extract
    soup = BeautifulSoup(user_and_source_txt[1])
    user = user_and_source_txt[0]
    for i in soup.find_all('span' , class_='u-linkComplex-target') :
        new_user = str(i.string)
        if new_user != user :
            followings.append(new_user)
            relation_list.append(new_user)
    G[user] = relation_list
    return

def add_user_mainpage_source(user):
    global value
    global mainpage_sources_with_user
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
    login_html = opener.open('https://twitter.com/%s'%user)
    txt = login_html.read()
    mainpage_sources_with_user.append(  (user,txt) )
    return

def search_keyword(mainpage_sources_with_user) :
    counter = 0
    global keywords
    whole_text = ''
    try:
        user = mainpage_sources_with_user[0]
        soup = BeautifulSoup(mainpage_sources_with_user[1])    
        for i in soup.find_all('p' , class_='ProfileTweet-text js-tweet-text u-dir') :
            text = str(i.next.encode('ascii' , 'ignore'))
            try :
                text += str(i.find('span' , class_='js-display-url').string)
            except :
                pass
            whole_text += text
            whole_text += '    '
        for i in keywords :
            counter += whole_text.count(i)
        except:
            pass
    Compiled_Users.append( (user , counter) )
    return
    

def specify_items(List):
    try:
        item = List[0]
        if List == followings:
            if item not in lvl1_passed_users:
                lvl1_passed_users.append(item)
        List.remove(List[0])
        return item
    except:
        pass
    

#---------- threads
class pause_Thread (threading.Thread):
    def __init__(self):
        self.t = time.time()
        threading.Thread.__init__(self)
    def run(self):
        global Compiled_Users
        while 1:
            if sys.stdin.read(1) == 'p':
                print time.time() - self.t
                print Compiled_Users
                

class lvl1_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.item = ''
    def run(self):
        global followings
        while True:
            if ( len(followings) != 0 ):
                self.do_it()
    def do_it(self):
        self.item = specify_items(followings)
        add_user_page_source(self.item)


class lvl2_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.item = ''
    def run(self):
        global sources_for_user_extract
        while True:
            if ( len(sources_for_user_extract) != 0 ):
                self.do_it()
    def do_it(self):
        self.item = specify_items(sources_for_user_extract)
        user_extract(self.item)


class lvl3_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.item = ''
    def run(self):
        global lvl1_passed_users
        while True:
            if ( len(lvl1_passed_users) != 0 ):
                self.do_it()
    def do_it(self):
        self.item = specify_items(lvl1_passed_users)
        add_user_mainpage_source(self.item)


class lvl4_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.item = ''
    def run(self):
        global mainpage_sources_with_user
        while True:
            if ( len(mainpage_sources_with_user) != 0 ):
                self.do_it()
    def do_it(self):
        self.item = specify_items(mainpage_sources_with_user)
        search_keyword(self.item)


#--------- main

pThread = pause_Thread()
pThread.start()

lvl1Thread_1 = lvl1_Thread()
lvl1Thread_2 = lvl1_Thread()
lvl1Thread_1.start()
lvl1Thread_2.start()

lvl2Thread_1 = lvl2_Thread()
lvl2Thread_2 = lvl2_Thread()
lvl2Thread_1.start()
lvl2Thread_2.start()

lvl3Thread_1 = lvl3_Thread()
lvl3Thread_2 = lvl3_Thread()
lvl3Thread_1.start()
lvl3Thread_2.start()

lvl4Thread_1 = lvl4_Thread()
lvl4Thread_2 = lvl4_Thread()
lvl4Thread_3 = lvl4_Thread()
lvl4Thread_4 = lvl4_Thread()
lvl4Thread_1.start()
lvl4Thread_2.start()
lvl4Thread_3.start()
lvl4Thread_4.start()










        




