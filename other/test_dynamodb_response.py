import boto3
dynamodb = boto3.client('dynamodb')

# recommendid = 1
# item = dynamodb.get_item(TableName='movies', Key={'movieId': {'N': str(recommendid)}})

response=dynamodb.put_item(
    TableName="logs",
    Item={
        'unixtime': {'S': "2"},
        'mymess': {'S': "asd"}
    })

print(response)