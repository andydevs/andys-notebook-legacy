"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import jinja2
import logging
from .config import Configurable
from . import builders


class Site(Configurable):
    """
    Site object, handles all of the building
    """
    # Default configuration for site
    _config = {
        'base_url': '/andys-notebook',
        'templates_dir': 'templates',
        'notebook_dir': 'notebook',
        'output_dir': 'docs',
        'builders': [
            builders.NotebookBuilder(),
            builders.IndexBuilder(),
            builders.UtilityBuilder(filename='.nojekyll')
        ]
    }

    @property
    def jinja_loader(self):
        """
        Return jinja2 filesystem loader for this config
        """
        return jinja2.FileSystemLoader(self.templates_dir)

    @property
    def jinja_env(self):
        """
        Return jinja2 environment for this config
        """
        return jinja2.Environment(
            loader=self.jinja_loader,
            autoescape=jinja2.select_autoescape(['html']))

    def build(self):
        """
        Build site
        """
        log = logging.getLogger('site')
        log.info('Building site.')
        self._make_directory()
        log.debug(f'Builders: {self.builders}')
        for builder in self.builders:
            log.info(f'Running {builder}')
            builder.build(self)

    def _make_directory(self):
        """
        Ensure that output directory exists
        """
        log = logging.getLogger('site')
        log.debug(f'Output Directory: {self.output_dir}')
        if os.path.exists(f'./{self.output_dir}'):
            log.info(f"'{self.output_dir}' directory exists!")
        else:
            log.info(f"Creating '{self.output_dir}' directory")
            os.mkdir(f"{self.output_dir}")