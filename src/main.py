#!/usr/bin/env python3

import click
from click import UsageError
from os import environ, path, remove
import os
from sys import exit
import json

from .audio.split import split_directory_into_chunks
from .files.names import get_brk_name
from .sqlite.db import DB
from .sqlite.migrations import run_migrations
from .config.config import Config

def prepare_sqlite(output_dir):
    DB().set_db(output_dir)
    run_migrations()

def setup_config(input_file):
    Config().set_value("CURRENT_DIRECTORY", input_file)
    



@click.group()
def cli():
    pass

@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=True))
def split(output, input):
    click.echo(click.format_filename(input))
    click.echo(click.format_filename(output))
    target_path = os.path.join(input, input)
    setup_config(target_path)
    split_directory_into_chunks(target_path, output)
    
    



@cli.group()
def m8():
    pass

