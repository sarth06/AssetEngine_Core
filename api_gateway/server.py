import os
import subprocess
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="AeroCanvas API Gateway")

# Custom exception handler for parsing errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return {"status": "error", "detail": f"Request validation error: {str(exc)}"}

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
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

input_path = os.path.join(WORKSPACE_DIR, "input.ppm")
output_path = os.path.join(WORKSPACE_DIR, "high_res_output.ppm")
engine_path = os.path.join(BASE_DIR, "AeroCanvas.exe")

os.makedirs(WORKSPACE_DIR, exist_ok=True)

# Mount workspace assets
app.mount("/assets", StaticFiles(directory=WORKSPACE_DIR), name="assets")

# ---------------------------------------------------------
# FRONTEND ROUTE
# ---------------------------------------------------------
@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file"""
    frontend_file = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(frontend_file):
        raise HTTPException(status_code=404, detail="Frontend not found")

    with open(frontend_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# ---------------------------------------------------------
# HEALTH CHECK ROUTE
# ---------------------------------------------------------
@app.get("/health")
async def health_check():
    """Check API gateway health"""
    engine_exists = os.path.exists(engine_path)
    return {
        "status": "healthy",
        "engine_available": engine_exists,
        "workspace_ready": os.path.exists(WORKSPACE_DIR),
        "workspace_path": WORKSPACE_DIR,
        "engine_path": engine_path
    }

# ---------------------------------------------------------
# DEBUG ROUTE
# ---------------------------------------------------------
@app.get("/debug")
async def debug_info():
    """Get debug information"""
    return {
        "base_dir": BASE_DIR,
        "workspace_dir": WORKSPACE_DIR,
        "frontend_dir": FRONTEND_DIR,
        "input_path": input_path,
        "output_path": output_path,
        "engine_path": engine_path,
        "engine_exists": os.path.exists(engine_path),
        "workspace_exists": os.path.exists(WORKSPACE_DIR),
        "input_exists": os.path.exists(input_path),
        "output_exists": os.path.exists(output_path),
        "workspace_files": os.listdir(WORKSPACE_DIR) if os.path.exists(WORKSPACE_DIR) else []
    }

# ---------------------------------------------------------
# PROCESS ROUTE
# ---------------------------------------------------------
@app.post("/process-image/")
async def process_image(file: UploadFile = File(...), mode: str = Form(...)):
    """
    Process an uploaded PPM image with the specified filter mode.
    Modes: blur, invert, grayscale, sharpen, edge
    """
    logger.info(f"Received file: {file.filename}, mode: {mode}")

    # Validate mode
    valid_modes = ["blur", "invert", "grayscale", "sharpen", "edge"]
    if mode not in valid_modes:
        logger.error(f"Invalid mode: {mode}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode. Allowed: {', '.join(valid_modes)}"
        )

    # Validate engine exists
    if not os.path.exists(engine_path):
        logger.error(f"Engine not found at: {engine_path}")
        raise HTTPException(
            status_code=500,
            detail="Native engine (AeroCanvas.exe) not found. Please rebuild the native image."
        )

    try:
        # 1. Save the incoming file to the workspace
        logger.info(f"Reading file: {file.filename}")
        content = await file.read()
        logger.info(f"File size: {len(content)} bytes")

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        with open(input_path, "wb") as f:
            f.write(content)
        logger.info(f"Saved to: {input_path}")

        # 2. Trigger the Native Engine
        logger.info(f"Executing engine with mode: {mode}")
        result = subprocess.run(
            [engine_path, input_path, output_path, mode],
            check=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        logger.info(f"Engine output: {result.stdout}")

        # 3. Verify output was created
        if not os.path.exists(output_path):
            logger.error("Output file was not created by engine")
            raise HTTPException(
                status_code=500,
                detail="Engine executed but failed to generate output file"
            )

        output_size = os.path.getsize(output_path)
        logger.info(f"Output file created: {output_size} bytes")

        # 4. Return the exact JSON structure the frontend expects
        return {
            "status": "success",
            "output": f"http://127.0.0.1:8000/assets/high_res_output.ppm"
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Engine error: {e.stderr}")
        raise HTTPException(
            status_code=500,
            detail=f"Engine crashed: {e.stderr or e.stdout or str(e)}"
        )
    except subprocess.TimeoutExpired:
        logger.error("Engine processing timeout")
        raise HTTPException(
            status_code=500,
            detail="Engine processing timeout (>30 seconds)"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )

# ---------------------------------------------------------
# STARTUP EVENT
# ---------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("=" * 50)
    logger.info("🚀 FastAPI Gateway Starting...")
    logger.info(f"📁 Workspace: {WORKSPACE_DIR}")
    logger.info(f"🎯 Engine: {engine_path}")
    logger.info(f"✓ Engine available: {os.path.exists(engine_path)}")
    logger.info(f"✓ Workspace exists: {os.path.exists(WORKSPACE_DIR)}")
    logger.info("=" * 50)
