
from pathlib import Path

import yaml
import json



class ConfSpace:
    """A super config to store assets for the deployment
    """

    # the initial directory, the cwd of the script.
    init_dir = None
    # The directory containing the config file
    config_dir = None
    config_path = None
    # The directory of source code, the root (as checked-out)
    source_dir = None

    # the deployment_assets_dir is a directory containing all
    # extra scripts etc.. for the deployment.
    deployment_assets_dir = None

    def __init__(self, **kw):
        self.__dict__.update(**kw)

    def load_app_args(self, args):
        self.app_args = args

    def load_default_config(self, config):
        self.config = config

    def load_config(self, config, path=None):
        self.config.update(config)

        if path:
            self.config_path = path
            self.config_dir = Path(path).parent

    def add_config(self, config):
        self.config.update(config)


def get_config(path_or_url):
    opt = Path(path_or_url)

    loader = get_config_data(opt)
    if loader:
        return loader

    print('unknown suffix', opt)

    if opt.is_file():
        print('a config file should be a yaml or json')
        return

    if opt.is_dir():
        get_dir = get_config_dir(opt)
        return get_dir


def get_config_dir(opt, name='pocket-deployment.yaml'):
    # assume the config is within this dir
    conf = opt.absolute() / name
    print('Assuming local config.', conf)
    conf_info = get_config_data(conf)
    if conf_info:
        print('Returning data from', conf_info)
        return conf_info
    else:
        print('No load')


def get_config_data(path_or_url):
    opt = Path(path_or_url)

    suffix = opt.suffix
    loaders = {
        ".yml": load_yaml_config,
        ".yaml": load_yaml_config,
        ".json": load_json_config,
        '.git': load_git_string,
    }

    loader = loaders.get(suffix, None)
    if loader:
        return loader(opt)

    if opt.exists() is False:
        print("file does not exist", opt)
        return

def load_git_string(path):
    return {"git_url": str(path), "git_branch": 'HEAD'}


def load_yaml_config(path):
    return yaml.safe_load(path.read_text())


def load_json_config(path):
    return json.loads(path.read_text())

