from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # Correct import for ObjectId
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/corider'

# Initialize PyMongo
mongo = PyMongo(app)

def str_to_objectid(id_str):
    """
    Convert a string to ObjectId.
    """
    try:
        return ObjectId(id_str)
    except Exception as e:
        return None
    

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


@app.route('/users/all', methods=['GET'])
def get_users():
    """
    Get all users from the database.
    """
    users = list(mongo.db.users.find())
    for user in users:
        user['_id'] = str(user['_id']) # Convert ObjectId to string
    return jsonify(users), 200


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    """
    Get a single user by ID.
    """
    obj_id = str_to_objectid(id)
    if not obj_id:
        return jsonify({"error": "Invalid ID format"}), 400
    user = mongo.db.users.find_one({"_id": obj_id})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/users/create', methods=['POST'])
def create_user():
    """
    Create a new user in the database.
    """
    data = request.json
    result = mongo.db.users.insert_one(data)
    return jsonify({result}), 201


@app.route('/users/update/<id>', methods=['PUT'])
def update_user(id):
    """
    Update an existing user by ID.
    """
    obj_id = str_to_objectid(id)
    if not obj_id:
        return jsonify({"error": "Invalid ID format"}), 400
    data = request.json
    result = mongo.db.users.replace_one({"_id": obj_id}, data)
    if result.matched_count:
        return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/users/delete/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete a user by ID.
    """
    obj_id = str_to_objectid(id)
    if not obj_id:
        return jsonify({"error": "Invalid ID format"}), 400
    result = mongo.db.users.delete_one({"_id": obj_id})
    if result.deleted_count:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
