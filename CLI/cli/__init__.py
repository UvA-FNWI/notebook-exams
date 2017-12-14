import click

import commands.setup
import commands.list

import subprocess
import json
import pandas as pd
from tabulate import tabulate

@click.group()
def cli():
    pass

@cli.group()
def setup():
	pass
	
@cli.group()
def list():
	pass

setup.add_command(commands.setup.exam)
setup.add_command(commands.setup.students)
list.add_command(commands.list.exams)
list.add_command(commands.list.students)