@echo off
setlocal enabledelayedexpansion

REM Start AI Orchestrator Agent in a separate terminal
REM This should be run AFTER MASTER_BUILD_AND_LAUNCH.bat

cls
color 0B
title AeroCanvas - AI Orchestrator Agent

echo.
echo ================================================================
echo                 AeroCanvas - AI Agent
echo                  (Gemini-Powered Orchestrator)
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python not installed!
    pause
    exit /b 1
)
echo [OK] Python is ready
echo.

REM Check dependencies
python -c "import google" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing google-generativeai...
    pip install google-generativeai
)
echo.

REM Navigate to project
cd /d "C:\Users\User\Desktop\AssetEngine_Core"

echo ================================================================
echo                    Starting AI Agent...
echo.
echo Press Ctrl+C to stop the agent
echo.
echo Usage:
echo   You can now interact with the AI agent to:
echo   - Process images with natural language
echo   - Convert formats (e.g., "Convert to monochrome")
echo   - Apply filters via chat interface
echo ================================================================
echo.

REM Start AI agent
python ai_orchestrator/ai_agent.py

echo.
echo AI Agent stopped.
pause

