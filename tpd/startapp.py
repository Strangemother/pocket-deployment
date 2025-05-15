from pprint import pprint
from pathlib import Path


from .git import refresh_repo
from .env_tool import install_requirements, ensure_venv
from .conf_tools import get_config_dir

import os

def init_start_command(cf):
    """Perform the first action from _start_. The source should be cloned of
    fetched, then perform the next actions
    """

    config = cf.config
    print('\n-- init_start_command', config)
    # check for _new_ or _continiue_
    url = config['git_url']
    if url is None:
        print('No git_url in config')
        return
    branch_name = config['git_branch']
    # Ensure the repo exists and it upto date.
    project_path = refresh_repo(url, branch_name)
    if project_path is None:
        print('Repo path is unknown')
        return

    print('getting project config')
    kw = get_config_dir(project_path)
    if kw:
        print('Appending source project config:', kw)
        cf.add_config(kw)

    print("Conf set: ", config)
    # Append the custom directory config info.
    ppp = Path(project_path)
    asset_dir = ppp / config['deployment_assets_dir']
    if asset_dir.exists():
        print('Adding assets content:', asset_dir)
    else:
        print('Assets directory does not exist:', asset_dir)
    cf.deployment_assets_dir = asset_dir
    kw = get_config_dir(asset_dir)
    if kw:
        print('Appending source/deployment config:', kw)
        cf.add_config(kw)
    config.setdefault('project_name', ppp.name)

    # Get the site-install config
    site_conf = get_site_config(cf, project_path)
    print('-- site_conf', site_conf)
    cf.add_config(site_conf)

    pprint(config)

    print('============================')

    ensure_linux_apt(cf)

    # Create env
    env_path = ppp / config['env_dir']
    env = ensure_venv(env_path, config['env_name'])

    # Requirements are dependant upon the deployment module
    assets_requirements = cf.deployment_assets_dir / config['assets_requirements_name']
    install_requirements(env, assets_requirements)


def ensure_linux_apt(cf):
    config = cf.config
    # apt
    apt = config.get('apt', {})
    if apt.get('update', False) is False:
        print('Will not perform apt update')
        return

    print('Perform apt-update')
    if apt.get('first_time_only') is False:
        # Straight to install,
        print('Perform apt installs')
        return run_apt_update()

    # Only first-time tested installs reach here.
    if config['first_time_install'] is False:
        # Is not first time,
        print('Will not perform apt update')

    print('Perform apt installs')
    return run_apt_update()


def run_apt_update():
    current_user = os.getenv('USER') or os.getlogin()

    if is_sudoer(current_user):
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            print("Update successful.")
        except subprocess.CalledProcessError as e:
            print(f"Sudo update failed: {e}")
    else:
        print(f"User '{current_user}' is not a sudoer. Cannot proceed.")


import subprocess

def is_sudoer(user):
    try:
        # Try running a harmless command with sudo -l
        result = subprocess.run(
            ['sudo', '-lU', user],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "may run the following commands" in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking sudo status: {e}")
        return False


import json

def get_site_config(cf, project_path):
    """The site config is a system specific tracking of the
    install and deployment routine. This doesn't change through
    deployments - and likely is not commited into the repo.
    """
    default = {
        "first_time_install": True,
        "platform": 'linux',
        "created_now": False,
    }

    config = cf.config
    site_conf_name = config['site_conf_name'].format(**config)
    site_conf_path = Path(project_path) / config['site_conf_dir'] / site_conf_name
    site_conf_path = site_conf_path.resolve()

    if site_conf_path.exists():
        default.update(json.loads(site_conf_path.read_text()))
    else:
        default["created_now"] = True
        site_conf_path.write_text(json.dumps(default))

    return default