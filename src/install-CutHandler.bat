@echo off
ECHO 🚀 Starting CutHandler setup for Windows...

REM --- 1. Check for and install ffmpeg/ffprobe ---
ECHO Checking for ffmpeg and ffprobe...

REM 'where' is the Windows equivalent of 'command -v'
REM >nul 2>nul suppresses all output
where ffmpeg >nul 2>nul
IF %ERRORLEVEL% NEQ 0 ( GOTO install_ffmpeg )

where ffprobe >nul 2>nul
IF %ERRORLEVEL% NEQ 0 ( GOTO install_ffmpeg )

ECHO ✅ ffmpeg and ffprobe are already installed.
GOTO install_python

:install_ffmpeg
ECHO ffmpeg and/or ffprobe not found. Attempting to install...

ECHO Checking for winget...
where winget >nul 2>nul
IF %ERRORLEVEL% NEQ 0 ( GOTO winget_fail )

ECHO Attempting to install ffmpeg with winget...
winget install Gyan.FFmpeg -e --accept-source-agreements
IF %ERRORLEVEL% NEQ 0 ( GOTO ffmpeg_fail )

ECHO ffmpeg/ffprobe installed successfully.
GOTO install_python

:winget_fail
ECHO Error: The 'winget' package manager was not found.
ECHO Please install ffmpeg and ffprobe manually.
ECHO Download from: https://www.gyan.dev/ffmpeg/builds/
ECHO Then, add the 'bin' folder to your system's PATH.
GOTO :eof

:ffmpeg_fail
ECHO Error: winget failed to install ffmpeg.
ECHO Please install ffmpeg and ffprobe manually.
ECHO Download from: https://www.gyan.dev/ffmpeg/builds/
ECHO Then, add the 'bin' folder to your system's PATH.
GOTO :eof

:install_python
REM --- 2. Install Python dependencies ---
ECHO.
ECHO Installing Python packages from pyproject.toml...

IF NOT EXIST "pyproject.toml" (
    ECHO Error: pyproject.toml not found.
    GOTO :eof
)

REM Using 'py -m pip' is the most robust way to call pip on Windows
py -m pip install .
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Python package installation failed.
    GOTO :eof
)

ECHO ✅ Python packages installed successfully.

ECHO.
ECHO 🎉 Installation complete! You can now use 'cuthandler-clip' and 'cuthandler-xml' commands from your terminal.

:eof