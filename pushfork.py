import os, subprocess
from urllib.parse import urlparse, urlunparse


def run(cmd, **kwargs):
    res = subprocess.run(
        cmd, **{
            **kwargs, 'text': True,
            'capture_output': True,
            'check': True
        })
    if res.returncode != 0:
        raise Exception(f'Command {" ".join(cmd)} failed with {res.stderr}')
    return res.stdout.strip()


def change_url():
    u = urlparse(run(["git", "remote", "get-url", "origin"]))
    new_path = "/".join(
        u.path.strip('/').split('/')[:-2] + ['toxicwind'] +
        [u.path.strip('/').split('/')[-1]])
    run([
        "git", "remote", "set-url", "origin",
        urlunparse(u._replace(netloc="github.com", path=new_path))
    ])


def push(repo):
    os.chdir(repo)
    branch_name = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    change_url()
    run(["git", "push", "origin", branch_name])


def main(base):
    for r, dirs, files in os.walk(base):
        if ".git" in dirs:
            push(r)
            dirs.remove(".git")  # prevent re-traversing .git directories


if __name__ == "__main__":
    main(os.getcwd())
