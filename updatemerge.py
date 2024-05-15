import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s')


<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
def run_command(command, capture_output=False):
    logging.info(f'Running command: {" ".join(command)}')
    if capture_output:
        result = subprocess.run(command,
                                capture_output=capture_output,
                                text=True)
        logging.info(f'Command output: {result.stdout}')
        return result
    else:
        return subprocess.run(command)
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
def run_command(command,
                check=False,
                capture_output=False,
                handle_errors=False):
    """
    Run a shell command with optional error checking, output capture, and custom error handling.
    """
    try:
        result = subprocess.run(command,
                                check=check,
                                capture_output=capture_output,
                                text=True)
        if capture_output:
            return result.stdout.strip()
        return result
    except subprocess.CalledProcessError as e:
        if handle_errors:
            handle_git_errors(e.output, command)
        raise


def handle_git_errors(output, command):
    """
    Handle common Git errors and take corrective actions.
    """
    if 'permission denied' in output.lower():
        print("Permission denied. Attempting to fork the repository...")
        if 'push' in command:
            remote_url = run_command(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True).rstrip('/')
            owner, repo = extract_owner_repo(remote_url)
            fork_repository(owner, repo)
    elif 'could not read from remote repository' in output.lower():
        print(
            "Failed to read from the remote repository. Please ensure the repository exists and you have internet access."
        )
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    """Fork a repository using the GitHub CLI."""
    try:
        run_command(["gh", "repo", "fork", f"{owner}/{repo}", "--clone=false", "--remote=true"], check=True)
    except subprocess.CalledProcessError:
        print(f"Could not fork {owner}/{repo}. It might already exist or there's another issue.")

def update_repo(fullpath):
    """Update a repository."""
    if os.path.isdir(fullpath) and ".git" in os.listdir(fullpath):
=======
    """
    Fork a repository using the GitHub CLI.
    """
    try:
=======
    """
    Fork a repository using the GitHub CLI.
    """
    try:
>>>>>>> Stashed changes
=======
    """
    Fork a repository using the GitHub CLI.
    """
    try:
>>>>>>> Stashed changes
=======
    """
    Fork a repository using the GitHub CLI.
    """
    try:
>>>>>>> Stashed changes
        run_command([
            "gh", "repo", "fork", f"{owner}/{repo}", "--clone=false",
            "--remote=true"
        ],
                    check=True)
    except subprocess.CalledProcessError:
        print(
            f"Could not fork {owner}/{repo} - it may already exist or another error occurred."
        )


def extract_owner_repo(url):
    """
    Extract the owner and repository name from a GitHub URL.
    """
    if "github.com" in url:
        parts = url.split("github.com/")[1].strip("/").split("/")
        return parts[0], parts[1].split(".git")[0]
    return None, None


def remove_duplicates_from_gitignore(gitignore_path):
    """
    Remove duplicate entries from a .gitignore file.
    """
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as file:
            lines = file.readlines()
        unique_lines = sorted(
            set(line.strip() for line in lines if line.strip()))
        with open(gitignore_path, 'w') as file:
            file.write('\n'.join(unique_lines) + '\n')


def update_repo(fullpath, is_main_directory=False):
    """
    Update a repository by stashing changes, pulling updates, and merging.
    """
    if os.path.isdir(fullpath) and os.path.exists(
            os.path.join(fullpath, '.git')):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        os.chdir(fullpath)
        run_command(["git", "stash"])
        branch = run_command(["git", "branch", "--show-current"])

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    for remote in ["origin", "upstream"]:
=======
        branch_name = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                  capture_output=True)
>>>>>>> Stashed changes
=======
        branch_name = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                  capture_output=True)
>>>>>>> Stashed changes
=======
        branch_name = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                  capture_output=True)
>>>>>>> Stashed changes
=======
        branch_name = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                  capture_output=True)
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
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

=======
        run_command(["git", "fetch", "upstream"], handle_errors=True)
        run_command(["git", "switch", branch_name])
        run_command(["git", "merge", f"upstream/{branch_name}"],
                    handle_errors=True)

        gitignore_path = os.path.join(fullpath, '.gitignore')
        remove_duplicates_from_gitignore(gitignore_path)

        run_command(["git", "add", "."])
        run_command([
            "git", "commit", "-m",
            'Auto-merge and remove duplicates from .gitignore'
        ])
        run_command(["git", "push", "origin", branch_name])

        run_command(["git", "stash", "apply"])


def verify_and_correct_remote():
    """
    Verify if the 'upstream' remote exists and add it if necessary.
    """
    remotes = run_command(["git", "remote", "-v"], capture_output=True)
    if 'upstream' not in remotes:
        origin_url = run_command(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True).rstrip('/')
        upstream_url = origin_url.replace('origin', 'upstream')
        run_command(["git", "remote", "add", "upstream", upstream_url])
        print(f"Upstream remote added with URL: {upstream_url}")


def main():
    """
    Main function to update all custom nodes and the base repository.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    custom_nodes_path = os.path.join(base_path, "custom_nodes")
    for filename in sorted(os.listdir(custom_nodes_path)):
        fullpath = os.path.join(custom_nodes_path, filename)
        update_repo(fullpath)

    update_repo(base_path, is_main_directory=True)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    run_command(["git", "submodule", "update", "--remote"])

if __name__ == "__main__":
    main()
