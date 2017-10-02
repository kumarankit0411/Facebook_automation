import speech_recognition as sr
import os
from selenium import webdriver
import time

path = '/Users/ankitkrsingh/Desktop/code/FunScripts/sivraj/chromedriver' # change this accordingly
driver = webdriver.Chrome(path)

def openPage():
    global driver
    driver.get('https://www.facebook.com')
    driver.implicitly_wait(10)
    driver.find_element_by_id('email').send_keys('your username')
    driver.find_element_by_id('pass').send_keys('your password')
    driver.find_element_by_xpath("//input[@value='Log In']").click()
   

def getCommand():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            
        return r.recognize_google(audio, language="en")
    except:
        return 'oops'

def main():
    global driver
    openPage()
    current_feed = None
    time.sleep(10)
    poss=0
    post_number = 0
    posts = driver.find_elements_by_xpath('//div[@data-fte="1"]')
    while(1):
        if post_number > len(posts)-1:
            posts = driver.find_elements_by_xpath('//div[@data-fte="1"]')
        capture = getCommand()
        if 'next' in capture:
            os.system('say "going down"')
            post_number+=1
            pos=0
            try:
                loc = posts[post_number].location
            except:
                driver.execute_script('window.scroll(0,%s)' % str(loc+300))
                post_number-=1
                continue
            loc = loc['y']
            driver.execute_script('window.scroll(0,%s)' % str(loc-50))
            '''
            distance_to_travel = loc - poss
            while(pos<distance_to_travel):
                driver.execute_script('window.scroll(0,%s)' % str(pos+poss))
                time.sleep(.00001)
                pos+=1
            poss+=distance_to_travel
            '''
        elif 'back' in capture:
            if post_number!=0:
                post_number-=1
                os.system('say "going up"')
            else:
                os.system('say "cannot go up"')
            pos=0
            try:
                loc = posts[post_number].location
            except:
                driver.execute_script('window.scroll(0,%s)' % str(loc+300))
                post_number+=1
                continue
            loc = loc['y']
            driver.execute_script('window.scroll(0,%s)' % str(loc+50))
            '''
            distance_to_travel = poss - loc
            while(pos<distance_to_travel):
                driver.execute_script('window.scroll(0,%s)' % str(poss-pos))
                time.sleep(.00001)
                pos+=1
            if poss<distance_to_travel:    
                poss = 0
            else:
                poss-=distance_to_travel
            '''
        elif 'oops' in capture:
            os.system("say 'cannot hear you, please be clear'")
        elif 'exit' in capture:
            os.system('say "exiting, bye bye!!"')
            time.sleep(2)
            driver.quit()
            break 

if __name__ == '__main__':
    main()
    driver.quit()
    
