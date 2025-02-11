'''
        Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
        SPDX-License-Identifier: MIT-0
'''

import boto3
import time
from googleapiclient.discovery import build

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
rekognition = boto3.client('rekognition')
personalize = boto3.client('personalize-runtime')

face_collection = "Faces"  # Name of the face collection that the AWS Rekognition uses
face_match_threshold = 70  # Match Threshold for the faces to be considered the same person
logging_table = 'logs'  # DynamoDB table name for the log files


def lambda_handler(event, context):
    utime = str(int(time.time()))  # Current Unix Time

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    image = {
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
        }
    }

    response = rekognition.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-1:910854190331:project/movie4/version/movie4.2020-02-10T19.12.42/1581333159624',
        Image=image,
        MaxResults=1,
        MinConfidence=51
    )

    try:
        itemid = response['CustomLabels'][0]['Name']
    except IndexError:
        itemid = None

    if itemid:
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': utime},
                'mymess': {'S': "we have detect" + itemid}
            })
        #debug
        print("we have detect" + itemid +"   " + utime)
    else:
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': utime},
                'mymess': {'S': "we can't detect any movie"}
            })
        #debug
        print("we can't detect any movie" + "    "+ utime)

    Faceid = detect_faces(image, bucket, key)

    #debug
    print("faceid:   " + Faceid)

    if key[5] =="3" and itemid:
        videoid =get_videoid(itemid)
        put_interaction(Faceid, itemid)
    else:
        videoid = get_recommend_trailerlink(itemid,Faceid)
    print(key)
    # make the time a bit larger, since if the time is same, it will update the same record of detect the item or not message.
    dynamodb.put_item(
        TableName=logging_table,
        Item={
            'unixtime': {'S': str(int(utime)+10)},
            'mymess': {'S': "This is your youtube videoid:  " + videoid}
        })
    # debug
    print("This is your youtube videoid :  " + videoid +"    " + str(int(utime)+10))

    if key[5] in ["2","3"]:
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': "2"},
                'mymess': {'S': videoid}
            })
    else:
        #this record is for pc to get the videoid
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': "1"},
                'mymess': {'S':videoid}
            })

    return videoid

def detect_faces(image, bucket, key):
    # Checks if user face is already registered in rekongtion collection
    faces = rekognition.search_faces_by_image(CollectionId=face_collection, Image=image,
                                              FaceMatchThreshold=face_match_threshold, MaxFaces=1)
    utime = int(time.time())  # Current Unix Time
    time_5_minutes_ago = int(utime) - 300

    if len(faces['FaceMatches']) == 1:  # User is already registered in the collection
        # Authenticate
        faceid = faces['FaceMatches'][0]['Face']['FaceId']

        # Checks if 5 minutes passed since the last upload
        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': str(utime)},
                'mymess': {'S': "person: " + str(faceid)}
            })
        return faceid

    else:
        # Face not found in the Rekognition database
        faces = rekognition.index_faces(Image=image, CollectionId=face_collection)

        # Check if there are no faces in the image:
        if len(faces['FaceRecords']) == 0:
            dynamodb.put_item(
                TableName=logging_table,
                Item={
                    'unixtime': {'S': str(utime)},
                    'mymess': {'S': "No faces were found in the picture"}
                })
        # More than one face in the image:
        elif len(faces['FaceRecords']) > 1:
            rekognition.delete_faces(CollectionId=face_collection,
                                     FaceIds=[f['Face']['FaceId'] for f in faces['FaceRecords']])

            dynamodb.put_item(
                TableName=logging_table,
                Item={
                    'unixtime': {'S': str(utime)},
                    'mymess': {'S': "Error: More than one face detected in the image"}
                })

            return 'More than one face in the image'

        # One new face in the image, register it:
        else:
            face_id = faces['FaceRecords'][0]['Face']['FaceId']

            dynamodb.put_item(
                TableName=logging_table,
                Item={
                    'unixtime': {'S': str(utime)},
                    'mymess': {'S': "Congratulations! " + face_id + "  have been register"}
                })

            return face_id


def get_recommend_trailerlink(itemid=None, FaceId=None):
    # if we have itemid, we can get more accurate recommendation by sims, if we also have faceid, we can push the interation to personalize
    if itemid and FaceId:
        response = personalize.get_recommendations(
            campaignArn="arn:aws:personalize:us-east-1:910854190331:campaign/sims",
            itemId=itemid,
            numResults=1
        )


        recommendid = response["itemList"][0]["itemId"]
        videoid = get_videoid(recommendid)
        put_interaction(FaceId, itemid)
        return videoid


    elif itemid:
        response = personalize.get_recommendations(
            campaignArn="arn:aws:personalize:us-east-1:910854190331:campaign/sims",
            itemId=itemid,
            numResults=1
        )

        recommendid = response["itemList"][0]["itemId"]
        videoid = get_videoid(recommendid)
        return videoid

    #if we can't detect the item, we still can give recommendation by the userid
    elif FaceId:
        response = personalize.get_recommendations(
            campaignArn="arn:aws:personalize:us-east-1:910854190331:campaign/personlize-metadata",
            userId=FaceId,
            numResults=1
        )
        recommendid = response["itemList"][0]["itemId"]
        videoid = get_videoid(recommendid)
        return videoid
    else:
        pass


def get_videoid(recommendid):
    # query dynamodb table to get the moviename of this itemid
    item = dynamodb.get_item(TableName='movies', Key={'movieId': {'N': str(recommendid)}})
    # Gets the moviename
    moviename = item['Item']['title']['S']

    videoid = search_videoid(moviename)
    return videoid



def search_videoid(moviename):

    # api = "AIzaSyAPmLV6syClmBFPBsQP15ATG3axev1dtUk"
    # api = "AIzaSyBNeB4tPi4pJtPwaqfZoDMAlp-A4D0gdRA"
    # api = "AIzaSyDNytLy54eX78XnZIZTwfWoO_wtqRL_5-8"
    # api = "AIzaSyC0doWSvgIslVMFtEZaMatNhlu9DlIzIZU"
    # api = "AIzaSyDLth8xB9eWXXMb7JfdXZ5sG6_Qzilk3H4"
    # api = "AIzaSyA23-AIarv-AieyK_pDZfFpH_7lxLe3nOQ"
    api = "AIzaSyB767n9_ZqeFXBMlpqIQD76BRBYmPIMgi0"
    youtube = build('youtube', 'v3', developerKey=api, cache_discovery=False)

    moviename = moviename
    req = youtube.search().list(q=moviename + ' official trailer', part="snippet", type="video", maxResults=50,
                                videoDuration="short").execute()
    videoid = req['items'][0]['id']['videoId']

    return videoid

def put_interaction(userid,movieid):
    # put interaction to personalize event tracker also the log table for debug
    personalize_events = boto3.client('personalize-events')

    current_time = int(time.time())
    utime = str(int(time.time()))



    #debug
    lastaction = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "3"}})
    lastuserid = lastaction['Item']['faceid']['S']
    lastitemid = lastaction['Item']['mymess']['S']

    if (lastuserid != userid) or (lastitemid != movieid):
        personalize_events.put_events(
            trackingId="281a4064-fdfc-46be-b169-986ee3840aa4",
            userId=userid,
            sessionId='1',

            eventList=[{
                'sentAt': current_time,
                'properties': "{\"itemId\":\"" + str(movieid) + "\"}",
                'eventType': 'CLICK',
            }]
        )

        dynamodb.put_item(
            TableName=logging_table,
            Item={
                'unixtime': {'S': "3"},
                'mymess': {'S': movieid},
                'faceid': {'S': userid}
            })




    dynamodb.put_item(
        TableName=logging_table,
        Item={
            'unixtime': {'S': str(int(utime)+20)},
            'mymess': {'S': "put_event to userid: "+ userid + "itemid: "+ movieid}
        })


def debug(Faceid, itemid):
    #debug
    lastaction = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "3"}})
    lastuserid = lastaction['Item']['faceid']['S']
    lastitemid = lastaction['Item']['mymess']['S']

    if (lastuserid != Faceid) or (lastitemid != itemid):
        return ("we haven't detect that before, so we will have put event  movieid:" + lastitemid  +"  with person: " + lastuserid)
    else:
        return ("movieid: " + lastitemid  +"  with person: " + lastuserid)
