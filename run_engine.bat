@echo off
setlocal

:: 1. Initialize MSVC Build Environment
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

:: 2. Move to source directory and compile
cd /d "C:\Users\User\Desktop\AssetEngine_Core\core_engine\src"
"C:\GraalVM\bin\javac.exe" Main.java Image.java
if %errorlevel% neq 0 (
    echo [ERROR] Java compilation failed.
    pause
    exit /b %errorlevel%
)

:: 3. Build native executable
"C:\GraalVM\bin\native-image.cmd" -O3 Main AeroCanvas
if %errorlevel% neq 0 (
    echo [ERROR] Native image build failed.
    pause
    exit /b %errorlevel%
)

:: 4. Relocate the executable to project root
move AeroCanvas.exe "..\..\"

:: 5. Launch FastAPI/Uvicorn server
cd /d "C:\Users\User\Desktop\AssetEngine_Core"
python -m uvicorn api_gateway.server:app --reload --port 8000

endlocal