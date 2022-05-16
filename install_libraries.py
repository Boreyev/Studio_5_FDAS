import subprocess

def create_venv():
    subprocess.run("python -m venv venv")

def activate():
     activate_this_file = "venv/Scripts/activate.ps1"
     exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'), dict(__file__=activate_this_file))
    #subprocess.run("./venv/scripts/activate.bat")

def install(package):
    subprocess.run("pip install " + package)

#create_venv()
#activate()
install('numpy')
install('cmake')
install('face_recognition')
install('opencv-python')