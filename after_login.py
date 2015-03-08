import urllib2 , urllib , random
from bs4 import BeautifulSoup

following = []

def searching_users () :
    global following
    value = '8442bbd15f5dcc18c6ebf950328053b3b9db1766'
    
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
    page = opener.open('https://twitter.com/following')
    
    txt = page.read()
    
    soup = BeautifulSoup(txt)
    user = '_arefhosseini'
    for i in soup.find_all('span' , class_='u-linkComplex-target') :
        new_user = str(i.string)
        if new_user != user :
            following.append(new_user)
    
    for i in range(10) :
        user = random.choice(following)
        following.remove(user)
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
        page = opener.open('https://twitter.com/%s/following'%user)
        
        txt = page.read()
        
        soup = BeautifulSoup(txt)
        for i in soup.find_all('span' , class_='u-linkComplex-target') :
            new_user = str(i.string)
            if new_user != user :
                following.append(new_user)
        


