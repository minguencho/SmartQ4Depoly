from pymongo import MongoClient

client = "mongodb+srv://bmk802:ahdrhelqlqlqjs1!@smartq.gan6cow.mongodb.net/?retryWrites=true&w=majority"
database = "smartQ"


mongodb_client = MongoClient(client)
db = mongodb_client[database]


def find_user(email):
    user = db['Users'].find_one({'email': email})
    print(user)
    return user

# create_user
def check_user(email):
    if db['Users'].find_one({'email': email}):
        return True
    else:
        return False

# create_user
def insert_user(user):
    db['Users'].insert_one(dict(user))
    return True

# inference
def get_models(email, model_names):
    model_list = []
    for model_name in model_names:
        model_list.append({f'{model_name}': db['Models'].find({'email': email}, {'model_name': model_name})['model_contents']})

    return model_list

# device_register
def check_device(email, device_name):
    if db['Devices'].find_one({'email': email}, {'device_name': device_name}):
        return True
    else:
        return False

# device_register
def insert_device(device):
    db['Devices'].insert_one(dict(device))
    return True

# my_model_register
def check_my_model(email, my_model_name):
    if db['Models'].find_one({'email': email}, {'my_model_name': my_model_name}):
        return True
    else:
        return False
    
# my_model_register
def insert_my_model(my_model):
    db['Models'].insert_one(dict(my_model))
    return True