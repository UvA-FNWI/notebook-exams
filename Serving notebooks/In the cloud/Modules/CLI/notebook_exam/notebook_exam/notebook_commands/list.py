import click
import subprocess
import json
import pandas as pd
from tabulate import tabulate

from colorama import Fore, Back, Style

from notebook_client import Client

from os.path import expanduser
home = expanduser('~')

with open(home +'/.notebook-exam-password') as f:
	interface_password = f.read()

@click.command('exams')
def exams():
    c = Client(password=interface_password)
    data = c.execute('cat /var/uva/exams.json')

    if data:
        data = json.loads(data)
    
        for exam in data['exams']:
            if 'students' in data['exams'][exam]:
                data['exams'][exam]['student_count'] = len(
                    data['exams'][exam]['students'])
    
                del data['exams'][exam]['students']
            else:
                data['exams'][exam]['student_count'] = 0
    
        if len(data['exams']):
            df = pd.DataFrame.from_dict(data['exams'], orient='index')
            df = df[['name', 'exam_location', 'student_count']]
    
            print tabulate(df, headers='keys', tablefmt='psql', showindex='never')
        else:
            print "No exams found."
    else:
        print "No exams found."

@click.command('students')
@click.argument('exam_name')
def students(exam_name):
    c = Client(password=interface_password)
    data = c.execute('cat /var/uva/exams.json')
    
    data = json.loads(data)

    if exam_name in data['exams']:
        exam = data['exams'][exam_name]

        students = exam['students']

        if len(students):
            df = pd.DataFrame(students)
            df = df[['StudentID', 'FirstName', 'MiddleName',
                     'LastName', 'Email', 'home_folder']]

            #df = df[['name', 'exam_location', 'student_count']]

            print tabulate(df, headers='keys', tablefmt='psql', showindex='never')
        else:
            print "No students found."
    else:
        print Fore.RED + ('Exam with name "%s" does not exist.' % exam_name) + Style.RESET_ALL
