from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()
BASE_DIR = os.path.dirname(__file__)

#default endpoint
@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(BASE_DIR,"statics","waby.html"))

