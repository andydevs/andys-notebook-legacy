"""
Hosting Jupyter Notebooks on GitHub Pages

Author:  Anshul Kharbanda
Created: 10 - 12 - 2020
"""
import click
import sys
import logging
import coloredlogs
from .site import load_site


@click.group()
def cli():
    """
    Command line interface
    """
    pass

@cli.command()
@click.option('--debug/--no-debug', default=False, help='Toggle debug logs')
def build(debug):
    """
    Build the site
    """
    # Configure logging
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)
    coloredlogs.install(level=level)

    # Get logger
    log = logging.getLogger('build')

    # Load and build site
    site = load_site()
    log.info(site)
    site.build()