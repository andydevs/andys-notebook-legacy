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
        extra_loaders=[jinja2.FileSystemLoader(site.templates_dir)],
        template_file='notebook.html'
    )
    log.debug(f'HTMLExporter: {repr(html)}')

    # Conditionally build each file
    for filename in glob.glob(f'{site.notebook_dir}/*.ipynb'):
        log.debug(f'Checking {repr(filename)}')
        notebook = Notebook.read(filename)
        if notebook.publish:
            log.debug('Notebook marked for publishing!')
            log.info(f"Building '{filename}'")
            notebook.export(html, site)
        else:
            log.debug('Notebook not marked for publishing!')


def build_index_page(site):
    """
    Build index page
    """
    log = logging.getLogger('build_index_page')
    log.info("Building 'index.html'")

    # Get template
    template = site.jinja_env.get_template('index.html')

    # Get notebook data
    notebooks = []
    for filename in glob.glob(f'{site.notebook_dir}/*.ipynb'):
        log.debug(f"Checking: '{filename}'")
        notebook = Notebook.read(filename)
        if notebook.publish:
            log.debug('Notebook marked for publishing!')
            notebook_data = notebook.get_notebook_data(site)
            log.debug(f'Notebook data: {notebook_data}')
            notebooks.append(notebook_data)
        else:
            log.debug('Notebook not marked for publishing!')

    # Read README markdown file
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