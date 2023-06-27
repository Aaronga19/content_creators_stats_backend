from fastapi import FastAPI, status
import json

app = FastAPI()
# ROUTERS
from users.routers import users
app.include_router(users.router)
@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

@app.get("/suma")
def read_root(number:int):
    number += 1
    return {"Tu numero": number}

@app.post("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}

@app.put("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}

@app.delete("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}

@app.patch("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}

@app.trace("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}


@app.options("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}

@app.head("/direct")
def write_root(huevos:str)->dict:
    return {"Hello": huevos}



# app = FastAPI(
#     title='Users Microservice',
#     description='This microservice manage the users and their activity',
#     version='1.0'
# )





    
