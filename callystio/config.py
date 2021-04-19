"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import logging

# Initialize logger
log = logging.getLogger('configurable')

class Configurable:
    """
    YAML configurable object with default config
    """
    _config = {}

    def __init__(self, **kwargs):
        """
        Initialize configurable with keyword args
        """
        for key, value in self._config.items():
            setattr(self, key, kwargs.get(key, value))
        log.debug(self)
        
    def __repr__(self):
        """
        String representation
        """
        cfgstr = ', '.join(
            f'{k}={repr(getattr(self,k))}' 
            for k in self._config.keys())
        return f'{type(self).__name__}({cfgstr})'


def load_config_file(path):
    """
    Load configuration file
    """
    config = {}
    with open(path) as f:
        data = f.read()
        exec(data, config)
        del config['__builtins__']
    return config