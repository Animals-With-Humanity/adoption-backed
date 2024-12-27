import tinify
import numpy as np
from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
import io

tinify.key ="KMmB9PmRG6MG87Mmmvn2KdyNZkZYCJW8"
# Configure Cloudinary
cloudinary.config(
    cloud_name="dsm1ingy6",
    api_key="815961248834572",
    api_secret="KDnxt9IF0rUEXresLszPVwRqFhA"
)

def compress_image(file: UploadFile) -> bytes:
    # Read the file's content
    file_content = file.file.read()

    # Compress the file using TinyPNG
    compressed_content = tinify.from_buffer(file_content).to_buffer()

    return compressed_content

def upload_to_cloudinary(file: UploadFile, folder: str) -> str:
    try:
        compressed_image = compress_image(file)

        # Upload the compressed image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            compressed_image,
            folder=folder,
            resource_type="image"
        )

        # Return the secure URL of the uploaded image
        return upload_result["secure_url"]
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        raise e


def animal_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="Paltu")


def adoptor_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="Adopters")


def caretaker_upload(file: UploadFile) -> str:
    return upload_to_cloudinary(file, folder="caretaker")
