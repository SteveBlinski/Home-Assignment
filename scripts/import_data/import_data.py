import pymongo
import pandas as pd
import os


mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
target_db_name = os.getenv("TARGET_DB_NAME")

atlas_username = os.getenv("ATLAS_USERNAME")
atlas_password = os.getenv("ATLAS_PASSWORD")

target_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{target_db_name}"
atlas_uri = f"mongodb+srv://{atlas_username}:{atlas_password}@cluster0.aiwcg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

atlas_client = pymongo.MongoClient(atlas_uri)
atlas_db = atlas_client["sample_training"]
atlas_collection = atlas_db["posts"]

data = list(atlas_collection.find())
df = pd.json_normalize(data)

target_client = pymongo.MongoClient(target_uri)
target_db = target_client["sample_training"]
target_collection = target_db["posts"]

target_collection.delete_many({})

target_collection.insert_many(df.to_dict("records"))

print("Export from Atlas and import to MongoDB completed.")
