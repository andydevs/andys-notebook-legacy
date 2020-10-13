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

    # Loop through each file
    for filename in glob.glob(f'{site.notebook_dir}/*.ipynb'):
        log.info(f"Building '{filename}'")

        # Get output filename
        name = os.path.basename(filename)
        name = os.path.splitext(name)[0]
        outn = f'{site.output_dir}/{name}.html'

        # Read file and convert
        body, _ = html.from_filename(filename)

        # Write to file
        with open(outn, 'w+', encoding='utf-8') as out:
            out.write(body)


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
        with open(filename, 'r') as file:
            notebook = nbformat.read(file, as_version=4)

        # Get root name and url
        rootname = os.path.basename(filename)
        rootname = os.path.splitext(rootname)[0]
        indexurl = f'{site.base_url}/{rootname}.html'
        
        # Get title
        title = notebook.metadata.title or rootname
        notebooks.append((indexurl, title))

    # Read README markdown file
    with open('README.md', 'r') as f:
        text = f.read()
    readme = markdown.markdown(text)

    # Render and write to file
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
        with open(f'{site.output_dir}/{filename}', 'w+') as f:
            f.write('')
    return build_utility_file