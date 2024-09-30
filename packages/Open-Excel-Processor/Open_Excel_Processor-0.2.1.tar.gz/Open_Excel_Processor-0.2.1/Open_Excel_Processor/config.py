import os
import requests
import firebase_admin
from firebase_admin import credentials, db

def download_service_account_key(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    else:
        raise Exception(f"Failed to download service account key from {url}")

def initialize_firebase(service_account_url, database_url, upload_folder='/tmp'):
    os.makedirs(upload_folder, exist_ok=True)
    service_account_path = os.path.join(upload_folder, 'serviceAccountKey.json')
    
    try:
        download_service_account_key(service_account_url, service_account_path)
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        return db.reference('/')
    except Exception as e:
        print(e)
        exit(1)

# Define your service account URL and Firebase Realtime Database URL
SERVICE_ACCOUNT_URL = 'https://mark-1-excels.s3.ap-south-1.amazonaws.com/serviceAccountKey.json'
DATABASE_URL = 'https://mark1-backup-default-rtdb.firebaseio.com'

# Initialize Firebase
firebase_ref = initialize_firebase(SERVICE_ACCOUNT_URL, DATABASE_URL)

# Firebase configuration details for REST API
apiKey = "AIzaSyBYlRzXObxn7d5oVWzgGqXhM6xaBFkXN58",
authDomain = "mark1-backup.firebaseapp.com",
databaseURL = "https://mark1-backup-default-rtdb.firebaseio.com",
projectId = "mark1-backup",
storageBucket = "mark1-backup.appspot.com",
messagingSenderId = "1070285792269",
appId = "1:1070285792269:web:8fb26aeb3cf0c158f2a144",
measurementId = "G-BSH0HVMJK8"