from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from fastapi.security.api_key import APIKey
from fastapi import status, HTTPException, Depends
from datetime import datetime

from users.utils import password
from users.models import schemas
from users.connection.mongodb import users_collection
from users.utils.dates import age
from users.utils.oauth2 import create_access_token
from users.utils.password import verify
from users.utils.api_key import get_api_key

import json

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", status_code= status.HTTP_200_OK)
async def get_all_home(api_key:APIKey = Depends(get_api_key))->list:
    """Obtained all the users registered in data base with the password hashed.

    Args:
        api_key (APIKey, optional): Key necessary to do requests. Defaults to Depends(get_api_key).

    Returns:
        list: All the users registered in the application.
    """
    user_list = []
    users = users_collection.find({})
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return user_list


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, api_key:APIKey = Depends(get_api_key))->dict:
    """Creates a new user according with information given.

    Args:
        user (schemas.UserCreate): Information of the user that is going to be registered.
        api_key (APIKey, optional): Key necessary to do requests. Defaults to Depends(get_api_key).

    Returns:
        json: Message success
    """
    # HASH the password
    hashed_password = password.hash_password(user.password)
    user.password = hashed_password
    user.birthdate = datetime.strptime(user.birthdate, '%Y-%m-%d')
    users_collection.insert_one(jsonable_encoder(user)) 
    return {'message':'user created succesfully'}

@router.post("/login", status_code= status.HTTP_202_ACCEPTED)
async def user_login(user:schemas.GetUser, api_key:APIKey = Depends(get_api_key))->dict:
    """After do a post request with email and password, the endpoint assings a token JWT

    Args:
        user (schemas.GetUser): Credentials of the users to be able to login.
        api_key (APIKey, optional): Key necessary to do requests. Defaults to Depends(get_api_key).

    Raises:
        HTTPException: Incorrect email.
        HTTPException: Incorrect password.

    Returns:
        json: Credentials as authenticated user.
    """
    user_found = await users_collection.find_one({"email":user.email})
    if user_found != None:
       
        if verify(user.password,user_found['password']):
            user_found['_id'] = str(user_found['_id'])
            date_of_birth = datetime.strptime(user_found['birthdate'], '%Y-%m-%dT%H:%M:%S')
            user_found['age'] = age(date_of_birth)  
            user_found.pop('birthdate')
            token = create_access_token(user_found)
            user_found['token'] = token
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password, verify your data')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email does not match with any user')
    
    return user_found
