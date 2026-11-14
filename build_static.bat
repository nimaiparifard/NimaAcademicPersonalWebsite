@echo off
setlocal
cd /d "%~dp0"
set /p SITE_URL=Public site URL (e.g. https://nima.pages.dev) [Enter = http://localhost:8000]:
if "%SITE_URL%"=="" set SITE_URL=http://localhost:8000
python manage.py check || goto :fail
python manage.py build_static --site-url %SITE_URL% || goto :fail
echo.
echo Done. Upload the "dist" folder to Cloudflare Pages / GitHub Pages.
pause
exit /b 0
:fail
echo.
echo ===== Build failed, see the error above =====
pause
exit /b 1
