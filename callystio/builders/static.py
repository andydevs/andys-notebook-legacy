"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from .builder import Builder
import logging
import glob
import os

class StaticBuilder(Builder):
    """
    Copies static files into the site build
    """
    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        log = logging.getLogger('static_builder')
        log.info('Copying static files')

        # Loop through static file in the root
        for inname in glob.glob(f'{site.static_dir}/*'):
            log.debug(f'Copying {inname}')
            basename = os.path.basename(inname)
            outname = f'{site.output_dir}/{basename}'
            with open(inname, 'r') as fin, open(outname, 'w+') as fout:
                fout.write(fin.read())