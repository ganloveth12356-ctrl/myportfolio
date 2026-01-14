@echo off
echo ===================================================
echo      STARTING AUTOMATED ONLINE DEPLOYMENT
echo ===================================================
echo.
echo 1. Installing Deployment Tool (Vercel)...
call npm install -g vercel
echo.

echo 2. Logging in...
echo    (A browser window will open. Please log in with GitHub or Email)
call vercel login
echo.

echo 3. Configuring Project...
echo    (Press ENTER to all questions to accept defaults)
echo.
call vercel
echo.

echo ===================================================
echo      DEPLOYMENT COMPLETE!
echo ===================================================
echo Your site is now online. Check the URL above.
echo.
pause
