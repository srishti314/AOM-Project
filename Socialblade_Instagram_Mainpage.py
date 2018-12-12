import requests
from bs4 import BeautifulSoup
import pandas
import re

URL = 'https://socialblade.com/instagram/user/zoella'
req = requests.get(URL)

soup = BeautifulSoup(req.text, 'html.parser')

content0 = soup.find_all("div",{"class" :"TableMonthlyStats"},style =re.compile(r'width: 150px;'))
content1 = soup.find_all("div",{"class" :"TableMonthlyStats"},style =re.compile(r'width: 290px;'))
content2 = soup.find_all("div",{"class" :"TableMonthlyStats"},style =re.compile(r'width: 240px;'))

web_content_list = []

for date,af,totfol, afol, totfol in zip(content0,content1,content1,content2, content2):
    
    # To store the information to a dictionary
      web_content_dict = {}
      web_content_dict["Date"]=date.find('div',attrs = {'style':'width: 80px;','class':'TableMonthlySubStats'}).text.replace("\n","")
      web_content_dict["Added_Followers"]=af.find('div',attrs = {'style':'width: 100px;','class':'TableMonthlySubStats'}).text
      web_content_dict["Total_Followers"]=af.find('div',attrs = {'style':'width: 185px;','class':'TableMonthlySubStats'}).text.replace("\n","")
      web_content_dict["Added Following"]=afol.find('div',attrs = {'style':'width: 135px;','class':'TableMonthlySubStats'}).text.replace("\n","")
      web_content_dict["Total Following"]=totfol.find('div',attrs = {'style':'width: 100px;','class':'TableMonthlySubStats'}).text.replace("\n","")

     # To store the dictionary to into a list
      web_content_list.append(web_content_dict)

# To make a dataframe with the list
df = pandas.DataFrame(web_content_list)
 
# To write the dataframe to a csv file
df.to_csv("Zoe Sugg_Instagram_SocialbladeMain.csv")  