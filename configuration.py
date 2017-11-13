import yaml


def get_config(parameter_name):
    with open("/home/dietpi/RaspGenWithEmail/config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg['creds'][parameter_name]


def get_white_list():
    with open("/home/dietpi/RaspGenWithEmail/config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg['white_list']
