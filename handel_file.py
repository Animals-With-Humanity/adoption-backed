import cv2
import numpy as np
from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
import io
from pathlib import Path
# Configure Cloudinary
cloudinary.config(
    cloud_name="dsm1ingy6",
    api_key="815961248834572",
    api_secret="KDnxt9IF0rUEXresLszPVwRqFhA"
)

def compress_image(file: UploadFile, quality: int = 50) -> io.BytesIO:
    """
    Compress an image using OpenCV and return it as a file-like object.
    """
    # Read the uploaded file content
    file_content = file.file.read()
   
    # Convert file content to numpy array
    nparr = np.frombuffer(file_content, np.uint8)

    # Decode image from the numpy array
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Compress the image using OpenCV's imencode
    success, encoded_image = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

    if not success:
        raise ValueError("Failed to encode image")

    # Convert the compressed image to a file-like object
    return io.BytesIO(encoded_image.tobytes())

def upload_to_cloudinary(file: UploadFile, folder: str,quality:int=50) -> str:
    try:
        compressed_image = compress_image(file,quality)
        original_filename = Path(file.filename).stem
        # Upload the compressed image to Cloudinary
        upload_result = cloudinary.uploader.upload(
            compressed_image,
            folder=folder,
            resource_type="image",
             public_id=original_filename 
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
