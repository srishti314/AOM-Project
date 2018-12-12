from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint 

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q, channelId,token, max_results=50,order="relevance", location=None, location_radius=None):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want 
    maxResults=max_results,
    location=location,
    locationRadius=location_radius,
    channelId=channelId).execute()

    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    #likeCount = []
    #dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []
    date=[]
    
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            title.append(search_result['snippet']['title']) 

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            #likeCount.append(response['items'][0]['statistics']['likeCount'])
            #dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
            date.append(response['items'][0]['snippet']['publishedAt'])

        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])
        else:
            commentCount.append([])
	  
        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])

    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'commentCount':commentCount,'favoriteCount':favoriteCount, 'date':date}
    
    youtube_video=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in youtube_dict.items() ]))
    
    try:
      nexttok = search_response["nextPageToken"]
      return(youtube_video, nexttok)
    except Exception as e:
      nexttok = "last_page"
      return(youtube_video, nexttok)
      

writer = pd.ExcelWriter('youtube_video.xlsx', engine='xlsxwriter')
  
#video=pd.DataFrame()

channel=[['Michelle Phan', 'UCuYx81nzzz4OFQrhbKDzTng'], ['Shaaanxo', 'UCMpOz2KEfkSdd5JeIJh_fxw'], ['Jeffree Star', 'UCkvK_5omS-42Ovgah8KRKtg'], ['Kandee Johnson', 'UC9TreTE-iXwfwQl72DzDurA'], ['Naomi Giannopoulos', 'UCatI2zOJvBf5AM-V7GLGC2g'], ['Samantha Ravndahl', 'UC0qI3HpiBua75glb4RV5mWA'], ['Huda Kattan', 'UCRSvEADlY-caz3sfDNwvR1A'], ['Wayne Goss', 'UCCvoAe__WFYMNAEN-C-CtYA'], ['Zoe Sugg', 'UCrUbqTCagwsaP2Fmr0p1TsA'], ['PONY Syndrome', 'UCT-_4GqC-yLY1xtTHhwY0hA'], ["Manny Gutierrez" , "UCbO9bltbkYwa56nZFQx6XJg"]]

for i in range(0,len(channel)):
    video=pd.DataFrame()
    token=None
    x, token = youtube_search(None, channel[i][1], token)
    video=video.append(x)
    
    while token != "last_page":
        x, token = youtube_search(None, channel[i][1], token)
        video=video.append(x)
        
    sheet=channel[i][0]
    video.to_excel(writer, header=True, index=False, sheet_name=sheet)

writer.save()

    


    

