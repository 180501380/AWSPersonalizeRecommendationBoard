import boto3

client = boto3.client('rekognition')

response = client.detect_custom_labels(
    ProjectVersionArn='arn:aws:rekognition:us-east-1:910854190331:project/movie4/version/movie4.2020-02-10T19.12.42/1581333159624',
    Image={
        'S3Object': {
            'Bucket': 'bucket-for-upload-frame',
            'Name': 'frame-20200211-135713.jpg'
        }
    },
    MaxResults=5,
    MinConfidence=43
)

print(response)



