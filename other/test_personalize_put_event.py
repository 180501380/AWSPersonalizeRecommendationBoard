import boto3
import time

kungfu= 31878
Ong_Bak= 27801
cradle2= 6196
rushhour= 4701

spiderman= 8636
xmen2= 6333
terminator= 589

harrypotter= 5816
lionking= 364



personalize_events = boto3.client('personalize-events')

current_time = int(time.time())
response = personalize_events.put_events(
    trackingId="281a4064-fdfc-46be-b169-986ee3840aa4",
    userId="testK",
    sessionId='1',

    eventList=[{
        'sentAt': current_time,
        'properties': "{\"itemId\":\"" + str(5816 ) + "\"}",
        'eventType': 'CLICK',
    }]
)



print(response)