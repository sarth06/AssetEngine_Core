from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import subprocess
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace_data")
os.makedirs(ASSETS_DIR, exist_ok=True)

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...), mode: str = Form("blur")):
    try:
        input_path = os.path.join(ASSETS_DIR, "input.ppm")
        engine_path = os.path.join(BASE_DIR, "AeroCanvas.exe")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # We append the 'mode' string variable right into the execution array
        result = subprocess.run([engine_path, mode], check=True, capture_output=True, text=True)
        print(f"[ENGINE STDOUT]: {result.stdout}")

        return JSONResponse(content={
            "status": "success",
            "output": "http://127.0.0.1:8000/assets/high_res_output.ppm"
        })

    except subprocess.CalledProcessError as e:
        print(f"[ENGINE ERROR]: {e.stderr}")
        raise HTTPException(status_code=500, detail="Native engine crash")
    except Exception as e:
        print(f"[SYSTEM ERROR]: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))