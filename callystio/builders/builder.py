"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
from ..config import Configurable

class Builder(Configurable):
    """
    Base class for builders
    """
    def build(self, site):
        """
        Build component of site

        :param site: site instance
        """
        raise NotImplementedError