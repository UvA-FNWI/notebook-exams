import click

import commands.setup
import commands.list
import commands.provision

import subprocess
import json
import pandas as pd
from tabulate import tabulate

@click.group()
def cli():
    pass

@cli.group()
def setup():
	'''Commands for setting up exams and students.'''
	pass
	
@cli.group()
def list():
	'''Commands for listing exams and students.'''
	pass
	
@cli.group()
def provision():
	'''Commands for provisioning a cluster.'''
	pass

setup.add_command(commands.setup.exam)
setup.add_command(commands.setup.students)
list.add_command(commands.list.exams)
list.add_command(commands.list.students)
provision.add_command(commands.provision.cluster)