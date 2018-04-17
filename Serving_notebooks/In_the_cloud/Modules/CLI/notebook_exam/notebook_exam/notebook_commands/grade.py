import click
import subprocess
import json
import pandas as pd
import numpy as np
import os
from subprocess import call
from tabulate import tabulate

from colorama import Fore, Back, Style

from notebook_client import Client, download_file
from random import shuffle
from glob import glob

from shutil import copyfile

from os.path import expanduser
home = expanduser('~')

with open(home +'/.notebook-exam-password') as f:
	interface_password = f.read()
	
def execute(c):
    call(c.split())

@click.command('collect-submissions')
@click.argument('exam_name')
def collect_submissions(exam_name):
    print '-- Generating submissions file...'
    
    c = Client(password=interface_password)
    c.execute('/var/uva/scripts/collect_submissions %s' % exam_name)
    
    print '-- Downloading submissions file from hub...'
    c = Client(password=interface_password)
    download_file(c, 'submissions.zip')
    
    execute('unzip -q submissions.zip -d hub-submissions/')
    execute('rm -f submissions.zip')

    print
    print Fore.GREEN + ('Exam submissions for exam "%s" have been saved to hub-submissions/.' % exam_name) + Style.RESET_ALL
    
@click.command('divide-submissions')
@click.argument('submissions_folder')
@click.argument('graders')
def divide_submissions(submissions_folder, graders):
    graders = graders.split(',')
    
    notebooks = glob('%s/*.ipynb' % submissions_folder)
    if not len(notebooks):
        foldered = True
        notebooks = glob('%s/*/*.ipynb' % submissions_folder)
    else:
        foldered = False
    
    shuffle(notebooks)
    
    chunks = [ list(l) for l in np.array_split(notebooks, len(graders)) ]
    notebook_by_grader = zip(graders, chunks)
    
    if os.path.exists('%s/student-answers.csv' % submissions_folder):
        answers = pd.read_csv('%s/student-answers.csv' % submissions_folder, dtype={ 'student': str })
        
        #answers.set_index(['student', 'question'], inplace=True)
        #answers.sort_index(level=0, inplace=True)
    else:
        answers = None
        
        if os.path.exists('answer-model.json'):
            answer_model_file = 'answer-model.json'
        elif os.path.exists('%s/answer-model.json' % os.path.dirname(submissions_folder)):
            answer_model_file = '%s/answer-model.json' % os.path.dirname(submissions_folder)
        elif os.path.exists('%s/answer-model.json' % submissions_folder):
            answer_model_file = '%s/answer-model.json' % submissions_folder
        else:
            answer_model_file = None
             
        if answer_model_file and len(glob('%s/*/answers.json' % submissions_folder)):
            answer_model = json.load(open(answer_model_file))
            
            all_answers = { f.split('/')[-2]: json.load(open(f)) for f in glob('%s/*/answers.json' % submissions_folder) }
            all_answers = { (student, question): all_answers[student][question] for student in all_answers for question in all_answers[student] }
            
            answers = pd.DataFrame.from_dict(all_answers).transpose()
            answers['score'] = None
            
            answers = answers[['score', 'answer']]
            answers.index.names = ['student', 'question']
            
            answers.to_csv('student-answers.csv', encoding='utf8')
            
            answers = pd.read_csv('student-answers.csv', dtype={ 'student': str })
        else:
            # Create empty answers-file
            empty_answers = pd.DataFrame(columns=['student', 'question', 'score', 'answer'])
            empty_answers.to_csv('student-answers.csv', index=False, encoding='utf8')
        

    os.makedirs('divided-submissions')
    for grader, notebooks in notebook_by_grader:
        os.makedirs('divided-submissions/%s' % grader)
        
        if answer_model_file:
            copyfile(answer_model_file, 'divided-submissions/%s/answer-model.json' % grader)
        
        for notebook in notebooks:
            if foldered:
                student_id = notebook.split('/')[-2]
                
                copyfile(notebook, 'divided-submissions/%s/%s.ipynb' % (grader, student_id))
            else:
                copyfile(notebook, 'divided-submissions/%s/%s' % (grader, os.path.basename(notebook)))
        
        if answers is not None:
            if foldered:
                student_ids = [ notebook.split('/')[-2] for notebook in notebooks ]
            else:
                student_ids = [ os.path.basename(notebook).split('.')[0].split('_')[-1] for notebook in notebooks ]
             
            answers_subset = answers[answers['student'].isin(student_ids)]
            #answers_subset = answers.loc[student_ids]
            
            answers_subset.to_csv('divided-submissions/%s/student-answers.csv' % grader, index=False, encoding='utf8')
        else:
            empty_answers.to_csv('divided-submissions/%s/student-answers.csv' % grader, index=False, encoding='utf8')
            
          
    print Fore.GREEN + ('Exam submissions have been divided among: %s' % ', '.join(graders))
    print 'Their folders can be found in divided-submissions/.' + Style.RESET_ALL
    
@click.command('merge-results')
@click.argument('divided_submissions_folder')
def merge_results(divided_submissions_folder):
    results_files = glob('%s/*/student-answers.csv' % divided_submissions_folder)
    
    results_dfs = [ pd.read_csv(f, dtype={ 'student': str }).set_index(['student', 'question']) for f in results_files ]
    all_results = pd.concat(results_dfs).sort_index(level=0)
            
    all_results.to_csv('all-results.csv', encoding='utf8')
    
    print Fore.GREEN + ('Exam results have been merged and saved to all-results.csv.') + Style.RESET_ALL
    
@click.command('calculate-grades')
@click.argument('results_file')
@click.argument('maximum_score')
def calculate_grades(results_file, maximum_score):
    results = pd.read_csv(results_file, dtype={ 'student': str })
    
    grades = (results.groupby('student').sum() / float(maximum_score)) * 10
    grades = grades.fillna(0)
    
    del grades['answer']
    
    grades.to_csv('grades.csv')
    
    print 'Grades are calculated using the formula: (score / max) * 10.'
    print Fore.GREEN + ('Grades have been calculated and saved to grades.csv.') + Style.RESET_ALL
    
@click.command('auto-score')
@click.argument('submissions_folder')
@click.argument('answer_model_file')
def auto_score(submissions_folder, answer_model_file):
    def check_answer(row):
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        
        if not pd.isnull(row['answer-spec']):
            X = row['answer']
            r = False
            try:
                r = eval(row['answer-spec'])
            except:
                pass
    
            if r:
                return row['points']
            else:
                return 0.0
    
    results_files = glob('%s/*/student-answers.csv' % submissions_folder) + glob('%s/student-answers.csv' % submissions_folder)
    answer_model = json.load(open(answer_model_file))
    
    auto_score_questions = { q['id']: { 'answer-spec': q['answer-spec'], 'points': (float(q['properties']['points']) if ('points' in q['properties']) else 1.0) } for q in answer_model if 'answer-spec' in q and not ('type' in q['properties'] and q['properties']['type'] == 'open') }
    auto_score_questions = pd.DataFrame.from_dict(auto_score_questions, orient='index')

    for f in results_files:
        results_df = pd.read_csv(f, dtype={ 'student': str })
        results_df = results_df.merge(auto_score_questions, how='left', left_on='question', right_index=True)
        
        results_df['score'] = np.where(pd.isnull(results_df['answer-spec']), results_df['score'], results_df.apply(check_answer, axis=1))
        
        results_df[['student', 'question', 'score', 'answer']].to_csv(f, index=False, encoding='utf8')
        execute('touch %s/auto-scoring-done' % os.path.dirname(f))
        
    print Fore.GREEN + ('Automatically scored questions have been scored.') + Style.RESET_ALL