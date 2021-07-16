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
        return nbs