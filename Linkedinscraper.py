# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 09:38:37 2021

@author: Main
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import random
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import pandas as pd
from lxml import html
import itertools
import numpy as np 


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:80% !important; }</style>"))

"""TO DO LIST""
1.Make a note of which pages "Missed" posts due to updates

"""
def make_soup(url):
  driver.get(url)
  sleep(5)
  m_soup = soup(driver.page_source)
  return m_soup

#https://www.linkedin.com/search/results/content/?keywords=%22m%26c%20saatchi%20group%22&origin=CLUSTER_EXPANSION&page=2
#https://www.linkedin.com/search/results/content/?keywords=%22m%26c%20saatchi%20group%22&origin=CLUSTER_EXPANSION
  

my_url = 'https://www.linkedin.com/search/results/content/?keywords=%22m%26c%20saatchi%20group%22&origin=CLUSTER_EXPANSION'
driver = webdriver.Chrome(r'C:\Users\Main\Documents\M&Saatchi\chromedriver')
driver.get(my_url)

sleep(random.uniform(30, 31.75))

####MAIN PROGRAM#### - Page 1

source = soup(driver.page_source)
#post_link= soup.select('.relative [href]')

postlinkhtml = source.find_all("a", {"class": "app-aware-link social-activity-counts-insight--text inline-flex t-12 mt3 t-black--light link-without-visited-state"})

post_links = [i['href'] for i in postlinkhtml]

links1=[]
dates1=[]
post_text1 = []
comments1 = []

for i in post_links:
   postsoups = make_soup(i)
   posttxthtml = postsoups.find_all("div", {"class":"feed-shared-update-v2__description-wrapper ember-view"})
   commenthtml = postsoups.find_all("div", {"class": "comments-comment-item-content-body"})
   datehtml = postsoups.find_all("div",{"class": "feed-shared-actor__meta relative"})
   datehtml = datehtml[0].find_all("span", {"class": "visually-hidden"})
   if len(posttxthtml)==0 and len(commenthtml)!=0:
       for s in commenthtml:
        post_text1.append(np.nan)
        comments1.append(s.text.strip())
        links1.append(i)
        date = datehtml[0].text
        dates1.append(date.replace(' ago',''))
   elif len(commenthtml)==0 and len(posttxthtml)!=0:
       comments1.append(np.nan)
       post_text1.append(posttxthtml[0].text.strip())
       links1.append(i)
       date = datehtml[0].text
       dates1.append(date.replace(' ago',''))
   elif len(commenthtml)+len(posttxthtml)==0:
       comments1.append(np.nan)
       post_text1.append(np.nan)
       links1.append(i)
       date = datehtml[0].text
       dates1.append(date.replace(' ago',''))
   else:
    for s in commenthtml:
       comments1.append(s.text.strip())
       post_text1.append(posttxthtml[0].text.strip())
       links1.append(i)
       date = datehtml[0].text
       dates1.append(date.replace(' ago',''))


mssatchisentiment1 = pd.DataFrame(
    {'URL': links1,
     'Date': dates1,
     'post_text': post_text1,
     'comments': comments1
    })


###Page 2 onwards
secondpageplus = ["https://www.linkedin.com/search/results/content/?keywords=%22m%26c%20saatchi%20group%22&origin=CLUSTER_EXPANSION&page="+str(i) for i in range(2, 11)]

soups2 = [make_soup(i) for  i in secondpageplus]
                          
postlinkhtml2 = [t.find_all("a", {"class": "app-aware-link social-activity-counts-insight--text inline-flex t-12 mt3 t-black--light link-without-visited-state"}) for t in soups2]



post_links2 = []
for i in range(len(postlinkhtml2)):
 post_links2.append([i['href'] for i in postlinkhtml2[i]])

for i in post_links2:
    print(f'Number of Posts Captured {len(i)}')

post_links2merg = list(itertools.chain(*post_links2))

comments = []
post_text2 = []
links = []
dates = []
#try:
for i in post_links2merg:
   postsoups = make_soup(i)
   posttxthtml = postsoups.find_all("div", {"class":"feed-shared-update-v2__description-wrapper ember-view"})
   commenthtml = postsoups.find_all("div", {"class": "comments-comment-item-content-body"})
   datehtml = postsoups.find_all("div",{"class": "feed-shared-actor__meta relative"})
   datehtml = datehtml[0].find_all("span", {"class": "visually-hidden"})
   if len(posttxthtml)==0 and len(commenthtml)!=0:
       for s in commenthtml:
        post_text2.append(np.nan)
        comments.append(s.text.strip())
        links.append(i)
        date = datehtml[0].text
        dates.append(date.replace(' ago',''))
   elif len(commenthtml)==0 and len(posttxthtml)!=0:
       comments.append(np.nan)
       post_text2.append(posttxthtml[0].text.strip())
       links.append(i)
       date = datehtml[0].text
       dates.append(date.replace(' ago',''))
   elif len(commenthtml)+len(posttxthtml)==0:
       comments.append(np.nan)
       post_text2.append(np.nan)
       links.append(i)
       date = datehtml[0].text
       dates.append(date.replace(' ago',''))
   else:
    for s in commenthtml:
       comments.append(s.text.strip())
       post_text2.append(posttxthtml[0].text.strip())
       links.append(i)
       date = datehtml[0].text
       dates.append(date.replace(' ago',''))
 # except:
      
mssatchisentiment = pd.DataFrame(
    {'URL': links,
     'Date': dates,
     'post_text': post_text2,
     'comments': comments
    })


print(post_links2merg.index(links[-1]))
print(post_links2merg.index(links[-1])/10)
print(links[-1])


mssatchisentiment = pd.concat([mssatchisentiment1,mssatchisentiment])

mssatchisentiment.to_excel('mssatchisentiment.xlsx')



#tester = post_link[0].select('app-aware-link.social-activity-counts-insight--text.inline-flex.t-12 mt3.t-black--light.link-without-visited-state [href]')

#post_link.has_attr('href')

#alemaofrancis@gmail.com
#MSaatchi12

