#get the itemid by personalize

import boto3
response={'CustomLabels': [{'Name': '589', 'Confidence': 88.96499633789062, 'Geometry': {'BoundingBox': {'Width': 0.26197001338005066, 'Height': 0.480459988117218, 'Left': 0.6402199864387512, 'Top': 0.3017599880695343}}}], 'ResponseMetadata': {'RequestId': 'c8ecea8e-5367-4fd8-b97e-cd5091f940b1', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Sun, 26 Jan 2020 11:36:48 GMT', 'x-amzn-requestid': 'c8ecea8e-5367-4fd8-b97e-cd5091f940b1', 'content-length': '199', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}

faceid = "532153"

print(response['CustomLabels'][0]['Name'])

client = boto3.client('personalize-runtime', region_name='us-east-1')

response = client.get_recommendations(
    campaignArn="arn:aws:personalize:us-east-1:910854190331:campaign/sims",
    itemId='589',
    userId=faceid,
    numResults=1
)

print(response["itemList"][0]["itemId"]) #only need one recommend


#query dynamodb table to get the moviename of this itemid
item = dynamodb.get_item(TableName='movies', Key={'movieId': {'S': str(movieid)}})

# Gets the item
face_id = item['Item']['title']['S']










# #query this movie ,its trailer
# from tmdbv3api import TMDb
#
# tmdb = TMDb()
# tmdb.api_key = '550aefcd2d348445784d813a310f7efc'
# tmdb.language = 'en'
# tmdb.debug = True
# from tmdbv3api import Movie
#
# moviename = "terminator 2"
# moviedetail = Movie().search(moviename)
#
#
# trailernameinyoutube = "http://api.themoviedb.org/3/movie/"+str(movieid)"/videos?api_key=550aefcd2d348445784d813a310f7efc"