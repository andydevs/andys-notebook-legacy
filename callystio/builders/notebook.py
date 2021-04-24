"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import logging
from .builder import Builder
from .. import notebook
import nbconvert

class NotebookBuilder(Builder):
    """
    Handles building jupyter notebooks
    """
    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        # Get logger
        log = logging.getLogger('notebook_builder')

        # Create exporter
        html = nbconvert.HTMLExporter(
            extra_loaders=[site.jinja_loader],
            template_file='notebook.html')
        log.debug(f'HTMLExporter: {repr(html)}')

        # Export notebooks
        notebooks = notebook.load_all(site)
        for nb in notebooks:
            log.info(f"Building '{nb.filename}'")
            nb.export(html, site)