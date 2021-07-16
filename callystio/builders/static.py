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
        log = logging.getLogger('StaticBuilder:build')

        # Write static files
        for filename, data in site.statics:
            log.info(f'Building {filename}')
            basename = os.path.basename(filename)
            outname = f'{site.output_dir}/{basename}'
            log.debug(f'Writing to {outname}')
            with open(outname, 'w+') as fout:
                fout.write(data)