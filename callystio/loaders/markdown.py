"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import logging
from .loader import Loader
from glob import glob
from markdown import markdown

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
        'file': ''
    }

    def _read_markdown_file(self, file):
        log = logging.getLogger('MarkdownLoader:_read_markdown_file')
        with open(file, 'r') as f:
            md = f.read()
        html = markdown(md)
        log.debug(f'Markdown file {file} to html: {html}')
        return MarkdownFile(self.file, html)

    def load(self, site):
        """
        Load markdown
        """
        log = logging.getLogger('MarkdownLoader:load')
        if self.directory != '':
            log.info(f'Reading directory: {self.directory}')
            return [
                self._read_markdown_file(file)
                for file in glob(f'{self.directory}/*{self.ext}')
            ]
        elif self.file != '':
            log.info(f'Reading file: {self.file}')
            return self._read_markdown_file(self.file)
        else:
            log.error(f'No markdown file or directory specified!')