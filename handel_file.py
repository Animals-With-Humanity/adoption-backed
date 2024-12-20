import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import os
from datetime import datetime as dt
import datetime
import requests
# Configure Cloudinary
cloudinary.config(
    cloud_name="dsm1ingy6",
    api_key="815961248834572",
    api_secret="KDnxt9IF0rUEXresLszPVwRqFhA"   
)
def animal_upload(File: UploadFile):
    try:
        # Read the file's content
        file_content = File.file

        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_content,
            folder="Paltu", 
            resource_type="auto"
        )

        # Extract the URL from the upload result
        return upload_result["secure_url"]
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        raise e
def adoptor_upload(File: UploadFile):
    try:
        # Read the file's content
        file_content = File.file

        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_content,
            folder="Adopters", 
            resource_type="auto"
        )

        # Extract the URL from the upload result
        print(upload_result)
        return upload_result["secure_url"]
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        raise e
def caretaker_upload(File: UploadFile):
    try:
        # Read the file's content
        file_content = File.file

        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_content,
            folder="caretaker", 
            resource_type="auto"
        )

        # Extract the URL from the upload result
        print(upload_result)
        return upload_result["secure_url"]
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        raise e