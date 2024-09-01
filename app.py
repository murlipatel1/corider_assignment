from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = 'mongodb://mongo:27017/user_db'

# Initialize PyMongo
mongo = PyMongo(app)

# MongoDB Schema 
def create_user_schema():
    """
    Create MongoDB schema validation for the 'users' collection.
    This ensures that documents in the 'users' collection conform to a specific structure.
    """
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "email", "password"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "Name of the user, must be a string and is required."
                },
                "email": {
                    "bsonType": "string",
                    "pattern": "^.+@.+$",
                    "description": "Email of the user, must be a string, must be in a valid email format, and is required."
                },
                "password": {
                    "bsonType": "string",
                    "description": "Password of the user, must be a string and is required."
                }
            }
        }
    }
    # Connect to the database and create the schema
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_database()
    try:
        db.command("collMod", "users", validator=schema)
    except Exception as e:
        # If the collection doesn't exist, create it with the schema
        db.create_collection("users", validator=schema)


# Utility function to convert ObjectId to string
def str_to_objectid(id_str):
    """
    Convert a string to ObjectId.
    """
    try:
        return ObjectId(id_str)
    except Exception as e:
        return None

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users from the database.
    This endpoint returns a list of all user documents from the 'users' collection.
    """
    users = list(mongo.db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(users), 200

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    """
    Get a single user by ID.
    This endpoint returns the user document with the specified ID from the 'users' collection.
    """
    obj_id = str_to_objectid(id)
    if not obj_id:
        return jsonify({"error": "Invalid ID format"}), 400
    user = mongo.db.users.find_one({"_id": obj_id})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user in the database.
    This endpoint creates a new user document in the 'users' collection.
    The password is hashed before storing for security.
    """
    data = request.json
    # Hash the password before storing
    data['password'] = generate_password_hash(data['password'])
    result = mongo.db.users.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    """
    Update an existing user by ID.
    This endpoint updates the user document with the specified ID in the 'users' collection.
    """
    obj_id = str_to_objectid(id)
    if not obj_id:
        return jsonify({"error": "Invalid ID format"}), 400
    data = request.json
    # If the password is updated, hash it before storing
    if 'password' in data:
        data['password'] = generate_password_hash(data['password'])
    result = mongo.db.users.replace_one({"_id": obj_id}, data)
    if result.matched_count:
        return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete a user by ID.
    This endpoint deletes the user document with the specified ID from the 'users' collection.
    """
    obj_id = str_to_objectid(id)
    if not obj_id:
        return jsonify({"error": "Invalid ID format"}), 400
    result = mongo.db.users.delete_one({"_id": obj_id})
    if result.deleted_count:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    # Ensure the MongoDB schema is enforced before starting the server
    create_user_schema()
    app.run(host='0.0.0.0', port=5000, debug=True)
