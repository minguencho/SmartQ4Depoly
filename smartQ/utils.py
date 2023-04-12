import os
import glob

from smartQ import rabbitmq


def img2msg(image):
    messages = []
    message = {}
    message['header'] = 'image'
    message['name'] = 'image.jpg'
    message['contents'] = image
    messages.append(message)
    
    return messages


def model_list2msg(model_list):
    messages = []
    for model_name, onnx in model_list.items():
        message = {}
        message['header'] = 'model'
        message['name'] = model_name
        message['contents'] = onnx
        messages.append(message)
        
    return messages


def make_routing_key(device_names):
    routing_keys = []
    for device_name in device_names:
        routing_keys.append(f'to{device_name}')
        
    return routing_keys


def publish_inference_message(messages, email, routing_keys):
    exchange_name = email
    for message in messages:
        for routing_key in routing_keys:
            rabbitmq.publish(message=message, exchange_name=exchange_name, routing_key_name=routing_key)
        
    return True


def check_model(email, model_name):
    user_dir = f'onnx_db/{email}'
    file_name = model_name
    model_dir = os.path.join(user_dir, file_name)
    
    if not os.path.exists(model_dir):
        return False
    else:
        return True


def write_onnx(email, model_name, model):
    user_dir = f'onnx_db/{email}'
    file_name = model_name
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        
    with open(os.path.join(user_dir, file_name), 'wb') as f:
        f.write(model)
        
    return True


def get_onnx_file(email, model_names):
    
    model_list = {}
    for model_name in model_names:
        user_dir = f'onnx_db/{email}'
        file_name = model_name
        model_dir = os.path.join(user_dir, file_name)
    
        if not os.path.exists(model_dir):
            return None
        else:
            with open(model_dir, 'rb') as f:
                model = f.read()
                model_list[model_name] = model
                
    return model_list


def get_model_name(email):
    models = glob.glob(f'onnx_db/{email}/*.onnx')
    model_name_list = []
    for model in models:
        model_tmp = model.replace(f'onnx_db/{email}/', '')
        model_name_list.append(model_tmp)
    
    return model_name_list


def result_to_list(results):
    results_list = []
    for result in results:
        result['_id'] = str(result['_id'])
        results_list.append(dict(result))
    
    return results_list
