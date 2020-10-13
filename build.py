#!/usr/bin/env python
"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import argparse
import sys
import logging
from buildsite.site import Site

# Parse args
parser = argparse.ArgumentParser(description="Build notebook site")
parser.add_argument('-d', '--debug', help='debug output', action='store_true')
args = parser.parse_args()

# Configure logging
level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)

# Build site
Site().build()