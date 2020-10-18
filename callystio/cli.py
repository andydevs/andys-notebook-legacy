"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import click
import sys
import logging
from .site import load_site


@click.group()
@click.option('--debug/--no-debug', default=False, help='Toggle debug logs')
def cli(debug):
    """
    Command line interface
    """
    # Configure logging
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)


@cli.command()
def build():
    """
    Build the site
    """
    # Get logger
    log = logging.getLogger('build')

    # Load and build site
    site = load_site()
    log.info(site)
    site.build()