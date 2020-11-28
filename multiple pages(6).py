import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium import webdriver

driver = webdriver.Chrome(executable_path=r'C:\Users\Main\Documents\Work\Projects\Scraping Websites\extra\chromedriver')

my_url = "https://www.carehome.co.uk/"

def make_soup(url):
  driver.get(url)
  m_soup = soup(driver.page_source, features='html.parser')
  return m_soup 

main_page = make_soup(my_url)

boroughs = [borough.text.strip() for borough in main_page.select('.seo_links.seo_links_country [href]')]

indexs = list(range(44,45))

london_list = [boroughs[i] for i in indexs]

boroughs1 = [bo.replace("Borough","") for bo in london_list]
boroughs2 = [b1.replace("&","and") for b1 in boroughs1]
boroughs3 = ['-'.join(b2.split()) for b2 in boroughs2]

borough_links = ["https://www.carehome.co.uk/care_search_results.cfm/searchunitary/" + b3 for b3 in boroughs3]

borough_soup = [make_soup(b_link) for b_link in borough_links]

def get_detail_links(borough_soup):
 links1 = []
 for soups in borough_soup:
   links = [link.get('href') for link in soups.select('.home-name [href]')]
   links1.append(links)
 return(links1)


def title(borough_soup):
 titles1 = []
 for soups in borough_soup:
   titles = [title.text.strip() for title in soups.select('.home-name [href]')]
   titles1.append(titles)
 return(titles1)

titles = title(borough_soup)

def address(borough_soup):
 address1 = []
 for soups in borough_soup:
   addresses = [address.text.strip() for address in soups.select('.home-name>p.grey')]
   address1.append(addresses)
 return(address1)

addresses = address(borough_soup)

#indexs3 = list(range(0,2))


#df_list = [pd.DataFrame(zip(titles[i], addresses[i]), columns = ['title','address']) for i in indexs3]
#df = pd.concat(df_list)



df = pd.DataFrame(columns=['boroughs'])

for i  in range(len(titles)):
   tmp = pd.DataFrame(list(zip(titles[i],addresses[i])),columns=['titles','add'])
   tmp["boroughs"] = boroughs2[i]
   df = df.append(tmp,ignore_index= True)


#df.to_csv(r'C:\Users\lemonade\Documents\Prannoy python\trial1.csv', index = False, header = True)