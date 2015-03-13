from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2 , urllib

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

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'auth_token=%s'%value))
login_html = opener.open('https://twitter.com/following')
txt = login_html.read()
text = open('token.txt' , 'w')
text.write(value)
text.close()
 

