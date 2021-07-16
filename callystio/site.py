"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import yaml
import jinja2
import logging
from importlib import import_module
from .config import Configurable, load_config_file
from . import builders
from . import loaders

# Default config file name
config_file = './config.py'


class Site(Configurable):
    """
    Site object, handles all of the building
    """
    # Default configuration for site
    _config = {
        'base_url': '',
        'templates_dir': 'templates',
        'static_dir': 'static',
        'notebook_dir': 'notebook',
        'output_dir': 'dist'
    }

    # Internal loaders map
    _loaders = {
        'notebooks': loaders.NotebookLoader(),
        'statics': loaders.StaticLoader(),
        'index': loaders.MarkdownLoader(file='README.md')
    }

    # Internal builders array
    _builders = [
        builders.NotebookBuilder(),
        builders.IndexBuilder(),
        builders.StaticBuilder()
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
        self._run_loaders()
        self._run_builders()

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

    def _run_loaders(self):
        """
        Run loaders step
        """
        log = logging.getLogger('site')
        log.debug(f'Loaders: {self._loaders}')
        for name, loader in self._loaders.items():
            log.info(f'Running {loader}')
            result = loader.load(self)
            setattr(self, name, result)

    def _run_builders(self):
        """
        Run builders step
        """
        log = logging.getLogger('site')
        log.debug(f'Builders: {self._builders}')
        for builder in self._builders:
            log.info(f'Running {builder}')
            builder.build(self)



def load_site():
    """
    Load site from config file
    """
    # Get logger
    log = logging.getLogger('load_site')

    # Read config python file
    log.debug(f'Config file: {config_file}')
    if os.path.exists(config_file):
        # Read config file
        log.debug('Config file found!')
        config = load_config_file(config_file)
        log.debug(f'Config data: {config}')
        return Site(**config)
    else:
        # Default config file
        log.debug('No config file found')
        log.debug('Default config')
        return Site()