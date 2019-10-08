# config_loader.py
import yaml
import os

from dotenv import load_dotenv
from pathlib import Path


class Config:
    """Interact with configuration variables."""

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    __configFilePath = (os.path.join(os.getcwd(), 'config.yaml'))
    __configParser = yaml.load(open(__configFilePath), Loader=yaml.SafeLoader)

    @classmethod
    def __getenv(cls):
        """DEV or PROD"""
        # env = cls.env_config['global']['env']
        env = os.getenv("env")
        if env is '' or env is None:
            # use default value as DEV, in case env is not set
            env = 'DEV'
        return env

    @classmethod
    def get_config_val(cls, key, *args, **kwargs):
        # TODO change it to key1.key2.key3, parse the string, extract depth
        """Get prod values from config.yaml."""
        env = cls.__getenv()
        key_1depth = kwargs.get('key_1depth', None)
        key_2depth = kwargs.get('key_2depth', None)
        key_3depth = kwargs.get('key_3depth', None)
        try:
            if key_1depth is not None:
                if key_2depth is not None:
                    if key_3depth is not None:
                        return str(cls.__configParser[env][key][key_1depth][key_2depth][key_3depth])
                    else:
                        return str(cls.__configParser[env][key][key_1depth][key_2depth])
                else:
                    return str(cls.__configParser[env][key][key_1depth])
            else:
                return str(cls.__configParser[env][key])
        except Exception as e:
            print(e)
            print('invalid key structure passed for retrieving value from config.yaml')
        return None
