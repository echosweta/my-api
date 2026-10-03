# FastAPI is used to create our API
from fastapi import FastAPI

# BaseModel is used to validate incoming data
from pydantic import BaseModel

# json is used to read/write our users.json file
import json


# Create the FastAPI application
app = FastAPI()


# Model for data coming FROM the client when creating a user
# The client only needs to provide name and age
class UserCreate(BaseModel):
    name: str
    age: int


# Model representing a complete user
# A complete user also has an ID
class User(BaseModel):
    id: int
    name: str
    age: int


# Read existing users from users.json when the server starts
with open("users.json", "r") as file:
    users = json.load(file)


# Just an example list for our /LOL endpoint
lols = ["l", "doubleL"]


# --------------------------------------------------
# GET /
# --------------------------------------------------
# Basic endpoint to check if our API is working
@app.get("/")
def home():
    return {"message": "Hello World"}


# --------------------------------------------------
# GET /users
# --------------------------------------------------
# Return ALL users
@app.get("/users")
def get_users():
    return users


# --------------------------------------------------
# GET /users/{user_id}
# --------------------------------------------------
# Return ONE user based on their ID
#
# Example:
# GET /users/3
#
# FastAPI takes 3 and puts it inside user_id
@app.get("/users/{user_id}")
def get_user(user_id: int):

    # Go through every user in our users list
    for user in users:

        # Check if this user's ID matches
        # the ID requested by the client
        if user["id"] == user_id:

            # If we find the user, return it
            return user


# --------------------------------------------------
# GET /LOL
# --------------------------------------------------
# Return our example LOL list
@app.get("/LOL")
def get_LOL():
    return lols


# --------------------------------------------------
# POST /users
# --------------------------------------------------
# Create a new user
@app.post("/users")
def create_user(user: UserCreate):

    # Generate a new ID
    # len(users) tells us how many users currently exist
    # +1 gives the next ID
    new_id = len(users) + 1

    # Create the complete user object
    new_user = {
        "id": new_id,
        "name": user.name,
        "age": user.age
    }

    # Add the new user to our Python list
    users.append(new_user)

    # Save the updated list back into users.json
    with open("users.json", "w") as file:
        json.dump(users, file, indent=2)

    # Return the newly created user
    return new_user