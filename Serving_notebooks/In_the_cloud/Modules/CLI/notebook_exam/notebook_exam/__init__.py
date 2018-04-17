import click

import subprocess
import json
import pandas as pd
from tabulate import tabulate

import os

from notebook_commands.notebook_client import Client

from os.path import expanduser
home = expanduser('~')

@click.group()
def cli():
    pass
    
@click.command('authenticate')
@click.argument('password')
def authenticate(password):
	'''Authenticate with the service (needed once).'''
	
	try:
		c = Client(password)
	except:
		print "The password is incorrect."
		
		exit()
	
	with open(home +'/.notebook-exam-password', 'w') as f:
		f.write(password)
	    
	print "You are logged in."
	    
	c.send('close')
	c.close()

cli.add_command(authenticate)

if os.path.exists(home +'/.notebook-exam-password'):
	import notebook_commands.setup
	import notebook_commands.list
	import notebook_commands.provision
	import notebook_commands.prepare
	import notebook_commands.grade
	import notebook_commands.notebook
	
	@cli.group()
	def prepare():
	    '''Commands for preparing exams.'''
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
		
	@cli.group()
	def grade():
		'''Commands for grading exams.'''
		pass

	@cli.group()
	def notebook():
		'''Commands for notebook environment.'''
		pass
	
	prepare.add_command(notebook_commands.prepare.student_notebook)
	setup.add_command(notebook_commands.setup.exam)
	setup.add_command(notebook_commands.setup.students)
	list.add_command(notebook_commands.list.exams)
	list.add_command(notebook_commands.list.students)
	provision.add_command(notebook_commands.provision.cluster)
	grade.add_command(notebook_commands.grade.collect_submissions)
	grade.add_command(notebook_commands.grade.divide_submissions)
	grade.add_command(notebook_commands.grade.merge_results)
	grade.add_command(notebook_commands.grade.calculate_grades)
	grade.add_command(notebook_commands.grade.auto_score)
	notebook.add_command(notebook_commands.notebook.start)