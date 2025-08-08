@echo off
echo ================================
echo AI Query Assistant Setup Script
echo ================================
echo.

echo [1/6] Setting up backend environment...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
cd ..

echo.
echo [2/6] Installing frontend dependencies...
cd frontend
npm install
cd ..

echo.
echo [3/6] Creating necessary directories...
mkdir backend\models 2>nul
mkdir backend\data 2>nul

echo.
echo [4/6] Setup complete!
echo.
echo ================================
echo NEXT STEPS:
echo ================================
echo 1. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    python run.py
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    npm start
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo ================================
echo TROUBLESHOOTING:
echo ================================
echo - Make sure Python 3.8+ is installed
echo - Make sure Node.js 14+ is installed
echo - Check the README.md for detailed instructions
echo ================================
pause
