"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import logging
from .builder import Builder
import nbconvert

class NotebookBuilder(Builder):
    """
    Handles building jupyter notebooks
    """

    def get_all(self, site, include_non_publish=False):
        """
        Get all notebooks
        """
        return [ 
            nb for nb in site.notebooks 
            if nb.metadata.callystio.publish or include_non_publish ]

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
        for nb in self.get_all(site):
            # Get output filename
            log.info(f"Building '{nb.metadata.callystio.filename}'")
            output_filename = f'{site.output_dir}/{nb.metadata.callystio.rootname}.html'
            log.debug(f"Output filename: '{output_filename}'")

            # Export to html
            body, _ = html.from_notebook_node(nb, {
                'jupyter_widgets_base_url': 'https://cdn.jsdelivr.net/npm/',
                'html_manager_semver_range': '*'
            })
            log.debug(f'Body size: {len(body)} bytes')

            # Write file
            log.debug(f'Writing file to {repr(output_filename)}')
            with open(output_filename, 'w+', encoding='utf-8') as out:
                out.write(body)