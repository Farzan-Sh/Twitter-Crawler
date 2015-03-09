from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2 , urllib
from bs4 import BeautifulSoup
import threading


##------------------  scrape thread stuff
class scrape_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.user = ''
    def run(self):
        global following
        self.do_it()
    def do_it(self):
        self.user = specify_user()
        get_followers(value, self.user)

def get_page_source(url, user):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
    login_html = opener.open('https://twitter.com/%s/following'%user)
    txt = login_html.read()
    return txt

def searching_keyword(text , key_list) :
    counter = 0
    whole_text = ''
    soup = BeautifulSoup(text)
    for i in soup.find_all('p' , class_='ProfileTweet-text js-tweet-text u-dir') :
        text = str(i.next.encode('ascii' , 'ignore'))
        try :
            text += str(i.find('span' , class_='js-display-url').string)
        except :
            pass
        whole_text += text
    for i in key_list :
        counter += whole_text.count(i)
    print counter

##------------------  search thread stuff
class search_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.user = ''
    def run(self):
        global following
        while ( len(following) != 0 ):
            self.do_it()
            #print following
    def do_it(self):
        self.user = specify_user()
        get_followers(value, self.user)

def specify_user():
    global following
    try:
        user = following[0]
        if user not in added_list:
            added_list.append(user)
            print 'user added'
            following.remove(following[0])
            return user
        else:
            following.remove(following[0])
            specify_user()        
    except:
        pass

#----------- func to return following usernames list
following = []
added_list = []
def get_followers(token, username) :
    global following
    value = token

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
    page = opener.open('https://twitter.com/%s/following'%username)

    txt = page.read()

    soup = BeautifulSoup(txt)
    user =   'Sh_Farzan' #'_arefhosseini'
    for i in soup.find_all('span' , class_='u-linkComplex-target') :
        new_user = str(i.string)
        if new_user != user :
            following.append(new_user)
    #return following


#---------  log in stuff
browser = webdriver.Firefox()
browser.get('https://twitter.com')
element = browser.find_element_by_id('signin-email')
element.send_keys('arefhosseini@yahoo.com')
element = browser.find_element_by_id('signin-password')
element.send_keys('aref1441375')
element.send_keys(Keys.ENTER)
cookies = browser.get_cookies()
for i in cookies :
    if i['name'] == 'auth_token' :
        value = str(i['value'])
        break
browser.close()

#--------- opening following page using token
get_followers(value , 'Sh_Farzan')
for i in range(1,11):
    s = 'thread%d = search_Thread()'%i
    exec(s)

for i in range(1,11):
    s = 'thread%d.start()'%i
    exec(s)


