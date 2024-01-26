import os
import subprocess

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def update_repo(fullpath):
    git_path = os.path.join(fullpath, '.git')
    requirements_path = os.path.join(fullpath, 'requirements.txt')

    if os.path.isdir(git_path):
        print(fullpath)
        subprocess.run("git pull", shell=True, cwd=fullpath)

def update_custom_nodes():
    for filename in sorted(os.listdir(os.path.join(BASE_PATH, "custom_nodes"))):
        fullpath = os.path.join(BASE_PATH, "custom_nodes", filename)
        update_repo(fullpath)

def update_base():
    update_repo(BASE_PATH)

update_base()

update_custom_nodes()
