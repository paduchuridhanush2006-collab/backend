import re
from flask_jwt_extended import create_access_token
import datetime

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

def generate_token(user_id):
    return create_access_token(identity=str(user_id), expires_delta=datetime.timedelta(days=7))

def serialize_document(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if doc and "user_id" in doc:
        doc["user_id"] = str(doc["user_id"])
    return doc
