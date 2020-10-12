"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import glob
import nbconvert
import codecs
import logging
import markdown


def build_notebooks(site):
    """
    Build jupyter notebooks
    """
    log = logging.getLogger('build_notebooks')

    # Create exporter
    html = nbconvert.HTMLExporter()

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
        # Apparently we have to encode the body
        # manually because the exporter doesn't
        # return a properly encoded body string
        encoded = codecs.encode(body, 'utf-16')
        with open(outn, 'wb+') as out:
            out.write(encoded)


def build_index_page(site):
    """
    Build index page
    """
    log = logging.getLogger('build_index_page')
    log.info("Building 'index.html'")

    # Get template
    template = site.jinja_env.get_template('index.html')

    # Notebooks array
    notebooks = glob.glob(f'{site.notebook_dir}/*.ipynb')
    notebooks = [ os.path.basename(file) for file in notebooks ]
    notebooks = [ os.path.splitext(name)[0] for name in notebooks ]

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