from typing import Union
import stitchimage
from fastapi import FastAPI

app = FastAPI(title = "Image Stitiching Rnd")


app.include_router(stitchimage.router, prefix="/stitch_images")

