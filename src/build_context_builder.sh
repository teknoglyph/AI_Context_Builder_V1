#!/bin/bash
echo "Building AI Context Template Builder..."

# Install PyInstaller if not present
pip install pyinstaller

# Build GUI version
echo "Building GUI version..."
pyinstaller --onefile --windowed --name "AIContextBuilder" ai_context_builder.py

# Build CLI version
echo "Building CLI version..."
pyinstaller --onefile --name "context-cli" context_cli.py

echo ""
echo "Build complete!"
echo "GUI executable: dist/AIContextBuilder"
echo "CLI executable: dist/context-cli"
echo ""
