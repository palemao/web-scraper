#detail page code
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium import webdriver

driver = webdriver.Chrome(executable_path=r'C:\directory\Scraping Websites\extra\chromedriver')

my_url = "www.placed-url.com"

#function parsing a url int into HTML i.e. "soupifies"
def make_soup(url):
  driver.get(url)
  m_soup = soup(driver.page_source, features='html.parser')
  return m_soup 


main_page = make_soup(my_url)

#selecting borough name 
boroughs = [borough.text.strip() for borough in main_page.select('.seo_links.seo_links_country [href]')]

#controls the number of london boroughs 16-68 range// 44 for TH 
indexs = list(range(16,18)) ##16-22 to miss out croydon

london_list = [boroughs[i] for i in indexs]
#formats the borough names to be inputted into the link below
boroughs1 = [bo.replace("town","") for bo in london_list]
boroughs2 = [b1.replace("&","and") for b1 in boroughs1]
boroughs3 = ['-'.join(b2.split()) for b2 in boroughs2]

#inputting formatted borough names into a link to go onto each borough listing
borough_links = ["https://www.placed-url.com/care_search_results.cfm/searctary/" + b3 for b3 in boroughs3]

#turning each borough page with a list of care home listings into soup
borough_soups = [make_soup(b_link) for b_link in borough_links]


#this returns the links of detailed care home pages
detailed_soups_list = []
for soups in borough_soups:
   links = [link.get('href') for link in soups.select('.home-name [href]')]
   for link in links:
     detailed_soups_list.append(make_soup(link))
   next_html = soups.select('.col-sm-8.text-right [href]')
   for i in next_html:
      if i.text == 'Next':
       next_listing = make_soup(i.get('href'))
       for soups1 in next_listing:
         links2 = [link2.get('href') for link2 in soups1.select('.home-name [href]')]
         for link2 in links2:
          detailed_soups_list.append(make_soup(link2))
   

        
#lists the relvant HTML code for the care home profle dta for each care home
tags = [detailed_soup.select(".profile-group-description.col-xs-12.col-sm-8>p") for detailed_soup in detailed_soups_list]


h1_span_tags = [soup.select("div>h1>span") for soup in detailed_soups_list]

def return_title():
 title_ready = []
 for i in h1_span_tags:
    title_ready.append(['ListingName', i[0].text])
 return (title_ready)



#Address and postcode
span_tags = [soup.select("p>span") for soup in detailed_soups_list] 

def return_add():
 clean_addresses = []
 for s in range(len(span_tags)):
     clean_address_list = [i.text.replace('\n','').replace('\t', "") for i in span_tags[s][0:3]]
     clean_addresses.append("".join(clean_address_list))
 return(clean_addresses)



addresses_ready = []
for i in range(len(return_add())):
 addresses_ready.append(["Address", return_add()[i]])


def return_pc():
 clean_PC = []
 for i in range(len(span_tags)):
     clean_PC_list = [span_tags[i][2].text.replace('\n','').replace('\t', "")]
     clean_PC.append("".join(clean_PC_list))
 return(clean_PC)

pc_ready = []
for i in range(len(return_pc())):
 pc_ready.append(["Postcode", return_pc()[i]])





#cleans data of uncessarily HTML and structures the list necessary to used in a dataframe
def clean_str():
   structured_list = []
   for tag in tags:
     items = [t.text.replace('\n','').replace('\t', "").split(':') for t in tag]
     structured_list.append(items)
   return structured_list

data_ew = clean_str()



[data_ew[p].append(pc_ready[p]) for p in list(range(len(pc_ready)))]
[data_ew[a].append(addresses_ready[a]) for a in list(range(len(addresses_ready)))]
[data_ew[c].append(return_title()[c]) for c in list(range(len(return_title())))]


#create emptydata frame
headers = ['Company','ListingName', 'Address', 'Postcode', 'Local Authority', 
           'Owner', 'Manager', 'Type of Service']
df = pd.DataFrame(columns=headers)

  
filtered = [ [sl for sl in r if sl[0] in headers] for r in data_ew ]

     
#populates the datframe from clean_str function
for index, data in enumerate(filtered):
  # print(index,data)
    for item in data:
        # unpack the items in the list
       column, value = item[0], item[1]
        # store the value in the appropriate columns
       df.loc[index, column] = value
#print(df)

df.to_csv(r'C:\directory\trial14.csv', index = False, header = True)


