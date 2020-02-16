#query moviename in youtube and play the video(1,get videoid, 2,play the video in vlc)


api = "AIzaSyAPmLV6syClmBFPBsQP15ATG3axev1dtUk"
from apiclient.discovery import build




youtube = build('youtube','v3', developerKey = api)

moviename="terminator 2"
req = youtube.search().list(q=moviename +' official trailer', part="snippet", type="video", maxResults =50,videoDuration="short").execute()
videoid=req['items'][0]['id']['videoId']

import vlc, pafy
from time import sleep
url = "https://www.youtube.com/watch?v="+ videoid
video = pafy.new(url)
best = video.getbest()
media = vlc.MediaPlayer(best.url)


media.play()
sleep(2) #wait the player to be open
# while media.is_playing()==1:
#     pass

print("is that all righ?")

sleep(10)