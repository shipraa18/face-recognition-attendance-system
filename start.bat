@echo off
echo Starting Face Recognition Attendance System...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting web application...
echo.
echo Open your web browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
