from pymongo import MongoClient

client = "mongodb+srv://bmk802:ahdrhelqlqlqjs1!@smartq.gan6cow.mongodb.net/?retryWrites=true&w=majority"
database = "smartQ"


mongodb_client = MongoClient(client)
db = mongodb_client[database]


def find_user(email):
    user = db['Users'].find_one({'email': email})
    user['_id'] = str(user['_id'])
    return user


def check_user(email):
    if db['Users'].find_one({'email': email}):
        return False
    else:
        return True


def insert_user(user):
    db['Users'].insert_one(dict(user))
    return True


def get_models(email, model_names):
    model_list = []
    for model_name in model_names:
        temp = {}
        temp['model_name'] = model_name
        temp['model_contents'] = db['Models'].find({'email': email}, {'model_name': model_name})['model_contents']
        model_list.append(temp)

    return model_list