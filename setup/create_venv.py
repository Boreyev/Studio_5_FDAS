import subprocess

def create_venv():
    subprocess.run("python -m venv venv")


def activate():
     activate_this_file = "runvenv.bat"
     exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'), dict(__file__=activate_this_file))
    #subprocess.run("./venv/scripts/activate.bat")

create_venv()
#activate()