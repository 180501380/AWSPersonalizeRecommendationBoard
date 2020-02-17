import boto3
import vlc, pafy
from time import sleep

dynamodb = boto3.client('dynamodb')
media = None
logging_table = 'logs'

def getvideoid(unixtime):
    unixtime = str(unixtime)
    videoid = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': unixtime}})
    videoid = videoid['Item']['mymess']['S']
    return videoid

# media varible that inside the function must be define by global first, otherwise, media outside the function will still ==None, since it can't detect this variable outside the function
def playthevideo(videoid):
    url = "https://www.youtube.com/watch?v=" + videoid
    video = pafy.new(url)
    best = video.getbest()
    global media
    media = vlc.MediaPlayer(best.url)
    media.play()
    sleep(2)

while True:
    # it will check the unixtime=2 record in table, if does there have videoid update
    videoid2 = getvideoid(2)

    # if videoid 2 have record is not 0, we have to show this trailer first!, since it is the record he press the button first
    if videoid2 != "0":
        media.stop()
        playthevideo(videoid2)
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': "2"},
                'mymess': {'S': "0"}
            })

    elif media == None:
        videoid = getvideoid(1)
        playthevideo(videoid)

    elif media.is_playing() == True:
        sleep(2)
        print("media is still playing")
        continue

    # when media player is off, we open a new media player
    # after the media player is open, it take some time to start the video, so for start the media.is_playing() will return 0 for a second
    # this stats is for whenever the video is stop, we close the player first, then we get the videoid again and play it. keep they have trailer to play
    elif (media.is_playing() == 0):
        media.stop()
        videoid = getvideoid(1)
        playthevideo(videoid)