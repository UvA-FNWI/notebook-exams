import pandas as pd
import sys
import json
import os
from subprocess import call
from distutils.dir_util import copy_tree

import subprocess

from colorama import Fore, Back, Style

import click

@click.command('exam', short_help='Setup exam folders on hub')
@click.argument('exam_name')
@click.argument('exam_file',
				default='exam.zip')
def exam(exam_name, exam_file):
	"""Setup exam folders on hub."""
	
	if not os.path.exists(exam_file):
		print Fore.RED + 'The exam file does not exist.' + Style.RESET_ALL
		exit()
		
	print '-- Copying exam file to hub... (%s)' % exam_file
	
	exam_destination = '/tmp/'+ exam_name +'-exam.zip'
	
	proc = subprocess.Popen(['gcloud', '-q', 'compute', 'copy-files', exam_file, 'exam-admin@hub:'+ exam_destination ], shell=False)
	proc.communicate()
	
	print '-- Setting up exam on hub...'
	
	proc = subprocess.Popen(['gcloud', '-q', 'compute', 'ssh', 'jesse@hub', '--', 'sudo /var/uva/scripts/setup_exam %s %s' % (exam_name, exam_destination) ], shell=False)
	proc.communicate()
	
@click.command('students', short_help='Setup student home folders on hub')
@click.argument('exam_name')
@click.argument('students_file',
				default='students.xlsx')
def students(exam_name, students_file):
	"""Setup student home folders on hub."""
	
	if not os.path.exists(students_file):
		print Fore.RED + 'The students file does not exist.' + Style.RESET_ALL
		exit()
		
	print '-- Copying students file to hub... (%s)' % students_file
	
	students_destination = '/tmp/'+ exam_name +'-students.xlsx'
	
	proc = subprocess.Popen(['gcloud', '-q', 'compute', 'copy-files', students_file, 'exam-admin@hub:'+ students_destination ], shell=False)
	proc.communicate()
	
	print '-- Setting up students on hub...'
	
	proc = subprocess.Popen(['gcloud', '-q', 'compute', 'ssh', 'jesse@hub', '--', 'sudo /var/uva/scripts/setup_students %s %s' % (exam_name, students_destination) ], shell=False)
	proc.communicate()