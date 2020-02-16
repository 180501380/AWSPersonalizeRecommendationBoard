import boto3
import vlc, pafy
from time import sleep

media = None
while True:
    if media==None:
        dynamodb = boto3.client('dynamodb')

        videoid = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "1"}})
        videoid = videoid['Item']['mymess']['S']

        url = "https://www.youtube.com/watch?v=" + videoid
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.play()
        sleep(5)
    elif media.is_playing()==True:
        sleep(3)
        print(media.is_playing())
        continue

    # after the media player is open, it take some time to start the video, so for start the media.is_playing() will return 0 for a second
    elif (media.is_playing() == 0):
        media.stop()
        videoid = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "1"}})
        videoid = videoid['Item']['mymess']['S']
        url = "https://www.youtube.com/watch?v=" + videoid
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.play()
        sleep(5)



