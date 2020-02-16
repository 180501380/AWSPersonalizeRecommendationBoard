import vlc, pafy
from time import sleep
url = "https://www.youtube.com/watch?v=1yNfzVABvCM"


item = dynamodb.get_item(TableName='movies', Key={'movieId': {'S': str(movieid)}})

# Gets the item
face_id = item['Item']['title']['S']


video = pafy.new(url)
best = video.getbest()
media = vlc.MediaPlayer(best.url)

print("test")
media.play()
print("test ")
sleep(2) #wait the player to be open
# while media.is_playing()==1:
#     pass
print("test")
sleep(20)
# Instance = vlc.Instance('--fullscreen')
# player = Instance.media_player_new()
# Media = Instance.media_new('http://fsi.stanford.edu/sites/default/files/video_4.mp4')
# Media.get_mrl()
# player.set_media(Media)
# player.play()