"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import yaml
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
        'base_url': '',
        'templates_dir': 'templates',
        'notebook_dir': 'notebook',
        'output_dir': 'docs'
    }

    # Internal builders array
    _builders = [
        builders.NotebookBuilder(),
        builders.IndexBuilder(),
        builders.UtilityBuilder(filename='.nojekyll')
    ]

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
        log.debug(f'Builders: {self._builders}')
        for builder in self._builders:
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


def load_site():
    """
    Load site from config file
    """
    # Get logger
    log = logging.getLogger('load_site')

    # Read config python file
    config_file = './config.yaml'
    log.debug(f'Config file: {config_file}')
    if os.path.exists(config_file):
        log.debug('Config file found!')
        with open(config_file) as f:
            config = yaml.full_load(f)
        return Site(**config)
    else:
        log.debug('No config file found')
        log.debug('Default config')
        return Site()