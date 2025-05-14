import subprocess

import os
import venv
from pathlib import Path

def ensure_venv(project_path, env_name='env'):
    """
    Creates a Python virtual environment if it doesn't already exist.

    Args:
        project_path (str or Path): Base directory for the environment.
        env_name (str): Name of the environment directory. Default is 'env'.

    Returns:
        Path: Absolute path to the virtual environment.
    """
    env_path = (Path(project_path) / env_name).resolve()
    print('\n-- ensure_venv', project_path, ' :: folder name:', env_name)

    if env_path.exists():
        print(f"Virtual environment already exists at {env_path}")
    else:
        print(f"Creating virtual environment at {env_path}")
        venv.create(env_path, with_pip=True)

    return env_path.resolve()


def install_requirements(env_path, requirements_path=None):
    """
    Installs packages using the pip from the virtual environment.

    Args:
        env_path (str or Path): Path to the virtual environment.
        requirements_path (str or Path, optional): Path to requirements.txt.
            Defaults to 'requirements.txt' inside the project directory.

    Returns:
        int: 0 if successful, non-zero if pip fails.
    """
    print('\n-- install_requirements', env_path)
    env_path = Path(env_path)
    pip_path = env_path / 'bin' / 'pip' if os.name != 'nt' else env_path / 'Scripts' / 'pip.exe'

    if requirements_path is None:
        requirements_path = env_path.parent / 'requirements.txt'

    if not requirements_path.exists():
        print(f"[INFO] No requirements file found at {requirements_path}, skipping pip install.")
        return 0

    print(f"Installing dependencies from {requirements_path} using {pip_path}")
    result = subprocess.run(
        [str(pip_path), 'install', '-r', str(requirements_path)]
    )

    return result.returncode
