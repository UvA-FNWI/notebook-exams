import click

import subprocess
import json
import pandas as pd
from tabulate import tabulate

import os

from os.path import expanduser
home = expanduser('~')

@click.group()
def cli():
    pass
	
@click.command('start')
def start():
    '''Start the Docker notebook environment.'''

    script_path = os.path.dirname(os.path.realpath(__file__)) +'/scripts/run-notebook.sh'
    proc = subprocess.Popen([script_path], shell=False)
    proc.communicate()

cli.add_command(start)