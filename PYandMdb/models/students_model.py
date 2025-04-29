from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import gridfs

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]

# GridFS setup
fs = gridfs.GridFS(db)

def get_all_students():
    return list(collection.find())

def get_student_by_id(student_id):
    return collection.find_one({"_id": ObjectId(student_id)})

def add_student(data, image_file=None):
    data["date_created"] = datetime.now()
    if image_file:
        image_id = fs.put(image_file, filename=image_file.filename, content_type=image_file.content_type)
        data["image_id"] = str(image_id)
    return collection.insert_one(data)

def delete_student(student_id):
    student = get_student_by_id(student_id)
    if student and student.get("image_id"):
        try:
            fs.delete(ObjectId(student["image_id"]))
        except:
            pass
    return collection.delete_one({"_id": ObjectId(student_id)})

def update_student(student_id, data, new_image_file=None):
    student = get_student_by_id(student_id)
    if new_image_file:
        if student and student.get("image_id"):
            try:
                fs.delete(ObjectId(student["image_id"]))
            except:
                pass
        image_id = fs.put(new_image_file, filename=new_image_file.filename, content_type=new_image_file.content_type)
        data["image_id"] = str(image_id)
    return collection.update_one({"_id": ObjectId(student_id)}, {"$set": data})
