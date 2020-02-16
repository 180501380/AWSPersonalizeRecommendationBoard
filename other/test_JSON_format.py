JSON = {
  'Records': [
    {
      'eventVersion': '2.1',
      'eventSource': 'aws:s3',
      'awsRegion': 'us-east-1',
      'eventTime': '2020-01-21T08:56:10.672Z',
      'eventName': 'ObjectCreated:Put',
      'userIdentity': {
        'principalId': 'AXQ85V2ULRSHM'
      },
      'requestParameters': {
        'sourceIPAddress': '42.200.178.217'
      },
      'responseElements': {
        'x-amz-request-id': 'E63445D423FDC492',
        'x-amz-id-2': '7k0ZNFMjo6C2sUHhwN/JcKa3ximLJugg64Oq17GVBLBu1Hj5KLPTjXmTsNTabmnWCPRDFW7Nd93bYAFwLeAK9/OqcBSB1TKU'
      },
      's3': {
        's3SchemaVersion': '1.0',
        'configurationId': '88ee40b7-7046-4b62-b93a-ad6a4292aec3',
        'bucket': {
          'name': 'bucket-for-upload-frame',
          'ownerIdentity': {
            'principalId': 'AXQ85V2ULRSHM'
          },
          'arn': 'arn:aws:s3:::bucket-for-upload-frame'
        },
        'object': {
          'key': 'images/drink_coffee+-+5.jpg',
          'size': 137780,
          'eTag': 'ceeb79a7a4f3be020c9720a4d9faee2e',
          'sequencer': '005E26BCB2147AA346'
        }
      }
    }
  ]
}


print(JSON['Records'][0]['s3']['bucket']['name'])






