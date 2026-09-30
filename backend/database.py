import datetime
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import streamlit as st

@st.cache_resource
def init_mongo_connection():
    try:
        if "mongo" not in st.secrets or "uri" not in st.secrets["mongo"] or "database_name" not in st.secrets["mongo"]:
            st.error("MongoDB secrets not fully configured. Check secrets.toml.")
            st.stop()
        uri = st.secrets["mongo"]["uri"]
        DB_NAME = st.secrets["mongo"]["database_name"]
        client = MongoClient(uri)
        client.admin.command('ping') 
        database = client[DB_NAME]
        return client, database 
    except Exception as e:
        st.error(f"MongoDB connection error: {e}")
        st.stop()

client, db = init_mongo_connection() 

def get_user_collection(): return db["users"] 
def get_notes_collection(): return db["notes"] 

def login_user(email, password):
    user_doc = get_user_collection().find_one({"_id": email})
    if not user_doc: return False, "User not found."
    if user_doc.get("password") == password: return True, user_doc.get("name", email)
    return False, "Invalid password."

def register_user(email, password, name):
    user_coll = get_user_collection()
    if user_coll.find_one({"_id": email}):
        return False, "User already exists with this email."
    try:
        user_coll.insert_one({
            "_id": email,
            "name": name,
            "password": password,
            "created_at": datetime.datetime.now()
        })
        return True, "Registration successful! You can now Sign In."
    except Exception as e:
        return False, f"Error: {e}"

@st.cache_data(ttl=600) 
def get_trending_notes():
    try:
        notes = list(get_notes_collection().find().sort("downloads", pymongo.DESCENDING).limit(3))
        for note in notes:
            if isinstance(note["_id"], ObjectId): note["_id"] = str(note["_id"])
        return notes
    except: return []

def get_specific_resource(subject, year, sem, resource_type, unit_num=None):
    query = {"subject": subject, "year": year, "semester": sem}
    if unit_num: query["unit"] = int(unit_num)
    try:
        return get_notes_collection().find_one(query)
    except: return None

def submit_note_feedback(note_id, user_email, feedback_text):
    if not feedback_text: return False
    new_feedback = {"user_email": user_email, "text": feedback_text, "submitted_at": datetime.datetime.now()}
    try:
        target_id = ObjectId(note_id) if isinstance(note_id, str) and len(note_id) == 24 else note_id
        result = get_notes_collection().update_one({"_id": target_id}, {"$push": {"feedback": new_feedback}})
        return result.modified_count > 0
    except: return False
