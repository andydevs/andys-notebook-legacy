"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import glob
import nbconvert
import codecs
import jinja2


class Config:
    """
    Configuration of site builder
    So I can keep it all in a namespace
    """
    templates_dir = 'templates'
    notebook_dir = 'notebook'
    output_dir = 'docs'

    @property
    def jinja_env(self):
        """
        Return jinja2 environment for this config
        """
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(['html'])
        )


def make_directory(config):
    """
    Ensure that directory exists
    """
    if not os.path.exists(f'./{config.output_dir}'):
        os.mkdir(f'{config.output_dir}')


def build_notebooks(config):
    """
    Build jupyter notebooks
    """
    # Create exporter
    html = nbconvert.HTMLExporter()

    # Loop through each file
    for filename in glob.glob(f'{config.notebook_dir}/*.ipynb'):
        # Get output filename
        name = os.path.basename(filename)
        name = os.path.splitext(name)[0]
        outn = f'{config.output_dir}/{name}.html'

        # Read file and convert
        body, _ = html.from_filename(filename)

        # Write to file
        # Apparently we have to encode the body
        # manually because the exporter doesn't
        # return a properly encoded body string
        encoded = codecs.encode(body, 'utf-16')
        with open(outn, 'wb+') as out:
            out.write(encoded)


def build_index_page(config):
    """
    Build index page
    """
    # Get template
    template = config.jinja_env.get_template('index.html')

    # Notebooks array
    notebooks = glob.glob(f'{config.notebook_dir}/*.ipynb')
    notebooks = [ os.path.basename(file) for file in notebooks ]
    notebooks = [ os.path.splitext(name)[0] for name in notebooks ]

    # Render and write to file
    output = template.render(notebooks=notebooks)
    with open(f'{config.output_dir}/index.html', 'w+') as file:
        file.write(output)


def build_utility(config):
    """
    Build utility files
    """
    # Write nojekyll file
    with open(f'{config.output_dir}/.nojekyll', 'w+') as f:
        f.write('')


if __name__ == "__main__":
    config = Config()
    make_directory(config)
    build_notebooks(config)
    build_index_page(config)
    build_utility(config)