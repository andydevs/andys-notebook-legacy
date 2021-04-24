"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from ..config import Configurable
import logging
import nbformat
from glob import glob


class Notebooks:
    def __init__(self, nbs=[]):
        self.nbs = nbs

    def get_all(self, include_non_publish=False):
        """
        Get all notebooks
        """
        return [ 
            nb for nb in self.nbs 
            if nb.metadata.callystio.publish or include_non_publish ]

    def get_all_metadata(self, include_non_publish=False):
        return [
            nb.metadata.callystio
            for nb in self.nbs 
            if nb.metadata.callystio.publish or include_non_publish ]


class NotebookLoader(Configurable):
    ext = '.ipynb'

    def load(self, site):
        """
        Load all notebooks
        """
        log = logging.getLogger('NotebookLoader:load')
        log.info('Loading notebooks')
        nbs = []
        for filename in glob(f'{site.notebook_dir}/*{self.ext}'):
            log.debug(f'Reading {filename}')
            with open(filename, 'r') as f:
                nb = nbformat.read(f, as_version=4)
                nb.metadata.callystio.filename = filename
                nbs.append(nb)
        log.info(f'Loaded {len(nbs)} notebooks')
        return Notebooks(nbs)