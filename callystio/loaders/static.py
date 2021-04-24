"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from .loader import Loader
import logging
from glob import glob
import os


class StaticLoader(Loader):
    """
    Load static files
    """
    def load(self, site):
        """
        Load site files

        :param site: site instance
        """
        log = logging.getLogger('StaticLoader:load')

        # Read all files in static directory
        files = []
        for filename in glob(f'{site.static_dir}/*'):
            log.debug(f'Loading {filename}')
            with open(filename, 'r') as f:
                data = f.read()
            files.append((filename, data))

        # Return files
        log.info(f'Loaded {len(files)} files')
        return files