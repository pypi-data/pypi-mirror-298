import json
import os
from json import JSONDecodeError
from typing import Union

from dotenv import load_dotenv
from elemental_tools.logger import Logger


# load cache into class
cache_file = './_cache/.dump'


class Cache:

    def __init__(self, file: str = cache_file):
        self.cache_file = file

        if not os.path.isdir(os.path.dirname(os.path.abspath(cache_file))):
            os.makedirs(os.path.dirname(os.path.abspath(cache_file)), exist_ok=True)

        self.cache_file_content = open(cache_file, 'a+')
        if self.cache_file_content.readlines():
            self.cache_file_content = self.load()
            try:
                data = eval(self.cache_file_content.read())
                for cache_item in data:
                    for title, value in cache_item.items():
                        setattr(self, title, value)

            except SyntaxError:
                raise Exception("Failed to parse the cache file!")

    def save(self):
        self.cache_file_content.write(
            str([{title: value for title, value in self.__dict__.items() if not title.startswith('__')}]))
        self.cache_file_content.close()
        return open(cache_file, 'a+')

    def load(self):
        return open(self.cache_file, 'a+')

    def get(self, prop):
        return getattr(self, prop, None)


class Config:
    """
    A class for managing configuration settings and persisting them to a file.

    Attributes:
        target (args):
        _debug (bool): Flag indicating whether debug mode is enabled.
        _path (str): Path to the configuration file.

    Methods:
        __init__(): Initializes the Config object by loading configuration from file.
        _dump(): Serializes the non-private attributes to JSON and writes to the config file.
        _load(): Loads configuration from the config file, or creates a new one if not found.
        update_config(**kwargs): Updates configuration settings with new values and writes them to file.
    """
    _debug: bool = True
    _path: str = os.path.join(os.path.abspath('./'), '.config')
    _log: Logger.log = Logger(app_name="Elemental-Tools", owner='config').log
    _loaded: bool = False

    def __init__(self, *target):
        """
        Initializes the Config object by loading configuration from file.

        Parameters:
            target (Union[object, callable]): Methods or Classes to bound the config.\
             So whenever the config changes, the assigned items gets propagated to its bound Methods and Classes;

        """
        self._target = target
        self._load()

    def _dump(self):
        """
        Serializes the non-private attributes to JSON and writes to the config file.
        """
        content = self._attributes()

        with open(self._path, 'w') as config_file:
            json.dump(content, config_file, indent=4)

    def __setattr__(self, key, value):

        object.__setattr__(self, key, value)
        if self._loaded:
            self._dump()

    def _load(self):
        """
        Loads configuration from the config file, or creates a new one if not found.
        """

        _path = object.__getattribute__(self, '_path')
        _dump = object.__getattribute__(self, '_dump')
        _targets = [*object.__getattribute__(self, '_target')]
        _attributes = object.__getattribute__(self, '_attributes')().items
        _log = object.__getattribute__(self, '_log')

        try:
            with open(_path, 'r') as config_file:
                try:
                    content = json.load(config_file)
                    # Assign loaded values to class attributes
                    for name, value in content.items():
                        object.__setattr__(self, name, value)

                except JSONDecodeError as json_e:
                    _dump()

        # If the file doesn't exist, dump default configuration
        except FileNotFoundError as file_e:
            _dump()

        for target in _targets:
            for attr, value in _attributes():
                try:
                    _log('info', f'Assigning Config: {attr} to {value}', origin=target)
                    object.__setattr__(target, attr, value)
                    _log('success', f'Config Assigned', origin=target)
                except AttributeError as e:
                    _log('alert', f'Failed Assigning {attr}: {str(e)}', origin=target)

        for attr, value in _attributes():
            try:
                _log('info', f'Assigning Config: {attr} to {value}')
                object.__setattr__(self, attr, value)
                _log('success', f'Config Assigned')
            except AttributeError as e:
                _log('alert', f'Failed Assigning {attr}: {str(e)}')

        object.__setattr__(self, '_loaded', True)

    def _attributes(self):
        content = {name: value for name, value in object.__getattribute__(self, '__dict__').items() if
                   not name.startswith('_') and not name == 'update_config'}
        return content

    def __getattr__(self, attr):
        self._load()
        return None

    def __getattribute__(self, item):
        object.__getattribute__(self, '_load')()
        return object.__getattribute__(self, item)


def run_cmd(command, debug: bool = False, supress: bool = True, expected_status: int = 0):
    """
    Execute batch without struggling;

    Args:
        command: The batch command you want to execute
        debug: The log must show additional info (True) or should it run on a stealth mode (False)?
        supress: The stdout must be suppressed (True), indicating no logging at command the prompt result will be placed on the console.
        expected_status: An int that may vary on different OS`s;

    Returns:
        bool: Containing the result of the validation if the command returns the expected_status;
    """

    _log = Logger(app_name="Elemental-Tools", owner='cmd').log

    if supress:
        # Redirect stdout and stderr to /dev/null
        command = f"{command} > /dev/null 2>&1"

    if debug:
        _log('info', f'Running command: {command}')
    _exec = os.system(command)

    if os.WEXITSTATUS(_exec) == expected_status:
        if debug:
            _log('success', os.WEXITSTATUS(_exec))
    else:
        if debug:
            _log('error', os.WEXITSTATUS(_exec))

    return os.WEXITSTATUS(_exec) == expected_status


class LoadEnvironmentFile:
    if os.path.isfile(os.path.join(os.getcwd(), '.env')):
        load_dotenv(os.path.join(os.getcwd(), '.env'))

    def __init__(self, env_path: str):
        load_dotenv(env_path)

    @staticmethod
    def validate():
        return True

