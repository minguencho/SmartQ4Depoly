from pymongo import MongoClient

client = "mongodb+srv://cho000130:cho41455@capstone.ajviw1n.mongodb.net/?retryWrites=true&w=majority"
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

# inference
def get_models(email, model_names):
    model_list = []
    for model_name in model_names:
        model_list.append({f'{model_name}': db['Models'].find_one({'email': email, 'model_name': model_name})['onnx']})

    return model_list

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

# model_register
def check_model(email, model_name):
    if db['Models'].find_one({'email': email, 'model_name': model_name}) is None:
        return False
    else:
        return True
    
# model_register
def insert_model(model):
    db['Models'].insert_one(dict(model))
    return True


# insert_test_data
def insert_test_data(dict):
    db['Results'].insert_one(dict)
    return True

# search_all
def get_results(email):
    return db['Results'].find({'email': email})


