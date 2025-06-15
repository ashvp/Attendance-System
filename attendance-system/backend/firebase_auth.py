# backend/firebase_auth.py
import firebase_admin
from firebase_admin import credentials, auth
import os

base_dir = os.path.dirname(__file__)  # This points to backend/
cred_path = os.path.join(base_dir, "mpta-ymca-firebase-adminsdk-fbsvc-592c9df27b.json")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # contains email, uid, etc.
    except Exception as e:
        raise Exception("Token verification failed") from e
