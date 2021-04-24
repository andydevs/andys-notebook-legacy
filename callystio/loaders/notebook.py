"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from .loader import Loader
import logging
import nbformat
from glob import glob
import os


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


class NotebookLoader(Loader):
    ext = '.ipynb'

    def load(self, site):
        """
        Load all notebooks
        """
        log = logging.getLogger('NotebookLoader:load')
        nbs = []
        for filename in glob(f'{site.notebook_dir}/*{self.ext}'):
            # Read notebook
            log.debug(f'Reading {filename}')
            with open(filename, 'r') as f:
                nb = nbformat.read(f, as_version=4)
            
            # Move filename and rootname
            nb.metadata.callystio.filename = filename
            rootname = os.path.basename(filename)
            rootname = os.path.splitext(rootname)[0]
            nb.metadata.callystio.rootname = rootname
            log.debug(f'Rootname: {nb.metadata.callystio.rootname}')

            # Move title
            if 'title' in nb.metadata:
                nb.metadata.callystio.title = nb.metadata.title
            else:
                nb.metadata.callystio.title = rootname
            log.debug(f'Title: {nb.metadata.callystio.title}')

            # Add to notebooks
            nbs.append(nb)
        
        # Return notebooks
        log.info(f'Loaded {len(nbs)} notebooks')
        return Notebooks(nbs)