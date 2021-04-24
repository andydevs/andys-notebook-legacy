"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from ..config import Configurable

class Loader(Configurable):
    """
    Loader class
    """
    def load(self, site):
        """
        Load site files

        :param site: site instance
        """
        raise NotImplementedError