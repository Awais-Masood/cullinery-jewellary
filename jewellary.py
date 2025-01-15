from selenium import webdriver
#from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests
import json
from csv import writer
from time import sleep
import pandas as pd
import re
import os
import shutil
from urllib.parse import urljoin
Category_ = ''
Metal_ = ''
Shape_ = ''
Ring_ = ''
Sr_ = 0
datalist_rings = []
   
def selenium_section (url):    
    global Category_
    global Metal_
    global Shape_
    dir = 'engagement-rings'
    Category_ = 'engagement-rings'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #Without it warning are thrown.
    options.add_experimental_option("detach", True) # This enables browser to stay alive when run from command prompt.
    #options.add_argument('--proxy-server=%s' % proxy)
    #options.add_argument("start-maximized")
    #options.add_argument("disable-infobars")
    #proxy_helper = SeleniumAuthenticatedProxy (proxy_url="http://33994:49933@10.50.151.254:2356")
    #proxy_helper.enrich_chrome_options(options)
    #options.add_extension ("proxy.zip")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get (url)
    sleep (15)     
    last_height = driver.execute_script("return document.body.scrollHeight")
    els = driver.execute_script ('return document.body')
    els.send_keys (Keys.PAGE_DOWN)
    try:
        els = WebDriverWait (driver, 20).until (
            EC.presence_of_element_located((By.CLASS_NAME, 'close.reset.svelte-7f4f6y'))
        )
        print ('Pop up is present')
        els.click ()
    except Exception as e:
        print ('Pop up did not appear in 20 seconds. Going to move ahead')
        print (str (e))
    #els = driver.find_elements (By.CLASS_NAME, 'reset.root.svelte-8cbvf6')
    #### Metal Section (Single Tone )##########
    els = driver.find_element (By.CLASS_NAME, 'filters.limit-width.svelte-128ewnv')
    els = els.find_element (By.CLASS_NAME, 'filters_column_row')
    els = els.find_elements (By.CLASS_NAME, 'filters_column')
    print (len (els))
    els = els[1].find_elements (By.TAG_NAME, 'button')
    els.pop (0) # Remove spurious value from list of metals
    #els.pop (0) # Remove Platinum as it is scrapged
    #els.pop (0) # Remove 18K Yellow Gold as it is scrapped already.
    #els.pop (0) # Remove 18K Rose Gold as it is scrapped already.
    for item in els:
        first_time_entry = True
        metal = item.find_element (By.TAG_NAME, 'p').text
        Metal_ = metal 
        print ('Metal ==>> ' + metal)
        print ('-----------------')
        dir = 'engagement-rings'
        dir = os.path.join (dir, metal) # engagement-rings/platinum (18K Yellow Gold, 18K Rose Gold, 18K White Gold)
        item.click ()
        sleep (15)
        #### Shape Section ##########
        els_scroll = driver.find_element (By.CLASS_NAME, 'scroll-content.svelte-rexg8n')
        els = els_scroll.find_elements (By.TAG_NAME, 'button')
        print (len (els))
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        # els.pop (0)
        i = 0
        for item in els:
            # Following code section written because when new metal is clicked first time shapes section scroll will be at the end.
            # This code brings Shapes Section Scroll to the right.
            if first_time_entry:
                first_time_entry = False
                try:
                    els_right_scroll = driver.find_element (By.CLASS_NAME, 'root.svelte-rexg8n')
                    els = els_right_scroll.find_element (By.CLASS_NAME, 'reset.arrow.arrow-left.svelte-rexg8n')
                    els.click ()
                    sleep (2)
                    els.click ()
                except Exception as e:
                    print ('Exception occurred while scrolling left. Should reach start of shapes section by now')

            shape_dir = dir # engagement-rings/platinum (18K Yellow Gold, 18K Rose Gold, 18K White Gold)
            i += 1
            try:
                item.click ()
                sleep (15)
            except Exception as e:
                print ('Exception due to right scroll occurred.')
                print (str (e))
                els_right_scroll = driver.find_element (By.CLASS_NAME, 'root.svelte-rexg8n')
                els = els_right_scroll.find_element (By.CLASS_NAME, 'reset.arrow.arrow-right.svelte-rexg8n')
                els.click ()
                sleep (2)
                item.click ()
                sleep (15)

            shape = item.find_element (By.TAG_NAME, 'span').text
            Shape_ = shape
            print ('Shape == >> ', shape)
            shape_dir = os.path.join (shape_dir, shape) # engagement-rings/platinum (18K Yellow Gold, 18K Rose Gold, 18K White Gold)/round (Round, Oval, Emerald, Radiant)
            item.click
            sleep (15)
            els = driver.find_elements (By.CLASS_NAME, 'link.svelte-19gl59f')
            driver.execute_script("arguments[0].scrollIntoView();", els[-1])
            sleep (3)
            try:
                els = driver.find_element (By.CLASS_NAME, 'shine-button.load-more.svelte-128ewnv')
                els.click ()
                sleep (15)
            except Exception as e:
                print ('Exception Occurred')
                print (str (e))
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                els = driver.find_elements (By.CLASS_NAME, 'link.svelte-19gl59f')
                driver.execute_script("arguments[0].scrollIntoView();", els[-1])
                sleep (10)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print ('---------- End of Web Page Reached ----------')
                    break
                last_height = new_height
            els = driver.execute_script ("return document.body")    
            els.send_keys (Keys.HOME)
            sleep (2)
            els.send_keys (Keys.PAGE_DOWN)
            #############################
            els = driver.find_elements (By.CLASS_NAME, 'link.svelte-19gl59f')
            base_url = 'https://www.cullenjewellery.com'
            j = 0
            for item in els:
                j += 1
                try:
                    url = urljoin (base_url, item.get_attribute ('href'))
                    print (url)
                    requests_section (url, shape_dir)
                except Exception as e:
                    print ('Exception occurred. Most probably ad encountered.')
                    print (str (e))
                # if j == 2:
                #     return
            #############################
            # if i == 1: # Shape Control Counter
            #     return
        #break
def requests_section (url, dir):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    r = requests.get (url, headers=headers)
    print (r.status_code)
    result = r.text
    beautiful_soup_section (result, dir)

def beautiful_soup_section (page_source, dir):
    global Ring_
    global datalist_rings
    global Sr_    
    doc = BeautifulSoup (page_source, 'html.parser')
    name = doc.find ('h1', class_='svelte-gwj5u7').get_text ()
    print (name)
    name = name.split ()
    print (name)
    name = name [0]
    print (name)
    Ring_ = name
    dir = os.path.join (dir, name) # engagement-rings/platinum (18K Yellow Gold, 18K Rose Gold, 18K White Gold)/round (Round, Oval, Emerald, Radiant)/Emma (Aysa, April)
    try:
        os.makedirs (dir)
    except Exception as e:
        print ('Exception Occurred')
        print (str (e))
        return
    div_ = doc.find_all ('div', class_='thumb')
    sr = 0
    ########## Images Section ###############
    for item in div_:
        Sr_+=1
        sr += 1
        img_ = item.find ('img')
        #print (img_)
        print ('===============================')
        img_source = img_['src']
        img_source = img_source.replace ('100x100', '600x600')
        try:
            im = requests.get (img_source, timeout=30)
            print (img_source)
        except Exception as e:
            print ('Exception occurred requests section while getting image', sr, 'of ', dir)
            print (str (e))
            #return
        sleep (5)
        print (dir)
        img_path = dir + '/' + str (sr) + '.jpg'
        print (img_path)
        empty_str = ""
        try:
            with open (img_path, 'wb') as f:
                f.write (im.content)
            dict_rings = {
                'Sr': Sr_,
                'Category': Category_,
                'Metal': Metal_,
                'Shape': Shape_,
                'Ring': Ring_,
                'Image':sr,
                'Picture': empty_str
            }
            datalist_rings.append (dict_rings)
        except Exception as e:
            print ('Exception Occurred while writing image')
            print (str (e))
    return
                
########### MAIN FUNCTION ###########
if __name__ == "__main__":
    url = "https://www.cullenjewellery.com/engagement-rings"
    selenium_section(url)
    #export_to_excel ()
