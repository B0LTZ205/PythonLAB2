import datetime  # At the top of your file, use this import
from models.students_model import add_student
from pymongo import MongoClient
import random
import string
import names  # You'll need to install this: pip install names
from datetime import datetime  # Import the datetime class directly

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]

# Function to generate a random date within the last 5 years
def random_date():
    # Generate random year, month, day
    year = random.randint(datetime.now().year - 5, datetime.now().year)
    month = random.randint(1, 12)
    # Adjust max day based on month
    if month in [4, 6, 9, 11]:
        max_day = 30
    elif month == 2:
        # Simple leap year check
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            max_day = 29
        else:
            max_day = 28
    else:
        max_day = 31
    
    day = random.randint(1, max_day)
    
    # Format as YYYY-MM-DD
    return f"{year}-{month:02d}-{day:02d}"

# Function to generate a random student ID
def random_student_id():
    return 'S' + ''.join(random.choices(string.digits, k=8))

# Function to generate a random email
def random_email(name):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com']
    name = name.lower().replace(' ', '.')
    return f"{name}@{random.choice(domains)}"

# Function to generate a random program
def random_program():
    programs = [
        'Computer Science', 'Information Technology', 'Software Engineering',
        'Data Science', 'Cybersecurity', 'Network Administration',
        'Business Administration', 'Marketing', 'Finance', 'Accounting',
        'Mechanical Engineering', 'Civil Engineering', 'Electrical Engineering',
        'Psychology', 'Sociology', 'Political Science', 'History',
        'Biology', 'Chemistry', 'Physics', 'Mathematics'
    ]
    return random.choice(programs)

# Generate and insert random students
def generate_random_students(count=50):
    for _ in range(count):
        name = names.get_full_name()
        student_data = {
            "studentid": random_student_id(),
            "name": name,
            "email": random_email(name),
            "program": random_program(),
            "enrollmentdate": random_date(),
            "date_created": datetime.now()  # This will work
        }
        
        # Insert the student without an image
        add_student(student_data, None)
        print(f"Added student: {student_data['name']}")

if __name__ == "__main__":
    num_students = int(input("How many random students do you want to generate? "))
    generate_random_students(num_students)
    print(f"{num_students} random students have been added to the database.")
