import os
import subprocess


def run_command(command, check=False, capture_output=False, handle_errors=False):
    """Utility function to run a shell command with optional error checking, output capture, and custom error handling."""
    try:
        result = subprocess.run(command, check=check,
                                capture_output=capture_output, text=True)
        if capture_output:
            return result.stdout.strip()
        return result
    except subprocess.CalledProcessError as e:
        if handle_errors:
            handle_git_errors(e.output, command)
        raise


def handle_git_errors(output, command):
    """Custom error handling based on Git command output."""
    if 'permission denied' in output.lower():
        print("Permission denied. Attempting to fork the repository...")
        if 'push' in command:
            remote_url = run_command(
                ["git", "config", "--get", "remote.origin.url"], capture_output=True).rstrip('/')
            owner, repo = extract_owner_repo(remote_url)
            fork_repository(owner, repo)
    elif 'could not read from remote repository' in output.lower():
        print("Failed to read from the remote repository. Please ensure the repository exists and you have internet access.")


def fork_repository(owner, repo):
    """Attempt to fork a repository using the GitHub CLI."""
    try:
        run_command(["gh", "repo", "fork",
                    f"{owner}/{repo}", "--clone=false", "--remote=true"], check=True)
    except subprocess.CalledProcessError:
        print(
            f"Could not fork {owner}/{repo} - it may already exist or another error occurred.")


def extract_owner_repo(url):
    """Extract the owner and repository name from a GitHub URL."""
    if "github.com" in url:
        parts = url.split("github.com/")[1].strip("/").split("/")
        return parts[0], parts[0].split(".git")[0]
    return None, None


def update_repo(fullpath, is_main_directory=False):
    """Update a repository by pulling the latest changes, merging, committing, and handling forks and remotes."""
    if os.path.isdir(fullpath) and os.path.exists(os.path.join(fullpath, '.git')):
        os.chdir(fullpath)
        run_command(["git", "stash"])

        branch_name = run_command(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True)
        try:
            run_command(["git", "pull", "origin", branch_name],
                        handle_errors=True)
            run_command(["git", "push", "origin", branch_name],
                        handle_errors=True)
        except subprocess.CalledProcessError:
            pass  # Error handling is already managed within run_command

        verify_and_correct_remote()

        run_command(["git", "fetch", "upstream"], handle_errors=True)
        run_command(["git", "switch", branch_name])
        run_command(
            ["git", "merge", f"upstream/{branch_name}"], handle_errors=True)
        run_command(["git", "add", "."])
        run_command(
            ["git", "commit", "-m", 'Auto-merge .gitignore and commit changes'])
        run_command(["git", "push", "origin", branch_name])

        run_command(["git", "stash", "apply"])


def verify_and_correct_remote():
    """Verify the remotes and correct them if necessary."""
    remotes = run_command(["git", "remote", "-v"], capture_output=True)
    if 'upstream' not in remotes:
        origin_url = run_command(
            ["git", "config", "--get", "remote.origin.url"], capture_output=True).rstrip('/')
        upstream_url = origin_url.replace('origin', 'upstream')
        run_command(["git", "remote", "add", "upstream", upstream_url])
        print(f"Upstream remote added with URL: {upstream_url}")


def main():
    """Main function to update all custom nodes and the base repository."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    custom_nodes_path = os.path.join(base_path, "custom_nodes")
    for filename in sorted(os.listdir(custom_nodes_path)):
        fullpath = os.path.join(custom_nodes_path, filename)
        update_repo(fullpath)

    update_repo(base_path, is_main_directory=True)

    run_command(["git", "submodule", "update", "--remote"])


if __name__ == "__main__":
    main()
