from os import getcwd, environ
from pymongo import MongoClient
from dotenv import load_dotenv

# Path to the environment file
env_path = getcwd() + "/.env"

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Create the credentials and also the URL
host = environ.get('MONGO_HOST')
user = environ.get('MONGO_USER')
password = environ.get('MONGO_PASSWORD')
port = environ.get('MONGO_PORT')
database = environ.get('MONGO_DB')

url = f'mongodb://{user}:{password}@{host}:{port}/{database}'

# Create the client
client = MongoClient(url)

print(type(client))

# Navigate to a database called api_retrieval
db_name = 'api_retrieval'

mongo_db = client[db_name]

print(type(mongo_db))

# Access a collection
collection_name = 'simple_test'

mongo_collection = mongo_db[collection_name]

print(type(mongo_collection))

# Insert data into a collection
user = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001"
    }
}

# # .insert_one() method from the collection
# mongo_collection.insert_one(document=user)

# List comprehension
many_objects = []

for i in range(10):
    
    user_copy = user.copy()
    
    user_copy['user_id'] = i

    many_objects.append(user_copy)

# print(many_objects)

# # insert_many() method from the collection
# mongo_collection.insert_many(documents=many_objects)

# Retrieve the data
mongo_objects = list(mongo_collection.find())

print(mongo_objects)
