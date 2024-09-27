import os
import sys
import subprocess
import platform

def install_dlib():
    if platform.system() != "Windows":
        print("This installer only supports Windows.")
        sys.exit(1)

    # Get Python version (major.minor) as string like '37', '38', etc.
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    
    # Define the corresponding dlib wheel files for each Python version
    whl_files = {
        "37": "wheels/dlib-19.22.99-cp37-cp37m-win_amd64.whl",
        "38": "wheels/dlib-19.22.99-cp38-cp38-win_amd64.whl",
        "39": "wheels/dlib-19.22.99-cp39-cp39-win_amd64.whl",
        "310": "wheels/dlib-19.22.99-cp310-cp310-win_amd64.whl",
        "311": "wheels/dlib-19.24.1-cp311-cp311-win_amd64.whl",
        "312": "wheels/dlib-19.24.99-cp312-cp312-win_amd64.whl",
    }

    # Check if the wheel for the current Python version is available
    if py_version in whl_files:
        whl_path = os.path.join(os.path.dirname(__file__), whl_files[py_version])
        if os.path.exists(whl_path):
            print(f"Installing dlib for Python {py_version} from {whl_path}")
            # Install the correct dlib wheel using pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", whl_path])
        else:
            print(f"Wheel file for Python {py_version} does not exist: {whl_path}")
            sys.exit(1)
    else:
        print(f"No dlib wheel file found for Python {sys.version_info.major}.{sys.version_info.minor}.")
        sys.exit(1)

def verify_installation():
    try:
        import dlib
        print("dlib installed successfully!")
    except ImportError:
        print("dlib is not installed.")
