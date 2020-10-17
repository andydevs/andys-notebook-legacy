"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import glob
import nbconvert
import logging
import markdown
from . import notebook


class Builder:
    config_vars = []

    def __repr__(self):
        config = { k:getattr(self,k) for k in self.config_vars }
        cfgstr = ', '.join(f'{k}={repr(v)}' for k,v in config.items())
        return f'{type(self).__name__}({cfgstr})'

    @property
    def log(self):
        return logging.getLogger(f'{self}.build')

    def build(self, site):
        raise NotImplementedError


class NotebookBuilder(Builder):
    def build(self, site):
        # Create exporter
        html = nbconvert.HTMLExporter(
            extra_loaders=[site.jinja_loader],
            template_file='notebook.html')
        self.log.debug(f'HTMLExporter: {repr(html)}')

        # Export notebooks
        notebooks = notebook.load_all(site)
        for nb in notebooks:
            self.log.info(f"Building '{nb.filename}'")
            nb.export(html, site)


class IndexBuilder(Builder):
    output_name = 'index.html'
    index_tamplate_name = 'index.html'

    def build(self, site):
        self.log.info(f"Building '{self.output_name}'")

        # Get template
        template = site.jinja_env.get_template(self.index_tamplate_name)

        # Get notebook data
        notebooks = notebook.load_all(site)
        notebooks = [ 
            notebook.get_notebook_data(site) 
            for notebook in notebooks ]
        self.log.debug(f'Notebooks data: {notebooks}')

        # Read README markdown file
        self.log.debug(f'Reading README.md')
        with open('README.md', 'r') as f:
            text = f.read()
        readme = markdown.markdown(text)
        self.log.debug(f'Readme: \n' + readme)

        # Render and write to file
        self.log.debug('Writing to output file')
        output = template.render(readme=readme, notebooks=notebooks)
        with open(f'{site.output_dir}/{self.output_name}', 'w+') as file:
            file.write(output)


class UtilityBuilder(Builder):
    config_vars = ['filename']

    def __init__(self, filename):
        self.filename = filename

    def build(self, site):
        self.log.info(f"Building '{self.filename}'")

        # Write nojekyll file
        outname = f'{site.output_dir}/{self.filename}'
        self.log.debug(f'Writing to {outname}')
        with open(outname, 'w+') as f:
            f.write('')