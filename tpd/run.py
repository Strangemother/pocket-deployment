# run.py
from pathlib import Path
import argparse
import yaml
import json

from .conf_tools import ConfSpace, get_config, get_config_data
from .startapp import init_start_command
import os

HERE = Path(__file__).parent.absolute()
tpd_filepath = HERE / 'default-deployment.yaml'

def main():
    parser = argparse.ArgumentParser(description="Deployment Tool")
    subparsers = parser.add_subparsers(title='subcommands', dest='command', required=True)

    # `start` subcommand
    start_parser = subparsers.add_parser('start', help='Start the application')
    start_parser.add_argument('input', nargs='?', help='Optional input string')
    start_parser.set_defaults(func=start_app)

    args = parser.parse_args()
    # global conf util
    cf = ConfSpace(init_dir=os.getcwd())
    cf.load_app_args(args)
    cf.load_default_config(get_config_data(tpd_filepath))
    # run the func applied to the parser
    args.func(cf)


def start_app(cf):
    """Run the "start" app command.
    """
    path_or_url = cf.app_args.input
    if not path_or_url:
        print("No input provided.")
        path_or_url = "."
        # return
    print(f"Start app input: '{path_or_url}'")
    conf = get_config(path_or_url)
    print('start_app response conf:', conf)
    if conf:
        print('can continue')
        cf.load_config(conf, path=path_or_url)
        # startapp.
        init_start_command(cf)
    else:
        print('no config. Not continuing')
    print('end')


if __name__ == "__main__":
    main()
