# test what will happen if we get some record it doesn't exist
import boto3

dynamodb = boto3.client('dynamodb')
videoid2 = dynamodb.get_item(TableName='logs', Key={'unixtime': {'S': "2"}})
videoid2= videoid2['Item']['mymess']['S']


print(videoid2)
#just set the record to zero, it would more easy to manage