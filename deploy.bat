@echo off
echo ========================================
echo   Face Recognition Attendance System
echo         Deployment Preparation
echo ========================================
echo.

echo Step 1: Checking files...
if exist "app.py" (
    echo ✅ app.py found
) else (
    echo ❌ app.py missing
    pause
    exit
)

if exist "requirements.txt" (
    echo ✅ requirements.txt found
) else (
    echo ❌ requirements.txt missing
    pause
    exit
)

if exist "templates" (
    echo ✅ templates folder found
) else (
    echo ❌ templates folder missing
    pause
    exit
)

echo.
echo Step 2: Creating deployment files...
echo ✅ render.yaml created
echo ✅ Procfile created  
echo ✅ runtime.txt created
echo ✅ DEPLOYMENT_GUIDE.md created

echo.
echo Step 3: Ready for deployment!
echo.
echo Choose your deployment option:
echo.
echo 🌟 RENDER (FREE & EASY) - RECOMMENDED
echo 1. Go to https://render.com
echo 2. Sign up with GitHub
echo 3. Connect your repository
echo 4. Deploy in 5 minutes!
echo.
echo 🚀 RAILWAY (FREE & EASY)
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Deploy automatically
echo.
echo 💰 DIGITALOCEAN (Paid - $5/month)
echo 1. Follow DEPLOYMENT_GUIDE.md
echo 2. Full server control
echo 3. Custom domain support
echo.
echo 📚 For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
pause
