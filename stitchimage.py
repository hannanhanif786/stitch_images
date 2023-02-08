from fastapi import APIRouter, UploadFile, Request
from typing import List
import cv2
from PIL import Image
import numpy as np 
import img2pdf
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("")
async def stitch_images(images: List[UploadFile], request: Request):

    images_data = []
    for img in images:
        img_data = await img.read()
        images_data.append(cv2.imdecode(np.frombuffer(img_data, np.uint8), -1))

    if len(images_data) == 0:
        return {"error":"no image found"}

    # Get the dimensions of the first image
    height, width, _ = images_data[0].shape

    # Check if all images have the same dimensions
    for i in range(1, len(images_data)):
        if images_data[i].shape[0] != height or images_data[i].shape[1] != width:
            return {"error": "All images should have the same dimension"}

    # Concatenate the images vertically
    concatenated_image = np.concatenate(images_data, axis=0)

    # Save the concatenated image
    img = Image.fromarray(concatenated_image)

    # Save and convert image to pdf
    pdf_path = "concatenated.pdf"
    img.save("concatenated_image.jpg")
    image = Image.open("concatenated_image.jpg")
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    print(request.url)
    return FileResponse(path=pdf_path, filename=pdf_path)
