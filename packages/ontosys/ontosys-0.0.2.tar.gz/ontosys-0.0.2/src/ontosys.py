#!/usr/bin/env python3
import click
import os
from .version import __version__  # Changed from ontosys_cli.version to .version

@click.command()
@click.version_option(version=__version__)
def main():
    """OntosysCLI - Process standard folders."""
    click.echo(f"OntosysCLI version: {__version__}")
    current_dir = os.getcwd()
    click.echo(f"Processing standard folders in: {current_dir}")
    # Your main app logic here

if __name__ == "__main__":
    main()