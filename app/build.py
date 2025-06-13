import PyInstaller.__main__
import os
import shutil

def build_app():
    # Clean up previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # PyInstaller configuration
    pyinstaller_args = [
        "app/main.py",  # Entry point
        "--onefile",    # Create single executable
        "--windowed",   # For GUI apps (no console)
        "--icon=assets/icon.ico",  # App icon
        "--name=TodoApp",
        "--add-data=assets;assets",  # Include assets folder
        "--add-data=data;data",      # Include data folder
        "--clean"
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)

if __name__ == "__main__":
    build_app()