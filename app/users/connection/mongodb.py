import pymongo
from users.connection.secrets import settings

password= settings.database_password
user = settings.database_username
database = settings.database_name
collection = settings.database_collection

uri = f"mongodb+srv://{user}:{password}@users-content-creators.3mqesqe.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client[database]
users_collection = db[collection]

