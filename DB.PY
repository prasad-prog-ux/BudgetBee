from pymongo import MongoClient

# Local MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["smartfinance"]  # Your database name

# Collections
users_collection = db["users"]
dashboard_collection = db["dashboard"]
