# Flask MongoDB User Management API

This project is a simple Flask application that performs CRUD (Create, Read, Update, Delete) operations on a MongoDB database for a User resource. The application exposes REST API endpoints to manage users, where each user has the following attributes:
- `id`: A unique identifier for the user.
- `name`: The name of the user.
- `email`: The email address of the user.
- `password`: The password of the user (stored in a hashed format).

### GET /users - Returns a list of all users.
![image](https://github.com/user-attachments/assets/35d1f5cc-b243-4d67-ae53-131f2ac75ddc)


### GET /users/<id> - Returns the user with the specified ID.
![image](https://github.com/user-attachments/assets/a557caca-de64-4876-b0a8-41cc6586915e)


### POST /users - Creates a new user with the specified data.
![image](https://github.com/user-attachments/assets/ebc41cd0-47f9-496c-b212-055171505d48)

### PUT /users/<id> - Updates the user with the specified ID with the new data(where we can only pass the date which we need to update).
![image](https://github.com/user-attachments/assets/8c6d0cb4-7b11-4ffe-900c-8b300ae2d268)


### DELETE /users/<id> - Deletes the user with the specified ID.
![image](https://github.com/user-attachments/assets/50e88172-b599-4e8f-8d04-0ba601dbe50c)


## How to run the above project

### Requirements
- Python 3.7 or higher
- MongoDB (local or cloud-based)
- Docker (for containerization)

### Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/flask-mongodb-user-management.git
cd flask-mongodb-user-management
```

### 2. Install require libraries
```bash
pip install -r requirements.txt
```

### 3. In the same directory run the project
```bash
python app.py
```

### Running with Dockerfile

### 1. Pulling the Docker Image from Docker Hub
### If you prefer to pull the image directly from Docker Hub instead of building it locally, you can do so using:

```bash
docker pull murlipatel1/flask-mongodb-user-management:latest
```

### 2. Then, run the container:

```bash
docker run -d -p 5000:5000 --name flask-mongodb-app murlipatel1/flask-mongodb-user-management:latest
```
### Accessing the Application
### 3. Once the container is running, the application will be accessible at http://localhost:5000.