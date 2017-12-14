import click
import subprocess
import json
import pandas as pd
from tabulate import tabulate

from colorama import Fore, Back, Style

@click.command('exams')
def exams():
	data = subprocess.check_output(['gcloud', '-q', 'compute', 'ssh', 'exam-admin@hub', '--', 'cat /var/uva/exams.json' ], stderr=subprocess.STDOUT)
	data = json.loads(data)
	
	for exam in data['exams']:
		if 'students' in data['exams'][exam]:
			data['exams'][exam]['student_count'] = len(data['exams'][exam]['students'])
			
			del data['exams'][exam]['students']
		else:
			data['exams'][exam]['student_count'] = 0
			
	df = pd.DataFrame.from_dict(data['exams'], orient='index')
	df = df[['name', 'exam_location', 'student_count']]
	
	if len(df):
		print tabulate(df, headers='keys', tablefmt='psql', showindex='never')
	else:
		print "No exams found."
	
@click.command('students')
@click.argument('exam_name')
def students(exam_name):
	data = subprocess.check_output(['gcloud', '-q', 'compute', 'ssh', 'exam-admin@hub', '--', 'cat /var/uva/exams.json' ], stderr=subprocess.STDOUT)
	data = json.loads(data)
	
	if exam_name in data['exams']:
		exam = data['exams'][exam_name]
		
		for exam in data['exams']:
			if 'students' in data['exams'][exam]:
				students = data['exams'][exam]['students']
			else:
				students = []
				
		df = pd.DataFrame.from_dict(students, orient='index')
		#df = df[['name', 'exam_location', 'student_count']]
		
		if len(df):
			print tabulate(df, headers='keys', tablefmt='psql', showindex='never')
		else:
			print "No students found."
	else:
		print Fore.RED + ('Exam with name "%s" does not exist.' % exam_name) + Style.RESET_ALL