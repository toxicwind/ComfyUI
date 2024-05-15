import os
import subprocess


def run_command(command, capture_output=False):
    if capture_output:
        return subprocess.run(command,
                              capture_output=capture_output,
                              text=True)
    else:
        return subprocess.run(command)

def handle_git_error(error, command):
    """Handle common Git errors."""
    msg = error.output.lower()
    if "permission denied" in msg and "push" in command:
        remote_url = run_command(["git", "config", "--get", "remote.origin.url"])
        owner, repo = remote_url.split("github.com/")[1].rstrip("/").split("/")
        fork_repository(owner, repo)
    elif "could not read from remote repository" in msg:
        print("Remote repository not accessible. Check existence and internet connection.")
        raise error  # Re-raise the error after printing the message

def fork_repository(owner, repo):
    """Fork a repository using the GitHub CLI."""
    try:
        run_command(["gh", "repo", "fork", f"{owner}/{repo}", "--clone=false", "--remote=true"], check=True)
    except subprocess.CalledProcessError:
        print(f"Could not fork {owner}/{repo}. It might already exist or there's another issue.")

def update_repo(fullpath):
    """Update a repository."""
    if os.path.isdir(fullpath) and ".git" in os.listdir(fullpath):
        os.chdir(fullpath)
        run_command(["git", "stash"])
        branch = run_command(["git", "branch", "--show-current"])

    for remote in ["origin", "upstream"]:
        try:
            run_command(["git", "fetch", remote])
            branch_process = run_command(["git", "branch", "--show-current"],
                                         capture_output=True)
            branch = branch_process.stdout.strip(
            )  # Extract branch name as string
            run_command(["git", "merge", f"{remote}/{branch}"])
            run_command(["git", "push", remote, branch])
        except subprocess.CalledProcessError:
            pass

        with open(".gitignore", "r+") as f:
            lines = sorted(set(line.strip() for line in f if line.strip()))
            f.seek(0)
            f.write("\n".join(lines) + "\n")
            f.truncate()

        run_command(["git", "add", "."])
        run_command(["git", "commit", "-m", "Auto-update and clean .gitignore"])
        run_command(["git", "push", "origin", branch])
        run_command(["git", "stash", "apply"])

def main():
    """Main function."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    for path in [base_path, os.path.join(base_path, "custom_nodes")]:
        for filename in sorted(os.listdir(path)):
            update_repo(os.path.join(path, filename))

    run_command(["git", "submodule", "update", "--remote"])

if __name__ == "__main__":
    main()
