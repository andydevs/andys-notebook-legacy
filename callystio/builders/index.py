"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from .builder import Builder
from .. import notebook
import os
import logging
import markdown

class IndexBuilder(Builder):
    """
    Handles building the index page
    """
    # Component configuration
    _config = {
        'output_name': 'index.html',
        'template_name': 'index.html'
    }

    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        # Get logger
        log = logging.getLogger('index_builder')
        log.info(f"Building '{self.output_name}'")

        # Get template
        template = site.jinja_env.get_template(self.template_name)

        # Get notebook data
        notebooks = site.notebooks.get_all_metadata()
        for notebook in notebooks:
            notebook.link = f'{site.base_url}/{notebook.rootname}.html'
        log.debug(f'Notebooks data: {notebooks}')

        # Read README markdown file
        log.debug(f'Reading README.md')
        with open('README.md', 'r') as f:
            text = f.read()
        readme = markdown.markdown(text)
        log.debug(f'Readme: \n' + readme)

        # Render and write to file
        log.debug('Writing to output file')
        output = template.render(readme=readme, notebooks=notebooks)
        with open(f'{site.output_dir}/{self.output_name}', 'w+') as file:
            file.write(output)