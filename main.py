import os
import pickle
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

# Import necessary libraries
# os: for interacting with the operating system
# pickle: for loading and saving encoded face data
# cv2: OpenCV library for computer vision tasks
# face_recognition: for recognizing and manipulating faces
# cvzone: for creating computer vision applications easily
# firebase_admin, credentials, db, storage: for Firebase database interaction
# numpy: for numerical operations
# datetime: for working with dates and times

# Firebase configuration and initialization
cred = credentials.Certificate("serviceAccountKey.json") # Load Firebase credentials
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-44f6a-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-44f6a.appspot.com"
})
# Initialize connection to Firebase with the credentials and database/storage URL


bucket = storage.bucket()# Access the Firebase storage bucket


# Setting up the camera
cap = cv2.VideoCapture(0)  # Start video capture from the default camera
cap.set(3, 640)  # Set camera width to 640 pixels
cap.set(4, 480)  # Set camera height to 480 pixels


imgBackground = cv2.imread('Resources/background.png')  # Read a background image

# Load mode images for the UI
folderModePath = 'Resources/Modes'  # Path to the folder containing mode images
modePathList = os.listdir(folderModePath)  # List files in the mode folder
imgModeList = []  # Initialize a list to store mode images
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))  # Load each mode image and append to the list

# Load encoded face data
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')  # Open the pickle file containing face encodings
encodeListKnownWithIds = pickle.load(file)  # Load the face encodings and corresponding IDs
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds  # Separate the encodings and IDs
print("Encode File Loaded")

modeType = 0  # Variable to track the current mode of the system
counter = 0  # A counter used for timing and control in the loop
id = -1  # Variable to store the ID of the recognized student
imgStudent = []  # To store the image of the recognized student


# Main loop for face recognition and UI updates
while True:
    success, img = cap.read()  # Read a frame from the camera

    # Preprocess the image for face recognition
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resize the image to 1/4th of its original size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Convert the image from BGR to RGB color space

    # Detect faces and encode them
    faceCurFrame = face_recognition.face_locations(imgS)  # Locate faces in the current frame
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)  # Encode the detected faces

    # Update the background and mode images on the UI
    imgBackground[162:162 + 480, 55:55 + 640] = img  # Place the webcam image on the background
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType] # Place the current mode image on the background

    # Face recognition and attendance logic
    if faceCurFrame:  # Check if there are any faces in the frame
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):  # Loop through each face and its encoding
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)  # Compare current face with known faces
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # Compute distance between faces
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)  # Find the best match index

            # If there is a match with known faces
            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale the face location coordinates back to the original size
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1  # Calculate bounding box coordinates for the detected face
                imgBackground = cvzone.cornerRect(imgBackground, bbox,rt=0)  # Draw a rectangle around the detected face
                id = studentIds[matchIndex]  # Get the student ID of the recognized face

                # Attendance logic
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))  # Display 'Loading' text
                    cv2.imshow("Face Attendance", imgBackground)  # Show the updated image with the 'Loading' text
                    cv2.waitKey(1)  # Wait for a short period
                    counter = 1  # Update the counter
                    modeType = 1  # Change mode type (possibly indicating a successful face detection)

        # Further processing after a face is recognized
        if counter != 0:
            if counter == 1:
                # Retrieve student data from Firebase
                studentInfo = db.reference(f'Students/{id}').get() # Get student data from Firebase
                print(studentInfo)
                # Retrieve the student's image from Firebase storage
                blob = bucket.get_blob(f'Images/{id}.jpg') # Access the image blob from Firebase storage
                array = np.frombuffer(blob.download_as_string(), np.uint8) # Convert the blob data to a NumPy array
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR) # Decode the NumPy array to an OpenCV image


                # Attendance time check and update

                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()  # Calculate the time elapsed since the last attendance
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')  # Reference to the student's data in Firebase
                    studentInfo['total_attendance'] += 1  # Increment attendance count
                    # Update Firebase database with new attendance data
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3  # Set mode to indicate attendance already marked
                    counter = 0  # Reset counter
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Update the mode image on the UI

            # Display student information on the UI
            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2 # Change mode type (possibly for displaying different information)

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType] # Update mode image

                if counter <= 10:
                    # Displaying various pieces of student information on the background image
                    # This includes attendance count, major, ID, academic standing, year, etc.
                    # Also, resizing and displaying the student's image

                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['Major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['Year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    # Resize imgStudent
                    imgStudentResized = cv2.resize(imgStudent, (216, 216))

                    # Place the resized image into the background image
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudentResized

                counter += 1 # Increment the counter

                if counter >= 20:
                    # Reset states for next recognition
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        # Reset mode and counter if no faces are detected
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    # Display the updated background image
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1) # A short delay to allow for UI updates
