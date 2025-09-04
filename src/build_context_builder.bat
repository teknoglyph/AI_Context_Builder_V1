@echo off
echo Building AI Context Template Builder...

REM Install PyInstaller if not present
pip install pyinstaller

REM Build GUI version
echo Building GUI version...
pyinstaller --onefile --windowed --name "AIContextBuilder" ai_context_builder.py

REM Build CLI version
echo Building CLI version...
pyinstaller --onefile --name "context-cli" context_cli.py

echo.
echo Build complete!
echo GUI executable: dist\AIContextBuilder.exe
echo CLI executable: dist\context-cli.exe
echo.
pause
