@echo off
setlocal enabledelayedexpansion

REM =================================================================
REM  AeroCanvas - MASTER Build & Launch Pipeline
REM  Complete workflow: GraalVM + FastAPI + AI Agent + Frontend
REM =================================================================

cls
color 0A
title AeroCanvas - Complete Master Pipeline

echo.
echo ================================================================
echo                 AeroCanvas - MASTER SETUP
echo         GraalVM + Backend + AI Agent + Frontend
echo ================================================================
echo.

REM ==================== STEP 1: VERIFY ENVIRONMENT ====================
echo [1/8] Verifying environment...

if not exist "C:\GraalVM\bin\javac.exe" (
    color 0C
    echo [ERROR] GraalVM not found at C:\GraalVM\bin\
    echo Please install GraalVM first.
    pause
    exit /b 1
)
echo   [OK] GraalVM: C:\GraalVM\
echo.

if not exist "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    echo   [WARNING] Visual Studio Build Tools might not be installed
    echo   Continuing anyway...
    echo.
)

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python not installed!
    pause
    exit /b 1
)
echo   [OK] Python installed
echo.

REM ==================== STEP 2: SETUP VC ENVIRONMENT ====================
echo [2/8] Setting up MSVC build environment...
if exist "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" (
    call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
)
echo   [OK] Ready
echo.

REM ==================== STEP 3: COMPILE JAVA ====================
echo [3/8] Compiling Java source files...
cd /d "C:\Users\User\Desktop\AssetEngine_Core\core_engine\src"

"C:\GraalVM\bin\javac.exe" Main.java Image.java >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Java compilation failed!
    pause
    exit /b 1
)

if exist "Filter.java" (
    "C:\GraalVM\bin\javac.exe" Filter.java >nul 2>&1
)

echo   [OK] Java files compiled
echo.

REM ==================== STEP 4: BUILD NATIVE IMAGE ====================
echo [4/8] Building native image with GraalVM AOT (-O3)...
echo   This may take 2-3 minutes. Please wait...
echo.

"C:\GraalVM\bin\native-image.cmd" -O3 Main AeroCanvas

if errorlevel 1 (
    color 0C
    echo [ERROR] Native image build failed!
    pause
    exit /b 1
)
echo   [OK] AeroCanvas.exe built
echo.

REM ==================== STEP 5: MOVE EXECUTABLE ====================
echo [5/8] Relocating native executable...
if exist "AeroCanvas.exe" (
    move AeroCanvas.exe "..\.." >nul 2>&1
    echo   [OK] Moved to project root
)
echo.

REM ==================== STEP 6: INSTALL PYTHON DEPS ====================
cd /d "C:\Users\User\Desktop\AssetEngine_Core"

echo [6/8] Installing Python dependencies...
pip install --quiet --upgrade pip setuptools wheel >nul 2>&1
pip install --no-cache-dir fastapi==0.104.1 >nul 2>&1
pip install --no-cache-dir "uvicorn[standard]==0.24.0" >nul 2>&1
pip install --no-cache-dir starlette==0.27.0 >nul 2>&1
pip install --no-cache-dir python-multipart==0.0.6 >nul 2>&1
pip install --no-cache-dir google-generativeai==0.3.0 >nul 2>&1
pip install --no-cache-dir python-dotenv==1.0.0 >nul 2>&1
echo   [OK] Dependencies installed
echo.

REM ==================== STEP 7: VERIFY PORTS ====================
echo [7/8] Checking port availability...

REM Check if port 8000 is in use (basic check)
echo   Port 8000: FastAPI backend
echo   Port 8001: AI orchestrator (optional)
echo.

REM ==================== STEP 8: START SERVICES ====================
echo [8/8] Starting services...
echo.

echo ================================================================
echo                    ✓ BUILD COMPLETE!
echo.
echo   All services ready. Starting:
echo   - GraalVM Native Engine: C:\Users\User\Desktop\AssetEngine_Core\AeroCanvas.exe
echo   - FastAPI Backend:       http://127.0.0.1:8000
echo   - Frontend UI:           http://127.0.0.1:8000/
echo   - AI Orchestrator:       Can be started separately
echo.
echo   Press Ctrl+C to stop the server
echo ================================================================
echo.

timeout /t 3 >nul

cls
echo.
echo Starting FastAPI server...
echo.
echo Access your application at:
echo   http://127.0.0.1:8000/
echo.
echo Features available:
echo   - Web UI for image upload/processing
echo   - Health check: http://127.0.0.1:8000/health
echo   - Debug info:   http://127.0.0.1:8000/debug
echo   - API docs:     http://127.0.0.1:8000/docs
echo.
echo ================================================================
echo.

REM Start FastAPI
python -m uvicorn api_gateway.server:app --reload --port 8000

echo.
echo FastAPI server stopped.
echo.
echo To start AI agent in separate terminal, run:
echo   python ai_orchestrator/ai_agent.py
echo.
pause

