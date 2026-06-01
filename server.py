from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import shutil

app = FastAPI()

# THIS IS THE CORS FIX: It allows your HTML file to talk to your Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    with open("assets/input.ppm", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("[API] Processing...")
    subprocess.run(["./AeroCanvas.exe"], check=True)

    return {"status": "success", "output": "assets/high_res_output.ppm"}