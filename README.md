Facial Recognition and Attendance System

Introduction
The Facial Recognition and Attendance System is an innovative solution designed to automate and streamline the attendance process in educational and corporate environments. Leveraging the power of real-time facial recognition technology and Google's Firebase Database, this system provides a secure, efficient, and user-friendly approach to attendance management.

Features
- Real-Time Facial Recognition: Utilizes advanced algorithms to accurately detect and recognize individual faces through a standard webcam.
- Google Firebase Integration: Seamlessly connects with Firebase for robust data handling, including a Realtime Database and Firebase Storage for storing personal details and attendance records.
- User-Friendly Interface: Offers an intuitive interface displaying the video feed, recognition status, and personalized information for each recognized individual.
- Automated Attendance Logging: Automates the process of attendance logging, significantly reducing manual effort and the risk of errors.
- Privacy and Security: Prioritizes user privacy and data security, ensuring compliance with data protection regulations.

System Requirements:
A computer with a webcam.
Python 3.6 or higher.
OpenCV library.
Face Recognition library.
Firebase Admin SDK.
Stable internet connection for Firebase integration.

Installation
1. Clone the Repository:
bashCopy code
git clone [repository URL] 
2. Install Dependencies:
pip install -r requirements.txt 
3. Firebase Setup:
Set up a Firebase project and download the serviceAccountKey.json file.
Place the serviceAccountKey.json in the project root.

Usage
1. Run the System:
cssCopy code
python main.py 
2. Register Faces:
Add known face encodings to the system.
Store corresponding details in Firebase.
3. System Operation:
The system will automatically detect and recognize faces.
Attendance is logged in real-time to Firebase.

Customization
The system can be customized to handle specific requirements for different organizational environments.
Firebase database structure and storage paths can be modified as needed.

Troubleshooting
Ensure all dependencies are correctly installed.
Verify Firebase credentials and database connectivity.
Check webcam functionality if face detection is not working.

