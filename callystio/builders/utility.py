"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from .builder import Builder
import logging

class UtilityBuilder(Builder):
    """
    Builds an empty utility file of the given name,
    passed in as "filename"
    """
    # Component configuration
    _config = {
        'filename': ''
    }

    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        # Get logger
        log = logging.getLogger('utility_builder')
        log.info(f"Building '{self.filename}'")

        # Write nojekyll file
        outname = f'{site.output_dir}/{self.filename}'
        log.debug(f'Writing to {outname}')
        with open(outname, 'w+') as f:
            f.write('')