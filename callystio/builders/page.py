"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import logging
from .builder import Builder

class PageBuilder(Builder):
    """
    Builds html pages from markdown files in "pages" directory
    """
    # Component configuration
    _config = {
        'template_name': 'page.html'
    }

    def build(self, site):
        """
        Build pages
        """
        # Get logger
        log = logging.getLogger('PageBuilder:build')
        log.info(f'Building page directory')

        # Get tamplate
        template = site.jinja_env.get_template(self.template_name)

        # Build all pages
        for file in site.pages:
            log.info(f'Building: {file.filename}')
            output_filename = f'{site.output_dir}/{file.rootname}.html'
            log.debug(f"Output filename: '{output_filename}'")
            output = template.render(content=file.html)
            with open(output_filename, 'w+', encoding='utf-8') as out:
                out.write(output)