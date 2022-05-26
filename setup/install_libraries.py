import subprocess


def install(package):
    subprocess.run("pip install " + package)

#create_venv()
#activate()
install('numpy')
install('cmake')
install('face_recognition')
install('opencv-python')
install('cvui')