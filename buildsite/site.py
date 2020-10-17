"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import jinja2
import logging
from .builders import (
    NotebookBuilder,
    IndexBuilder,
    UtilityBuilder
)


class Site:
    """
    Site object, handles all of the building
    """
    # Default configuration for site
    _defaults = {
        'base_url': '/andys-notebook',
        'templates_dir': 'templates',
        'notebook_dir': 'notebook',
        'output_dir': 'docs',
        'builders': [
            NotebookBuilder(),
            IndexBuilder(),
            UtilityBuilder('.nojekyll')
        ]
    }

    def __init__(self, **kwargs):
        """
        Initalize site object with given configuration,
        passed through **kwargs

        :see Site._defaults:
        """
        log = logging.getLogger('site')
        log.debug('Initialize site')
        for key, value in self._defaults.items():
            log.debug(f"Setting key='{key}', value={repr(value)}")
            setattr(self, key, kwargs.get(key, value))
            log.debug(f"site.{key} = {repr(getattr(self, key))}")

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