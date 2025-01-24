from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
import io
import requests
import bcrypt
from dotenv import load_dotenv
import os
from pathlib import Path
import random
import string
import time
load_dotenv()

API_KEY=os.getenv("CLOUDINARY_KEY", "default")
API_SECRECT=os.getenv("CLOUDINARY_SECRECT", "default")
AUTH_KEY=os.getenv("AUTH_KEY_GEN","default")

# Configure Cloudinary
cloudinary.config(
    cloud_name="dsm1ingy6",
    api_key=API_KEY,
    api_secret=API_SECRECT
)

def compress_image(file: UploadFile, quality: int = 20) -> io.BytesIO:
    """
    Send the image to an external compression API and return the compressed image as a file-like object.
    """
    url = "https://awh.pythonanywhere.com/compress"

    try:
        # Prepare the file and data for the POST request
        files = {"file": (file.filename, file.file, file.content_type)}
        data = {"quality": quality}

        # Send the file to the external API
        response = requests.post(url, files=files, data=data)

        # Check if the request was successful
        if response.status_code != 200:
            raise ValueError(f"Failed to compress image: {response.text}")

        # Return the response content as a BytesIO object
        return io.BytesIO(response.content)

    except Exception as e:
        print(f"Error while compressing image: {e}")
        raise
def upload_to_cloudinary(file: UploadFile, folder: str,quality:int=50) -> str:
    try:
        #compressed_image = compress_image(file,quality)
        #time.sleep(10)
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzDDYq0vs0ZhUUYf0JYVzT96VaoHtfNDxrew&s'
        #file_content = file.file.read()
        ## Upload the compressed image to Cloudinary
        #upload_result = cloudinary.uploader.upload(
        #    file_content,
        #    folder=folder,
        #    resource_type="image"
        #)
        ## Return the secure URL of the uploaded image
        #return upload_result["secure_url"]
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        raise e

def animal_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="Paltu")


def adoptor_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="Adopters")


def caretaker_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="caretaker")

def signeture_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="signetures")


## password handelling
def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    Args:
        password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    # Convert both password and hashed password to bytes
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Verify the password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
def genrate_auth_token(auth_key: str):
    if AUTH_KEY != auth_key:
        raise ValueError("AUTH_KEY_ERROR")
    else:
        letters = string.ascii_letters  # Includes both uppercase and lowercase letters
        random_string = ''.join(random.choice(letters) for _ in range(4))
        auth_token=hash_password(random_string)
        return auth_token