#!/bin/bash

echo "🚀 Starting CutHandler setup..."

# --- 1. Check for and install ffmpeg ---
echo "Checking for ffmpeg..."

if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found. Attempting to install..."

    # Check for OS and use the appropriate package manager
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Error: Homebrew is not installed. Please install it to continue."
            exit 1
        fi
        echo "Installing ffmpeg with Homebrew..."
        brew install ffmpeg
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Debian/Ubuntu Linux
        echo "Installing ffmpeg with apt-get..."
        sudo apt-get update && sudo apt-get install -y ffmpeg
    else
        echo "Could not detect OS. Please install ffmpeg manually."
        exit 1
    fi

    # Verify installation
    if ! command -v ffmpeg &> /dev/null; then
        echo "ffmpeg installation failed. Please install it manually."
        exit 1
    fi
    echo "ffmpeg installed successfully."
else
    echo "✅ ffmpeg is already installed."
fi


# --- 2. Install Python dependencies ---
echo -e "\nInstalling Python packages from pyproject.toml..."

if [ -f "pyproject.toml" ]; then
    pip install .
    echo "✅ Python packages installed successfully."
else
    echo "Error: pyproject.toml not found."
    exit 1
fi

echo -e "\n🎉 Installation complete! You can now use the 'cuthandler' command."