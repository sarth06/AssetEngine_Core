import os
import subprocess
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# DIRECTORY CONFIGURATION
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace_data")

input_path = os.path.join(WORKSPACE_DIR, "input.ppm")
output_path = os.path.join(WORKSPACE_DIR, "high_res_output.ppm")
engine_path = os.path.join(BASE_DIR, "AeroCanvas.exe")

os.makedirs(WORKSPACE_DIR, exist_ok=True)
app.mount("/assets", StaticFiles(directory=WORKSPACE_DIR), name="assets")

# ---------------------------------------------------------
# PROCESS ROUTE
# ---------------------------------------------------------
@app.post("/process-image/")
async def process_image(file: UploadFile = File(...), mode: str = Form(...)):
    # 1. Save the incoming file to the workspace
    content = await file.read()
    with open(input_path, "wb") as f:
        f.write(content)

    # 2. Trigger the Native Engine
    try:
        subprocess.run([engine_path, input_path, output_path, mode], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Engine crashed: {e}")


    # 3. Return the exact JSON structure the frontend expects
    return {"status": "success", "output": "http://127.0.0.1:8000/assets/high_res_output.ppm"}