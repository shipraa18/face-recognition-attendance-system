@echo off
echo ========================================
echo   GitHub Repository Setup
echo   Face Recognition Attendance System
echo ========================================
echo.

echo Step 1: Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo Please install Git from: https://git-scm.com/
    echo Then run this script again.
    pause
    exit
) else (
    echo ✅ Git is installed
)

echo.
echo Step 2: Initializing Git repository...
if exist ".git" (
    echo ✅ Git repository already exists
) else (
    git init
    echo ✅ Git repository initialized
)

echo.
echo Step 3: Adding files to Git...
git add .
echo ✅ All files added to Git

echo.
echo Step 4: Making initial commit...
git commit -m "Initial commit: Face Recognition Attendance System"
echo ✅ Initial commit created

echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Go to GitHub.com and create a new repository
echo 2. Copy the repository URL
echo 3. Run these commands in your terminal:
echo.
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Replace YOUR_REPOSITORY_URL with your actual GitHub repo URL
echo.
echo ========================================
echo.
echo Your project is ready for GitHub!
echo Run the commands above to push to GitHub.
echo.
pause
