import boto3
import vlc, pafy
from time import sleep

dynamodb = boto3.client('dynamodb')
media = None
logging_table = 'logs'

while True:
    # it will check the unixtime=2 record in table, if does there have videoid update
    videoid2 = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "2"}})
    videoid2 = videoid2['Item']['mymess']['S']

    if videoid2 != "0":
        media.stop()
        url = "https://www.youtube.com/watch?v=" + videoid2
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.play()
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': "2"},
                'mymess': {'S': "0"}
            })
        sleep(3)
    elif media == None:

        videoid = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "1"}})
        videoid = videoid['Item']['mymess']['S']

        url = "https://www.youtube.com/watch?v=" + videoid
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.play()
        sleep(3)

    elif media.is_playing() == True:
        sleep(3)
        print(media.is_playing())
        continue

    # after the media player is open, it take some time to start the video, so for start the media.is_playing() will return 0 for a second
    # this stats is for whenever the video is stop, we close the player first, then we get the videoid again and play it. keep they have trailer to play
    elif (media.is_playing() == 0):
        media.stop()
        videoid = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "1"}})
        videoid = videoid['Item']['mymess']['S']
        url = "https://www.youtube.com/watch?v=" + videoid
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.play()
        sleep(3)



