# config_loader.py
from configparser import SafeConfigParser
import os


class Config:
    """Interact with configuration variables."""

    configParser = SafeConfigParser()
    configFilePath = (os.path.join(os.getcwd(), 'config.ini'))

    @classmethod
    def initialize(cls, newhire_table):
        """Start config by reading config.ini."""
        cls.configParser.read(cls.configFilePath)

    @classmethod
    def prod(cls, key):
        """Get prod values from config.ini."""
        return cls.configParser.get('PROD', key)

    @classmethod
    def dev(cls, key):
        """Get dev values from config.ini."""
        return cls.configParser.get('DEV', key)