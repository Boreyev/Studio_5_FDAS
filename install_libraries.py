import subprocess
import sys
import os

def venv():
    subprocess.run([sys.executable, "python", "-m", "venv", "venv"])
    subprocess.run([sys.executable, "venv/", "scripts/", "Activate"])

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

venv()
install('cmake')
install('face_recognition')
install('numpy')
install('opencv-python')