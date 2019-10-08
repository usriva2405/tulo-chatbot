# config_loader.py
from configparser import SafeConfigParser, ConfigParser
import os


class Config:
    """Interact with configuration variables."""

    configParser = ConfigParser()
    configFilePath = (os.path.join(os.getcwd(), 'env.ini'))

    @classmethod
    def initialize(cls):
        """Start config by reading env.ini."""
        cls.configParser.read(cls.configFilePath)

    @classmethod
    def prod(cls, key):
        """Get prod values from env.ini."""
        return cls.configParser.get('PROD', key)

    @classmethod
    def dev(cls, key):
        """Get dev values from env.ini."""
        return cls.configParser.get('DEV', key)