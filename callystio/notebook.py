"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import glob
import nbformat
import nbconvert
import logging


class Notebook:
    """
    Handles loading and exporting individual notebooks
    """
    ext = '.ipynb'

    def __init__(self, nb, filename=''):
        """
        Initialize notebook

        :param nb: notebook node data
        :param filename: name of file read from if there is one
        """
        self._nb = nb
        self._filename = filename
        log = logging.getLogger('notebook:Notebook#__init__')
        log.debug(f"Filename: '{self._filename}'")
        log.debug(f"Rootname: '{self.rootname}'")
        log.debug(f"Title: '{self.title}'")
        log.debug(f'Metadata: {repr(self.metadata)}')

    def __repr__(self):
        """
        Notebook string representation
        """
        return f'Notebook(filename="{self._filename}")'

    @property
    def filename(self):
        """
        Filename of notebook
        """
        return self._filename

    @property
    def rootname(self):
        """
        Base name of file minus extension
        """
        name = os.path.basename(self._filename)
        return os.path.splitext(name)[0]

    @property
    def title(self):
        """
        Notebook title
        """
        return self._nb.metadata.get('title', self.rootname)

    @property
    def metadata(self):
        """
        Relevant notebook metadata
        """
        return self._nb.metadata.andysnb

    @property
    def publish(self):
        """
        True if the notebook is to be published
        """
        return self.metadata.get('publish', False)

    def get_output_filename(self, site):
        """
        Return output filename of notebook given site instance
        """
        return f'{site.output_dir}/{self.rootname}.html'

    def get_index_url(self, site):
        """
        Return index page url to notebook given site instance
        """
        return f'{site.base_url}/{self.rootname}.html'

    def get_notebook_data(self, site):
        """
        Return index notebook link data given site instance
        """
        return (self.get_index_url(site), self.title)

    def export(self, exporter, site):
        """
        Render the notebook

        :param exporter: Notebook exporter provided by builder
        :param site: Site instance provided by builder
        """
        log = logging.getLogger('notebook:Notebook#export')
        outn = self.get_output_filename(site)
        log.debug(f"Output filename: '{outn}'")
        body, _ = exporter.from_notebook_node(self._nb)
        log.debug(f'Body size: {len(body)} bytes')
        log.debug(f'Writing to {repr(outn)}')
        with open(outn, 'w+', encoding='utf-8') as out:
            out.write(body)


def load_all(site, include_non_publish=False):
    """
    Loads all notebooks from the given site

    :param site: Site instance
    :param include_non_publish: true if nonpublished notebooks are also included
    """
    log = logging.getLogger('notebook:load_all')
    log.debug(f'include_non_publish: {include_non_publish}')
    files = glob.glob(f'{site.notebook_dir}/*{Notebook.ext}')
    notebooks = [read(file) for file in files]
    returning = [nb for nb in notebooks 
        if nb.publish or include_non_publish]
    log.debug(f'Returning: {returning}')
    return returning


def read(filename):
    """
    Read single notebook from file

    :param filename: path of notebook file to read
    """
    log = logging.getLogger('notebook:read')
    log.debug(f"Reading '{filename}'")
    with open(filename, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    return Notebook(nb, filename)