import os.path
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.yml')
with open(config_path, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def get_config(parameter_name):
    return cfg['creds'][parameter_name]


def get_white_list():
    return cfg['white_list']


def get_pin():
    return cfg['pin']