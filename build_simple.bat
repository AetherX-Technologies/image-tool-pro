@echo off
echo ========================================
echo Image Processing Tool - EXE Builder
echo ========================================
echo.

echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ImageProcessor.spec del ImageProcessor.spec

echo.
echo Starting PyInstaller...
echo.

pyinstaller --name=ImageProcessor --onefile --windowed --icon=assets\icon.ico --add-data=assets;assets --noconsole main.py

echo.
echo ========================================
if exist dist\ImageProcessor.exe (
    echo Build SUCCESS!
    echo.
    echo EXE Location: dist\ImageProcessor.exe
    echo.

    echo Creating release package...
    if exist ImageProcessor_Release rmdir /s /q ImageProcessor_Release
    mkdir ImageProcessor_Release
    copy dist\ImageProcessor.exe ImageProcessor_Release\
    copy README.md ImageProcessor_Release\ 2>nul
    copy QUICKSTART.md ImageProcessor_Release\ 2>nul

    echo.
    echo Release package created: ImageProcessor_Release\
    echo.
    echo You can distribute the ImageProcessor_Release folder!
) else (
    echo Build FAILED!
    echo Please check the error messages above.
)
echo ========================================
echo.
pause
