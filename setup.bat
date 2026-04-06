@echo off
echo ============================================
echo  MetaCraft AI -- Indian Script Generator
echo  Setup Script for Windows
echo ============================================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is installed.
    pause
    exit /b 1
)

echo.
echo [2/3] Checking Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo Ollama not found. Please install from: https://ollama.com/download
    echo After installing, run this script again.
    pause
    exit /b 1
)
echo Ollama found!

echo.
echo [3/3] Pulling Qwen2.5:3b model (this downloads ~2GB, please wait)...
ollama pull qwen2.5:3b

echo.
echo ============================================
echo  Setup Complete!
echo  Run: python -m uvicorn api.main:app --reload --port 8000
echo  Then open: http://localhost:8000
echo ============================================
pause
