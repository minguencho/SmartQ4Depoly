import pymongo
from pymongo import MongoClient
import base64
import numpy as np

client = "mongodb+srv://bmk802:ahdrhelqlqlqjs1!@smartq.gan6cow.mongodb.net/?retryWrites=true&w=majority"
database = "smartQ"


mongodb_client = MongoClient(client)
db = mongodb_client[database]



onnx_string = ''
index = 0
while True:
    onnx = db['Models'].find_one({'email': '123', 'model_name': 'res', 'index': index})
    if onnx is None:
        break
    temp = onnx['onnx']
    onnx_string += temp
    index += 10000000
    print(index)
    
onnx_string = onnx_string.encode('utf-8')
print(type(onnx_string))
print(onnx_string[:10])
with open(f'mymodel', 'wb') as f:
    f.write(onnx_string)
    