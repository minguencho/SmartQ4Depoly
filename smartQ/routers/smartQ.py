from fastapi import APIRouter, Depends, status, HTTPException, Request

from smartQ import schemas, oauth2, utils, rabbitmq, database

router = APIRouter(
    prefix="/smartQ",
    tags=['SmartQ']
)


@router.get('/')
def all(db: Request, current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.app.database["Blogs"].find({"email": current_user.email})
    list_blogs = list(blogs)
    for blog in list_blogs:
        blog['_id'] = str(blog['_id'])
    return list_blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(db: Request, request: schemas.Blog, current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = schemas.Blog(title=request.title, body=request.body) 
    dict_new_blog = dict(new_blog)
    dict_new_blog["email"] = current_user.email
    print(current_user)
    db.app.database["Blogs"].insert_one(dict_new_blog)
    return new_blog


# 아직 못함
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(db: Request, id: int, current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.app.database["Blogs"].delete_one({'email': current_user.email}, {'id': id})
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
        
    return 'done'

"""
추론
request : current_user, img_file, list(model name), list(device_name)
response : None, just do inference
"""

@router.get('/inference', status_code=status.HTTP_200_OK)
def inference(inf_data: schemas.InferenceData, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    image = utils.extract_img(inf_data.image)
    rabbitmq.publish(header='image', message=image, exchange_name='?', routing_key_name='?')

    models = database.get_models(email=current_user.email, model_names=inf_data.model_names)
    for model in models:
        # model = {'model_name': resnet, 'model_contents': 1e23nfjui}
        rabbitmq.publish(header='model', message=model, exchange_name='?', routing_key_name='?')
        
        
        
        
    return True
