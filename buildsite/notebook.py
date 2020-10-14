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

log = logging.getLogger('notebook')

class Notebook:
    ext = '.ipynb'

    @staticmethod
    def load_all(site, include_non_publish=False):
        log.debug(f'include_non_publish: {include_non_publish}')
        files = glob.glob(f'{site.notebook_dir}/*{Notebook.ext}')
        notebooks = [Notebook.read(file) for file in files]
        returning = [nb for nb in notebooks 
            if nb.publish or include_non_publish]
        log.debug(f'Returning: {returning}')
        return returning

    @staticmethod
    def read(filename):
        log.debug(f"Reading '{filename}'")
        with open(filename, 'r') as f:
            nb = nbformat.read(f, as_version=4)
        return Notebook(nb, filename)

    def __init__(self, nb, filename=''):
        self._nb = nb
        self._filename = filename
        log.debug(f"Initialized notebook from file '{self._filename}'")
        log.debug(f"Rootname: '{self.rootname}'")
        log.debug(f"Title: '{self.title}'")
        log.debug(f'Metadata: {repr(self.metadata)}')

    def __repr__(self):
        return f'Notebook(filename="{self._filename}")'

    @property
    def filename(self):
        return self._filename

    @property
    def rootname(self):
        name = os.path.basename(self._filename)
        return os.path.splitext(name)[0]

    @property
    def title(self):
        return self._nb.metadata.get('title', self.rootname)

    @property
    def metadata(self):
        return self._nb.metadata.andysnb

    @property
    def publish(self):
        return self.metadata.get('publish', False)

    def get_output_filename(self, site):
        return f'{site.output_dir}/{self.rootname}.html'

    def get_index_url(self, site):
        return f'{site.base_url}/{self.rootname}.html'

    def get_notebook_data(self, site):
        return (self.get_index_url(site), self.title)

    def export(self, exporter, site):
        outn = self.get_output_filename(site)
        log.debug(f"Output filename: '{outn}'")
        body, _ = exporter.from_notebook_node(self._nb)
        log.debug(f'Body size: {len(body)} bytes')
        log.debug(f'Writing to {repr(outn)}')
        with open(outn, 'w+', encoding='utf-8') as out:
            out.write(body)