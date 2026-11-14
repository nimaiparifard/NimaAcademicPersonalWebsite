@echo off
setlocal
cd /d "%~dp0"
title Nima website - starting
set PORT=8000

echo === 1/6 Checking Python ===
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH. Install Python 3.10+ and tick "Add to PATH".
    goto :fail
)
python --version

echo.
echo === 2/6 Checking packages ===
python -c "import django, PIL, whitenoise" >nul 2>nul
if errorlevel 1 (
    echo Missing packages, installing from requirements.txt ...
    python -m pip install -r requirements.txt
    if errorlevel 1 goto :fail
) else (
    echo OK
)

echo.
echo === 3/6 Django system check ===
python manage.py check
if errorlevel 1 goto :fail

echo.
echo === 4/6 Database migrations ===
python manage.py makemigrations --check --dry-run >nul 2>nul
if errorlevel 1 (
    echo Model changes detected, creating migrations ...
    python manage.py makemigrations
    if errorlevel 1 goto :fail
)
python manage.py migrate --noinput
if errorlevel 1 goto :fail

echo.
echo === 5/6 Initial content and admin user ===
python manage.py shell -c "import sys; from core.models import SiteProfile; sys.exit(0 if SiteProfile.get() else 1)"
if errorlevel 1 (
    echo Site is empty, loading your resume data ...
    python manage.py seed_initial_data
    if errorlevel 1 goto :fail
) else (
    echo Content already loaded
)
python manage.py shell -c "import sys; from django.contrib.auth import get_user_model; sys.exit(0 if get_user_model().objects.filter(is_superuser=True).exists() else 1)"
if errorlevel 1 (
    echo No admin user yet. Create one now:
    python manage.py createsuperuser
    if errorlevel 1 goto :fail
) else (
    echo Admin user exists
)

echo.
echo === 6/6 Checking port %PORT% ===
netstat -ano | findstr /R /C:":%PORT% .*LISTENING" >nul
if not errorlevel 1 (
    echo [ERROR] Port %PORT% is already in use. Close the other server or change PORT in run.bat.
    goto :fail
)

echo.
echo All checks passed. Site:  http://127.0.0.1:%PORT%/    Admin:  http://127.0.0.1:%PORT%/admin/
echo Press Ctrl+C to stop the server.
start "" /b cmd /c "timeout /t 3 >nul & start http://127.0.0.1:%PORT%/"
title Nima website - running on port %PORT%
python manage.py runserver 127.0.0.1:%PORT%
goto :end

:fail
echo.
echo ===== Startup stopped because of the error above =====
pause
exit /b 1

:end
endlocal
