import yaml


def get_config(parameter_name):
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg['creds'][parameter_name]
