import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Load your service account key JSON file path
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize the Firebase application with the credentials and database URL
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-44f6a-default-rtdb.firebaseio.com/"
})

# Reference to the 'Students' node in the Firebase Realtime Database
ref = db.reference('Students')

# Data to be updated in the database.
# This is a dictionary where each key-value pair represents a student's record.
# The key is the student ID and the value is another dictionary containing the student's details.
data = {
    "321653": {
        # Student details in key-value pairs
        "name": "Eshitaa Behal",
        "Major": "Legal Studies",
        "starting_year": 2021,
        "total_attendance": 6,
        "standing": "G",
        "Year": 3,
        "last_attendance_time": "2023-12-11 00:54:34"
    },
    "496783": {
        # Student details in key-value pairs
        "name": "Kabir Lal",
        "Major": "CS+BBA",
        "starting_year": 2022,
        "total_attendance": 9,
        "standing": "G",
        "Year": 2,
        "last_attendance_time": "2024-01-10 00:54:34"
    }
}

# Iterating over the data dictionary
for key, value in data.items():
    # For each student (key-value pair), update the student record in the Firebase Realtime Database.
    # The child method is used to reference the specific student ID node, and set method updates the student data.
    ref.child(key).set(value)
