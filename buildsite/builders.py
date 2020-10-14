"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import glob
import nbconvert
import logging
import markdown
import jinja2
from .notebook import Notebook


def build_notebooks(site):
    """
    Build jupyter notebooks
    """
    log = logging.getLogger('build_notebooks')

    # Create exporter
    html = nbconvert.HTMLExporter(
        extra_loaders=[site.jinja_loader],
        template_file='notebook.html')
    log.debug(f'HTMLExporter: {repr(html)}')

    # Export notebooks
    notebooks = Notebook.load_all(site)
    for notebook in notebooks:
        log.info(f"Building '{notebook.filename}'")
        notebook.export(html, site)


def build_index_page(site):
    """
    Build index page
    """
    log = logging.getLogger('build_index_page')
    log.info("Building 'index.html'")

    # Get template
    template = site.jinja_env.get_template('index.html')

    # Get notebook data
    notebooks = Notebook.load_all(site)
    notebooks = [ notebook.get_notebook_data(site) for notebook in notebooks ]
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
    with open(f'{site.output_dir}/index.html', 'w+') as file:
        file.write(output)


def build_utility(filename):
    """
    Return builder that just writes an empty file
    with the given filename
    """
    def build_utility_file(site):
        log = logging.getLogger(f"build_utility('{filename}')")
        log.info(f"Building '{filename}'")

        # Write nojekyll file
        outname = f'{site.output_dir}/{filename}'
        log.debug(f'Writing to {outname}')
        with open(outname, 'w+') as f: f.write('')
    return build_utility_file