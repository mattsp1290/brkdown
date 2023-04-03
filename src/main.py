#!/usr/bin/env python3

import click
from click import UsageError
from os import environ, path, remove
import os
from sys import exit
import json

from .audio.split import split_directory_into_chunks
from .config.config import Config
from .audio.time_stretch import time_stretch_directory

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

@cli.command()
@click.argument('target_bpm')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=True))
def stretch(output, input, target_bpm):
    click.echo(click.format_filename(input))
    click.echo(click.format_filename(output))
    target_path = os.path.join(input, input)
    setup_config(target_path)
    time_stretch_directory(target_bpm, target_path, output)
    
    



@cli.group()
def m8():
    pass

