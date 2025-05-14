from pathlib import Path
from .execute import read_one_stream_command as execute
import os
import subprocess
from urllib.parse import urlparse



def refresh_repo(url, branch_name):
    """
        + (potentially) Git clone
        + then checkout
        + git pull

    return project path
    """
    # git clone git@github.com:Strangemother/polypoint.git
    print('\n-- refresh_repo', url)
    project_path = ensure_repo(url)
    print("Directory:", project_path)
    ok = checkout_branch(project_path, branch_name)
    if ok != 0:
        print('Checkout stall.')
        return
    print('perform pull.')
    ok = git_pull(project_path, branch_name)
    print(': Pull result', ok)
    return project_path


def ensure_repo(git_url, base_dir='.'):
    """
    Clones the git repository only if it doesn't already exist.

    Args:
        git_url (str): The Git repository URL.
        base_dir (str): Base directory where repos are stored.

    Returns:
        str: Path to the local project folder.
    """
    parsed = urlparse(git_url)
    repo_name = os.path.splitext(os.path.basename(parsed.path))[0]
    project_path = Path(os.path.join(base_dir, repo_name))

    if (project_path).exists():
        print(f"Project '{repo_name}' already exists at {project_path}")
    else:
        os.makedirs(base_dir, exist_ok=True)
        print(f"Cloning {git_url} into {project_path}...")
        subprocess.run(['git', 'clone', git_url, project_path.as_posix()], check=True)

    return project_path.absolute()


def checkout_branch(project_path, branch_name):
    """
    Checks for changes and attempts to checkout the target branch.

    Args:
        project_path (str or Path): Path to the local git repository.
        branch_name (str): Target branch to checkout.
    """
    print('\n-- checkout_branch', branch_name)
    project_path = Path(project_path)

    # Check for uncommitted changes
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=project_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] git status failed: {result.stderr.strip()}")
        return -1

    if result.stdout.strip():
        print(f"[WARNING] Uncommitted changes in {project_path}. Checkout aborted.")
        return -1

    # Checkout the branch
    print(f"Checking out branch '{branch_name}' in {project_path}")
    subprocess.run(['git', 'checkout', branch_name], cwd=project_path, check=True)
    return 0

# def git_pull(project_path, branch_name):
#     """
#     Performs a git pull for the specified branch.

#     Args:
#         project_path (str or Path): Path to the local git repository.
#         branch_name (str): Target branch to pull from.
#     """
#     project_path = Path(project_path)

#     print(f"Pulling latest changes for branch '{branch_name}' in {project_path}...")
#     subprocess.run(['git', 'pull', 'origin', branch_name], cwd=project_path, check=True)


def git_pull(project_path, branch_name):
    """
    Performs a git pull for the specified branch.

    Args:
        project_path (str or Path): Path to the local git repository.
        branch_name (str): Target branch to pull from.

    Returns:
        int: 0 if successful, non-zero if an error occurred.
    """
    project_path = Path(project_path)

    print(f"Pulling latest changes for branch '{branch_name}' in {project_path}...")
    result = subprocess.run(
        ['git', 'pull', 'origin', branch_name],
        cwd=project_path
    )

    return result.returncode
