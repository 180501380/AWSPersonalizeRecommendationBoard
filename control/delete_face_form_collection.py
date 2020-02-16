import boto3

rekognition = boto3.client('rekognition')
face_collection = "Faces"

response = rekognition.delete_faces(CollectionId=face_collection,FaceIds=["bf7e5ad0-48db-40dd-84bb-f4bd403cd530"])


print(response)