import pandas as pd
import sys
import json
import hashlib
from subprocess import call
from distutils.dir_util import copy_tree

import click

def execute(c):
	call(c.split())

def setup_student(student):
	student_id = str(student['StudentID'])
	student_hash =  hashlib.md5(student_id).hexdigest()
	
	print '----------------'
	print 'Student #'+ student_id
	print '----------------'
	
	print 'Creating user directory...'
	
	# Setup directory structure
	execute('mkdir /var/uva/data/users/'+ student_hash)
	execute('mkdir /var/uva/data/users/'+ student_hash +'/info')
	execute('mkdir /var/uva/data/users/'+ student_hash +'/work')
	
	# Create symbolic use for ease of use
	execute('ln -s /var/uva/data/users/'+ student_hash +' /var/uva/data/students/'+ student_id)
	
	print 'Saving student info...'
	
	# Store root-only student info (e.g. used to set UID of NFS user)
	student_data = student.to_dict()
	with open('/var/uva/data/users/'+ student_hash +'/info/info.json', 'w') as f:
		json.dump(student_data, f)
		
	with open('/var/uva/data/users/'+ student_hash +'/info/student_id', 'w') as f:
		f.write(str(student_data['StudentID']))
		
	print 'Copying exam files...'
	copy_tree(exam_location +'/exam', '/var/uva/data/users/'+ student_hash +'/work/'+ exam_name)
	
	# Set ownership and permissions
	execute('chown -R '+ student_id +':users /var/uva/data/users/'+ student_hash)
	execute('chmod -R 700 /var/uva/data/users/'+ student_hash)
	
	# Info is owned and thus only visible to root (because of 0600)
	execute('chown -R root:root /var/uva/data/users/'+ student_hash +'/info')
	execute('chmod -R 600 /var/uva/data/users/'+ student_hash +'/info')
	
	print 

@click.command('setup', short_help='Setup student home folders with exam')
@click.option('--title', 
				show_default=True,
				default='Exam',
				help='Title of the exam')
@click.option('--students', 
				show_default=True,
				default='students.xlsx',
				help='DataNose .xlsx export that containing all students')
@click.option('--exam', 
				show_default=True,
				default='exam.zip',
				help='Zip file containing the exam')
def setup(title, students, exam):
	"""Sets up student home folders and copies exam files."""

	exam_name, students_file, exam_file = sys.argv[1:]
	exam_location = '/'.join(exam_file.split('/')[:-1])

	execute('rm -rf '+ exam_location +'/exam')

	print 'Unzipping exam... ('+ exam_file +' to '+ exam_location +'/exam)'
	execute('unzip -j '+ exam_file +' -d '+ exam_location +'/exam')

	students = pd.read_excel(students_file)
	del students['UvAnetID']
	del students['Gender']
	del students['Programme']
	del students['PreviousAttempts']

	for i, student in students.iterrows():
		setup_student(student)

if __name__ == '__main__':
    setup()