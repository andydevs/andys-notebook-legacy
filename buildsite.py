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


def build_notebooks(site):
    """
    Build jupyter notebooks
    """
    # Create exporter
    html = nbconvert.HTMLExporter()

    # Loop through each file
    for filename in glob.glob(f'{site.notebook_dir}/*.ipynb'):
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
    # Get template
    template = site.jinja_env.get_template('index.html')

    # Notebooks array
    notebooks = glob.glob(f'{site.notebook_dir}/*.ipynb')
    notebooks = [ os.path.basename(file) for file in notebooks ]
    notebooks = [ os.path.splitext(name)[0] for name in notebooks ]

    # Render and write to file
    output = template.render(notebooks=notebooks)
    with open(f'{site.output_dir}/index.html', 'w+') as file:
        file.write(output)


def build_utility(site):
    """
    Build utility files
    """
    # Write nojekyll file
    with open(f'{site.output_dir}/.nojekyll', 'w+') as f:
        f.write('')


class Site:
    """
    Site object, handles all of the building
    """
    # Default configuration for site
    _defaults = {
        'templates_dir': 'templates',
        'notebook_dir': 'notebook',
        'output_dir': 'docs',
        'builders': [
            build_notebooks,
            build_index_page,
            build_utility
        ]
    }

    def __init__(self, **kwargs):
        """
        Initalize site object with given configuration,
        passed through **kwargs

        :see Site._defaults:
        """
        for key, value in self._defaults.items():
            setattr(self, key, kwargs.get(key, value))

    @property
    def jinja_env(self):
        """
        Return jinja2 environment for this config
        """
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(['html'])
        )

    def build(self):
        """
        Build site
        """
        self._make_directory()
        for run_builder in self.builders:
            run_builder(self)

    def _make_directory(self):
        """
        Ensure that output directory exists
        """
        if not os.path.exists(f'./{self.output_dir}'):
            os.mkdir(f'{self.output_dir}')



if __name__ == "__main__":
    my_site = Site()
    my_site.build()