import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Load your Firebase service account credentials
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize the Firebase application with your credentials and configuration
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-44f6a-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-44f6a.appspot.com"
})

# Define the folder path where student images are stored
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []

# Filter out hidden files (e.g., system files that start with ".")
pathList = [filename for filename in pathList if not filename.startswith(".")]

studentIds = []
for path in pathList:
    # Read each image and append to the image list
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # Extract student ID from filename and add to the studentIds list
    studentIds.append(os.path.splitext(path)[0])

    # Upload each image to Firebase Storage
    fileName = os.path.join(folderPath, path)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

# Function to find and return encodings for a list of images
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        # Convert image to RGB as face_recognition library uses RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Encode the face present in the image
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Start the encoding process
print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
# Pairing each encoding with the corresponding student ID
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save the encodings to a file for later use
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()  # Corrected to call the close method
print("File Saved")

'''
In the context of your code, "encoding" refers to the process of converting the facial features
from an image into a numerical representation that a computer can understand and process. 
This is done by the face_recognition library, which is a popular Python library for facial recognition tasks.
'''
