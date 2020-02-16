# import torch
#
#
# det = torch.tensor(
#     [
#         [229.00000, 230.00000, 520.00000, 425.00000,   0.98815,   0.00000],
#         [185.00000, 139.00000, 345.00000, 399.00000,   0.97173,  67.00000]
#     ]
#     , device='cuda:0')
# if type(det)== torch.Tensor:
#     print(type(det))
# else:
#     print("no")



response = {'ResponseMetadata': {'RequestId': '36f44e37-795e-4648-860a-d01003b2b5ad', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Mon, 27 Jan 2020 05:45:18 GMT', 'x-amzn-requestid': '36f44e37-795e-4648-860a-d01003b2b5ad', 'content-length': '534', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 'itemList': [{'itemId': '590'}, {'itemId': '150'}, {'itemId': '296'}, {'itemId': '318'}, {'itemId': '1'}, {'itemId': '260'}, {'itemId': '592'}, {'itemId': '780'}, {'itemId': '1198'}, {'itemId': '588'}, {'itemId': '2571'}, {'itemId': '1196'}, {'itemId': '858'}, {'itemId': '1210'}, {'itemId': '380'}, {'itemId': '527'}, {'itemId': '32'}, {'itemId': '356'}, {'itemId': '1270'}, {'itemId': '7153'}, {'itemId': '2959'}, {'itemId': '1784'}, {'itemId': '593'}, {'itemId': '457'}, {'itemId': '1721'}, {'itemId': '2028'}, {'itemId': '92259'}, {'itemId': '50'}, {'itemId': '79132'}, {'itemId': '165'}]}
response = {'CustomLabels': [{'Name': '589', 'Confidence': 88.96499633789062, 'Geometry': {'BoundingBox': {'Width': 0.26197001338005066, 'Height': 0.480459988117218, 'Left': 0.6402199864387512, 'Top': 0.3017599880695343}}}], 'ResponseMetadata': {'RequestId': '83182638-a53c-4e72-8f1c-83f3964d6fb4', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Tue, 28 Jan 2020 19:00:30 GMT', 'x-amzn-requestid': '83182638-a53c-4e72-8f1c-83f3964d6fb4', 'content-length': '199', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
response = {'CustomLabels': [], 'ResponseMetadata': {'RequestId': '06c49f02-b150-4c35-a275-6bd1d7d1f6a9', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Tue, 28 Jan 2020 19:06:20 GMT', 'x-amzn-requestid': '06c49f02-b150-4c35-a275-6bd1d7d1f6a9', 'content-length': '19', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
response = {'Item': {'unixtime': {'S': '1'}, 'mymess': {'S': 'sIFFywo_-1w'}}, 'ResponseMetadata': {'RequestId': 'P8MOAM5T7P77KPQGIA5MO5EM83VV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Wed, 29 Jan 2020 10:02:45 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '60', 'connection': 'keep-alive', 'x-amzn-requestid': 'P8MOAM5T7P77KPQGIA5MO5EM83VV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2715270222'}, 'RetryAttempts': 0}}


# if response['CustomLabels'][0]['Name']:
#     itemid = response['CustomLabels'][0]['Name']
# else:
#     itemid = None

print(response['Item']['mymess']['S'])