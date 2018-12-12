import requests
from bs4 import BeautifulSoup
import pandas
import re

URL = 'https://socialblade.com/youtube/user/therealvegasnay'
req = requests.get(URL)

soup = BeautifulSoup(req.text, 'html.parser')

content0 = soup.find_all("div",style =re.compile(r'width: 860px; height: 32px; line-height: 32px;'))
content2 = soup.find_all("div",{"style":"float: left; width: 205px;"})
content3 = soup.find_all("div",{"style":"float: left; width: 240px;"})

content0 = soup.find_all("div",style =re.compile(r'width: 860px; height: 32px; line-height: 32px;'))

web_content_list = []

for date1, totsubs, changeinsubs, vidtot1, changevid2 in zip(content0, content2, content2, content3, content3):
    
    # To store the information to a dictionary
      web_content_dict = {}
      web_content_dict["Date"]=date1.find('div',attrs = {'style':'float: left; width: 95px;'}).text.replace("\n","")
      web_content_dict["Change in Subscribers"]=changeinsubs.find('div',attrs = {'style':'width: 65px; float: left;'}).text.replace("\n","")
      web_content_dict["Total Subscribers"]=totsubs.find('div',attrs = {'style':'width: 140px; float: left;'}).text.replace("\n","")
      web_content_dict["Change in Views"]=changevid2.find('div',attrs = {'style':'width: 85px; float: left;'}).text.replace("\n","")
      web_content_dict["Total Views"]=vidtot1.find('div',attrs = {'style':'width: 140px; float: left;'}).text.replace("\n","")


# To store the dictionary to into a list
      web_content_list.append(web_content_dict)
      
# To make a dataframe with the list
df = pandas.DataFrame(web_content_list)
df = df[['Date','Change in Subscribers','Total Subscribers','Change in Views','Total Views']]
 
# To write the dataframe to a csv file
df.to_csv("Naomi_Youtube_SocialbladeMain.csv")
      

    