"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import logging
from .loader import Loader
import markdown

class MarkdownFile:
    """
    File representation in Callystio
    """
    def __init__(self, filename, html):
        """
        Initialize file
        """
        self.filename = filename
        self.html = html

class MarkdownLoader(Loader):
    """
    Load markdown page files
    """
    ext = '.md'

    _config = {
        'directory': '',
        'file': 'README.md'
    }

    def load(self, site):
        """
        Load markdown
        """
        log = logging.getLogger('MarkdownLoader:load')
        if self.directory != '':
            log.info(f'Reading directory: {self.directory}')
            return None
        else:
            log.info(f'Reading file: {self.file}')
            with open(self.file, 'r') as f:
                md = f.read()
            html = markdown.markdown(md)
            log.debug(f'Markdown to html: {html}')
            return MarkdownFile(self.file, html)