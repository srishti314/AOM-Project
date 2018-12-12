import requests
from bs4 import BeautifulSoup as bs
import pandas
import numpy as np


URL = 'https://socialblade.com/youtube/user/mannymua733'
req = requests.get(URL)

soup = bs(req.text, 'html.parser')

content= soup.find_all("script",{"type" :"text/javascript"})
b = content[5].text
a = content[6].text

A = a.replace("\t\t\r\n\tg = new Dygraph(\r\n\r\n\t// containing div\r\n\tdocument.getElementById(\'AverageSubsPerMonth\'),\r\n\t// CSV or path to a CSV file.\r\n\t","").replace("Date,Monthly Subs\\n","").replace("+","").replace('\\n','')
B = b.replace("\t\t\r\n\tg = new Dygraph(\r\n\r\n\t// containing div\r\n\tdocument.getElementById(\'AverageViewsPerMonth\'),\r\n\t// CSV or path to a CSV file.\r\n\t","").replace("Date,Monthly Views\\n","").replace("+","").replace('\\n','')


head,sep,tail = A.partition('2018-10-1,-70706') ##change 2018-10-1,7111839 to represent the last row of the data

head1 = head.replace("'","").replace('"',"")
E=head1.split('  ')
F = E[1:]
e = [F[i].split(',') for i in range(len(F))]

## To make a dataframe with the list
df = pandas.DataFrame(e)
df.columns = ['Date','Monthly Subs']
df[["Date", "Monthly Subs"]] = df[["Date", "Monthly Subs"]].apply(pandas.to_numeric,errors='ignore')
df1 = df[["Date", "Monthly Subs"]]
#
#
df1.to_csv("Manny_Youtube_DatevsMonthly Subscribers.csv") 

head,sep,tail = B.partition('2018-10-1,7111839') ##change 2018-10-1,7111839 to represent the last row of the data

head2= head.replace("'","").replace('"',"")
M=head2.split('  ')
N = M[1:]
m = [N[i].split(',') for i in range(len(N))]

## To make a dataframe with the list
df = pandas.DataFrame(m)
df.columns = ['Date','Monthly Views']
df[["Date", "Monthly Views"]] = df[["Date", "Monthly Views"]].apply(pandas.to_numeric,errors='ignore')
df2 = df[["Date", "Monthly Views"]]

df2.to_csv("Manny_Youtube_DatevsMonthly Views.csv") 
