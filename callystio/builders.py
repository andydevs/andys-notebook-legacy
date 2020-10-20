"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import glob
import nbconvert
import logging
import markdown
import os
from .config import Configurable
from . import notebook


class Builder(Configurable):
    """
    Base class for builders
    """
    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        raise NotImplementedError


class NotebookBuilder(Builder):
    """
    Handles building jupyter notebooks
    """
    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        # Get logger
        log = logging.getLogger('notebook_builder')

        # Create exporter
        html = nbconvert.HTMLExporter(
            extra_loaders=[site.jinja_loader],
            template_file='notebook.html')
        log.debug(f'HTMLExporter: {repr(html)}')

        # Export notebooks
        notebooks = notebook.load_all(site)
        for nb in notebooks:
            log.info(f"Building '{nb.filename}'")
            nb.export(html, site)


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
        notebooks = notebook.load_all(site)
        notebooks = [ 
            notebook.get_notebook_data(site) 
            for notebook in notebooks ]
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