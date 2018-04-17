import pandas as pd
import sys
import json
import os
from subprocess import call
from distutils.dir_util import copy_tree

import subprocess

from colorama import Fore, Back, Style

import click

from notebook_client import Client, upload_file

from os.path import expanduser
home = expanduser('~')

with open(home +'/.notebook-exam-password') as f:
	interface_password = f.read()

@click.command('exam', short_help='Setup exam folders on hub')
@click.argument('exam_name')
@click.argument('exam_file',
				default='exam.zip')
@click.option('--exam-start', help='Start time of exam in format: DD-MM-YYYY_HH:MM', default='none')
@click.option('--exam-password', help='Password needed to start the exam', default='none')
def exam(exam_name, exam_file, exam_start, exam_password):
    """Setup exam folders on hub."""
    
    if not os.path.exists(exam_file):
    	print Fore.RED + 'The exam file does not exist.' + Style.RESET_ALL
    	exit()
    
    print '-- Copying exam file to hub... (%s)' % exam_file
    
    c = Client(password=interface_password)
    upload_file(c, exam_file)
    
    exam_filename = os.path.basename(exam_file)
    exam_destination = '/var/uva/tmp/%s-exam.zip' % exam_name
    
    c = Client(password=interface_password)
    c.execute('mv /var/uva/delivery/incoming/%s %s' % (exam_filename, exam_destination))
    
    print '-- Setting up exam on hub...'
    
    c = Client(password=interface_password)
    c.execute('/scripts/setup_exam %s %s %s %s' % (exam_name, exam_destination, exam_start, exam_password), to_stdout=True)
	
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
    
    c = Client(password=interface_password)
    upload_file(c, students_file)
    
    students_filename = os.path.basename(students_file)
    students_destination = '/var/uva/tmp/'+ exam_name +'-students.xlsx'
    
    c = Client(password=interface_password)
    c.execute('mv /var/uva/delivery/incoming/%s %s' % (students_filename, students_destination))
    
    print '-- Setting up students on hub...'
    
    c = Client(password=interface_password)
    c.execute('/scripts/setup_students %s %s' % (exam_name, students_destination), to_stdout=True)
