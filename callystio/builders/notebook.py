"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
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
        for nb in site.notebooks.get_all():
            filename = nb.metadata.callystio.filename
            log.info(f"Building '{filename}'")

            # Get output filename
            rootname = os.path.basename(filename)
            rootname = os.path.splitext(rootname)[0]
            output_filename = f'{site.output_dir}/{rootname}.html'
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