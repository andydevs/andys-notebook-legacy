"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import sys
import logging
from .site import Site

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO)

if __name__ == "__main__":
    my_site = Site()
    my_site.build()