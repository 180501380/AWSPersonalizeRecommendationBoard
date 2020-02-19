#yolov3 detection



#for cooldowntime
import time
import datetime
time_now = datetime.datetime.now()
cooldown = datetime.datetime.now()
while True:
    if int((cooldown - time_now).total_seconds()) <= 1:
        cooldown = time_now + datetime.timedelta(seconds=11)
        time_now = datetime.datetime.now()
        print("take a picture")
    else:
        time_now = datetime.datetime.now()
        continue




##for uploading frame to s3
#import boto3
#s3 = boto3.client('s3')
# s3.upload_file('D:\main\\awsFYP\drink_coffee9.jpg', 'bucket-for-upload-frame', 'coffeetest2.jpg')