import configparser
from cryptography.fernet import Fernet
from SecurePassX import config

def encrypt(password: str) -> str:
    config_file = config.CONFIG_FILE_PATH
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    key = config_parser["Security"]["key"]
    fernet = Fernet(key)
    enc_password = fernet.encrypt(password.encode()).decode()
    return enc_password


def decrypt(password: str) -> str:
    config_file = config.CONFIG_FILE_PATH
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    key = config_parser["Security"]["key"]
    fernet = Fernet(key)
    dec_password = fernet.decrypt(password).decode()
    return dec_password