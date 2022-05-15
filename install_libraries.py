import subprocess

def create_venv():
    subprocess.run("python -m venv venv")

def install(package):
    subprocess.run("pip install " + package)

create_venv()
install('numpy')
install('cmake')
install('face_recognition')
install('opencv-python')