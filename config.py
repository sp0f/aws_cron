from yaml import load, FullLoader


def get_yaml_config(configFile="config.yaml"):
    with open(configFile,"r") as file:
        configDataRaw=file.read()
    configDataYAML=load(configDataRaw,Loader=FullLoader)
    return configDataYAML

# configuration
config_data_yaml = get_yaml_config("config.yaml")

log_file_path = config_data_yaml["logging"]["log_file_path"]
log_level = config_data_yaml["logging"]["log_level"]
boto_log_level = config_data_yaml["logging"]["boto_log_level"]
