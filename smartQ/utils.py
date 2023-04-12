import os
import base64
import numpy as np
import cv2
import zlib

from smartQ import rabbitmq


def img2msg(image):
    image = image[image.find(',')+1:]
    image = np.frombuffer(base64.b64decode(image), np.uint8)
    contents = cv2.imdecode(image, cv2.IMREAD_COLOR)
    """cv2.imwrite('smartQ/images/img.jpg', image)
    with open('smartQ/images/img.jpg', 'rb') as f:
        contents = f.read()
    os.remove('smartQ/images/img.jpg')"""
    message = {}
    message['header'] = 'image'
    message['name'] = 'image.jpg'
    message['contents'] = contents
    return contents


def models2msg(models):
    messages = []
    for name, contents in models.items():
        message = {}
        message['header'] = 'model'
        message['name'] = name
        message['contents'] = contents
        messages.append(message)
        
    return messages



def make_routing_key(device_names):
    routing_keys = []
    for device_name in device_names:
        routing_keys.append(f'to{device_name}')
        
    return routing_keys


def publish_inference_message(messages, exchange_name, routing_keys):
    for message in messages:
        # model = {'model_name': resnet, 'model_contents': 1e23nfjui}
        for routing_key in routing_keys:
            rabbitmq.publish(message=message, exchange_name=exchange_name, routing_key_name=routing_key)
        
    return True

# base64 -> bytes -> numpy.ndarry -> str
def extract_onnx(onnx):
    onnx_base64_string = base64.b64encode(onnx).decode('utf-8')
    
    return onnx_base64_string


def compress_onnx(onnx):
    return zlib.compress(onnx)


def result_to_list(results):
    results_list = []
    for result in results:
        result['_id'] = str(result['_id'])
        results_list.append(dict(result))
    
    return results_list