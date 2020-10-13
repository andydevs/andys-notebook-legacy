"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import glob
import nbformat
import nbconvert
import codecs
import logging
import markdown
import jinja2


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

    # Loop through each file
    for filename in glob.glob(f'{site.notebook_dir}/*.ipynb'):
        log.debug(f'Checking {filename}')

        # Read notebook
        log.debug('Reading notebook...')
        with open(filename) as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Get relevant metadata
        metadata = notebook.metadata.andysnb
        log.debug(f'Title: {repr(notebook.metadata.title)}')
        log.debug(f'Metadata: {repr(metadata)}')

        # Conditionally only write files that are to be published
        if metadata.get('publish', False):
            log.debug('Notebook marked for publishing!')
            log.info(f"Building '{filename}'")

            # Get output filename
            name = os.path.basename(filename)
            name = os.path.splitext(name)[0]
            outn = f'{site.output_dir}/{name}.html'
            log.debug(f"Root name '{name}'")
            log.debug(f"Output file '{outn}'")

            # Convert file
            body, _ = html.from_notebook_node(notebook)
            log.debug(f'Body size: {len(body)} bytes')

            # Write to file
            log.debug(f'Writing to {outn}')
            with open(outn, 'w+', encoding='utf-8') as out:
                out.write(body)
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

    # Get notebook
    notebooks = []
    for filename in glob.glob(f'{site.notebook_dir}/*.ipynb'):
        # Read notebook
        log.debug(f"Filename: '{filename}'")
        with open(filename, 'r') as file:
            notebook = nbformat.read(file, as_version=4)

        # Get root name and url
        rootname = os.path.basename(filename)
        rootname = os.path.splitext(rootname)[0]
        indexurl = f'{site.base_url}/{rootname}.html'
        
        # Get title
        title = notebook.metadata.title or rootname

        # Append notebook data
        notebook_data = (indexurl, title)
        log.debug(f'Notebook data: {notebook_data}')
        notebooks.append((indexurl, title))

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