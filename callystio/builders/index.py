"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from .builder import Builder
import logging
import markdown

class IndexBuilder(Builder):
    """
    Handles building the index page
    """
    # Component configuration
    _config = {
        'output_name': 'index.html',
        'template_name': 'index.html'
    }

    def _get_all_metadata(self, site, include_non_publish=False):
        """
        Get all notebook metadata
        """
        log = logging.getLogger('IndexBuilder:_get_all_metadata')
        metadata = [
            nb.metadata.callystio for nb in site.notebooks 
            if nb.metadata.callystio.publish or include_non_publish ]
        for notebook in metadata:
            notebook.link = f'{site.base_url}/{notebook.rootname}.html'
        log.debug(f'Notebooks data: {metadata}')
        return metadata

    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        # Get logger
        log = logging.getLogger('IndexBuilder:build')
        log.info(f"Building '{self.output_name}'")

        # Get template
        template = site.jinja_env.get_template(self.template_name)

        # Render and write to file
        log.debug('Writing to output file')
        metadata = self._get_all_metadata(site)
        output = template.render(readme=site.readme.html, notebooks=metadata)
        with open(f'{site.output_dir}/{self.output_name}', 'w+') as file:
            file.write(output)