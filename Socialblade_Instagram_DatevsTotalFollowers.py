import requests
from bs4 import BeautifulSoup as bs
import pandas
import numpy as np


URL = 'https://socialblade.com/instagram/user/vegas_nay'
req = requests.get(URL)

soup = bs(req.text, 'html.parser')

content= soup.find_all("script",{"type" :"text/javascript"})
a = content[5].text

A = a.replace("\t\t\r\n\tg = new Dygraph(\r\n\r\n\t// containing div\r\n\tdocument.getElementById(\'DailyFollowersGraph\'),\r\n\t// CSV or path to a CSV file.\r\n\t","")
B = A.replace("Date,Total Followers\\n","")
C = B.replace("+","")
D = C.replace('\\n','')

head,sep,tail = D.partition('2018-04-02,2112433') ##change 2018-04-02,2112433 to represent the last row of the data

head1 = head.replace("'","").replace('"',"")
E=head1.split('  ')
F = E[1:]
e = [F[i].split(',') for i in range(len(F))]


# To make a dataframe with the list
df = pandas.DataFrame(e)
df.columns = ['Date','Followers']
df[["Date", "Followers"]] = df[["Date", "Followers"]].apply(pandas.to_numeric,errors='ignore')
df1 = df[["Date", "Followers"]]


df1.to_csv("Naomi_Instagram_DatevsFollowers.csv") 