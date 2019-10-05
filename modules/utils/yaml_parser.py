# config_loader.py
import yaml
import os


class Config:
    """Interact with configuration variables."""

    __configFilePath = (os.path.join(os.getcwd(), 'config.yaml'))
    __configParser = yaml.load(open(__configFilePath), Loader=yaml.SafeLoader)

    @classmethod
    def prod(cls, key, *args, **kwargs):
        """Get prod values from config.yaml."""
        sub_key = kwargs.get('sub_key', None)
        sub_sub_key = kwargs.get('sub_sub_key', None)
        return cls.__generic('PROD', key, sub_key, sub_sub_key)

    @classmethod
    def dev(cls, key, *args, **kwargs):
        """Get dev values from config.yaml."""
        sub_key = kwargs.get('sub_key', None)
        sub_sub_key = kwargs.get('sub_sub_key', None)
        return cls.__generic('DEV', key, sub_key, sub_sub_key)

    @classmethod
    def __generic(cls, env, key, sub_key, sub_sub_key):
        try:
            if sub_key is not None:
                if sub_sub_key is not None:
                    return str(cls.__configParser[env][key][sub_key][sub_sub_key])
                else:
                    return str(cls.__configParser[env][key][sub_key])
            else:
                return str(cls.__configParser[env][key])
        except Exception as e:
            print(e)
            print('invalid key structure passed for retrieving value from config.yaml')
            return None
