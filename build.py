#!/usr/bin/env python
"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import os
import argparse
import sys
import logging
import yaml
from buildsite.site import Site

# Parse args
parser = argparse.ArgumentParser(description="Build notebook site")
parser.add_argument('-d', '--debug', help='debug output', action='store_true')
args = parser.parse_args()

# Configure logging
level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)
log = logging.getLogger('build.py')

# Read config python file
config_file = './config.yaml'
log.debug(f'Config file: {config_file}')
if os.path.exists(config_file):
    log.debug('Config file found!')
    with open(config_file) as f:
        config = yaml.full_load(f)
    site = Site(**config)
else:
    log.debug('No config file found')
    log.debug('Default config')
    site = Site()

# Build site
log.info(site)
site.build()