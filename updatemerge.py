import os
import subprocess


def update_repo(fullpath):
    git_path = os.path.join(fullpath, '.git')
    requirements_path = os.path.join(fullpath, 'requirements.txt')

    if os.path.isdir(git_path):
        os.chdir(fullpath)  # Change directory to the repository

        # Stash any local changes
        subprocess.run(["git", "stash"])

        # Get the current branch name
        branch_name = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode("utf-8")

        # Pull from the non-fork origin branch dynamically
        subprocess.run(["git", "pull", "origin", branch_name])

        # Push to the fork's origin
        subprocess.run(["git", "push", "origin", branch_name])

        # Extract and process remote URL
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"]).strip().decode("utf-8")
        if "github.com" in remote_url:  # Check if the remote URL matches GitHub format
            owner_repo = remote_url.split("github.com")[
                1].strip("/").split("/")
            owner = owner_repo[0]
            repo = owner_repo[1].split(".git")[0]

            try:
                # Fork the repository
                subprocess.run(
                    ["gh", "repo", "fork", f"{owner}/{repo}", "--clone=false", "--remote=true"], check=True)
            except subprocess.CalledProcessError:
                print(
                    f"Fork of {owner}/{repo} already exists or cannot be created.")

            # Get default branch
            default_branch_output = subprocess.check_output(
                ["git", "remote", "show", "origin"]).decode("utf-8")
            default_branch = [line for line in default_branch_output.split(
                "\n") if "HEAD branch" in line][0].split(":")[1].strip()

            # Append to .gitignore
            orig_gitignore = os.path.join(fullpath, ".gitignore")
            with open(orig_gitignore, "r") as f:
                orig_gitignore_content = f.read()
            with open(".gitignore", "a") as f:
                f.write(orig_gitignore_content)

            subprocess.run(["git", "add", ".gitignore"])  # Stage .gitignore

            # Fetch upstream changes
            subprocess.run(["git", "fetch", "upstream"])

            # Switch to default branch
            subprocess.run(["git", "switch", default_branch])

            # Merge upstream changes
            subprocess.run(["git", "merge", f"upstream/{default_branch}"])

            subprocess.run(["git", "add", "."])  # Stage all changes

            # Commit changes
            subprocess.run(
                ["git", "commit", "-m", "Auto-merge .gitignore and commit changes"])

            # Push to origin
            subprocess.run(["git", "push", "origin", default_branch])

            # Restore stashed changes
            subprocess.run(["git", "stash", "apply"])


def update_custom_nodes():
    base_path = os.path.dirname(os.path.abspath(__file__))
    custom_nodes_path = os.path.join(base_path, "custom_nodes")
    for filename in sorted(os.listdir(custom_nodes_path)):
        fullpath = os.path.join(custom_nodes_path, filename)
        update_repo(fullpath)


def update_base():
    base_path = os.path.dirname(os.path.abspath(__file__))
    update_repo(base_path)


update_base()
update_custom_nodes()
