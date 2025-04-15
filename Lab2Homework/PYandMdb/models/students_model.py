from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]

def get_all_students():
    return list(collection.find())

def get_student_by_id(student_id):
    return collection.find_one({"_id": ObjectId(student_id)})

def add_student(data):
    data["date_created"] = datetime.now()
    return collection.insert_one(data)

def delete_student(student_id):
    return collection.delete_one({"_id": ObjectId(student_id)})

def update_student(student_id, data):
    return collection.update_one({"_id": ObjectId(student_id)}, {"$set": data})
