from collections import defaultdict
from pymongo import MongoClient

client = "mongodb+srv://bmk802:ahdrhelqlqlqjs1!@smartq.gan6cow.mongodb.net/?retryWrites=true&w=majority"
database = "smartQ"


mongodb_client = MongoClient(client)
db = mongodb_client[database]



# login
def get_user(email):
    user = db['Users'].find_one({'email': email})
    return user

# MongoDB result insert
def insert_result(message):
    db['Results'].insert_one(message)
    return True

# create_user
def check_user(email):
    if db['Users'].find_one({'email': email}) is None:
        return False
    else:
        return True

# create_user
def insert_user(user):
    db['Users'].insert_one(dict(user))
    return True

# get inference page
def get_device_names(email):
    device_names = []
    devices = db['Devices'].find({'email': email})
    for device in devices:
        device_names.append(device['device_name'])
        
    return device_names

# get inference page
def get_group_names(email):
    group_names = []
    groups = db['Groups'].find({'email': email})
    for group in groups:
        group_names.appned(group['group_name'])
        
    return group_names

# inference
def get_models(email, model_names):
    model_list = []
    for model_name in model_names:
        model_list.append({f'{model_name}': db['Models'].find_one({'email': email, 'model_name': model_name})['onnx']})

    return model_list

# inference
def get_device_from_group(email, group_names):
    devices_list = []
    for group_name in group_names:
        group_devices = db['Groups'].find({'email': email, 'group_name': group_name})
        for group_device in group_devices:
            devices_list.append(group_device['device_name'])
            
    return devices_list

# device_register
def check_device(email, device_name):
    if db['Devices'].find_one({'email': email, 'device_name': device_name}) is None:    
        return False
    else:
        return True

# device_register
def insert_device(device):
    db['Devices'].insert_one(dict(device))
    return True

# get group_page
def get_group_dict_list(email):
    dict_list = defaultdict(list)
    groups = db['Groups'].find({'email': email})
    for group in groups:
        key = group['group_name']
        value = group['device_names']
        dict_list[key].update(value)
    
    return dict_list

# group_register
def check_group(email, group_name):
    if db['Devices'].find_one({'email': email, 'group_name': group_name}) is None:    
        return False
    else:
        return True

# group_register
def insert_group(group):
    db['Groups'].insert_one(dict(group))
    return True

# device2group
def insert_device2group(email, group_name, device_names):
    query = {'email': email, 'group_name': group_name}
    new_devices = device_names
    update = {"$addToSet": {"device_names": {"$each": new_devices}}}
    db['Groups'].update_one(query, update)
    return True

# search_all
def get_results(email):
    return db['Results'].find({'email': email})

