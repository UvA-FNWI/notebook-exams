import click
import json

import json
import sys
import os
from subprocess import call
from shutil import copyfile

from xml.etree import ElementTree as ET
import xml
from slugify import slugify

from colorama import Fore, Back, Style

@click.command('student-notebook')
@click.argument('notebook_file')
def student_notebook(notebook_file):
    '''Creates a student version of a notebook.'''
    
    if not os.path.exists(notebook_file):
        print Fore.RED + 'The notebook file does not exist.' + Style.RESET_ALL
        exit()
    
    def check_and_create(folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
            
    def execute(c):
        call(c.split())
    
    in_nb = notebook_file
    nb_name = os.path.splitext(in_nb)[0]
    
    out_nb = nb_name +'/Student/'+ os.path.basename(in_nb)
    
    out_questions = nb_name +'/Student/questions.json'
    out_questions_answers = nb_name +'/Teacher/Grading/submissions/answer-model.json'
    grading_info = nb_name +'/Teacher/Grading/submissions/Place_submissions_here'
    
    check_and_create(nb_name)
    check_and_create(os.path.dirname(out_nb))
    check_and_create(os.path.dirname(out_questions))
    
    check_and_create(os.path.dirname(os.path.dirname(os.path.dirname(out_questions_answers))))
    check_and_create(os.path.dirname(os.path.dirname(out_questions_answers)))
    check_and_create(os.path.dirname(out_questions_answers))
    
    copyfile(in_nb, nb_name +'/Teacher/'+ nb_name +'.template.ipynb')
    
    data = json.load(open(in_nb))
    
    questions = []
    questions_with_answers = []
    
    new_cells = []
    question_number = 0
    
    currentMarkdown = None
    
    for cell in data['cells']:
        if cell['cell_type'] == 'markdown':
            for l in cell['source']:
                el = None
    
                try:
                    el = ET.fromstring(l)
                except xml.etree.ElementTree.ParseError:
                    if not currentMarkdown:
                        currentMarkdown = []
    
                    currentMarkdown.append(l)
    
                if el is not None and el.tag == 'answer':
                    #print ET.tostring(el)
                    if currentMarkdown:
                        new_cells.append({
                           "cell_type": "markdown",
                           "metadata": {},
                           "source": currentMarkdown
                        },)
    
                        currentMarkdown = None
    
                    qid = el.attrib['id']
    
                    q = {
                        'id': qid,
                        'properties': el.attrib
                    }
    
                    questions.append(q)
    
                    if el.text:
                        q = q.copy()
                        q['answer-spec'] = el.text
    
                    questions_with_answers.append(q)
    
                    new_cells.append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "collapsed": False
                        },
                        "outputs": [],
                        "source": ['questions.ask("%s")' % q['id']]
                    })

                    if 'type' in q['properties'] and q['properties']['type'] == 'code':
                        new_cells.append({
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {
                                "collapsed": False
                            },
                            "outputs": [],
                            "source": ['']
                        })

                        new_cells.append({
                            "cell_type": "markdown",
                            "metadata": {},
                            "source": ['---']
                        })

                    if 'type' in q['properties'] and q['properties']['type'] == 'markdown':
                        new_cells.append({
                            "cell_type": "markdown",
                            "metadata": {},
                            "source": ['_Schrijf hier je antwoord in Markdown_']
                        })
    
        if currentMarkdown:
            new_cells.append({
               "cell_type": "markdown",
               "metadata": {},
               "source": currentMarkdown
            },)
    
            currentMarkdown = None
    
        if cell['cell_type'] == 'code':
            cell['execution_count'] = None
            cell['outputs'] = []
    
            new_cells.append(cell)
    
    data['cells'] = new_cells
    
    # Convert to Python 3 kernel
    data['metadata']['kernelspec']['display_name'] = 'Python 3'
    data['metadata']['kernelspec']['name'] = 'python3'
    data['metadata']['language_info']['codemirror_mode']['version'] = 3
    data['metadata']['language_info']['version'] = '3.6.3'
    data['metadata']['language_info']['pygments_lexer'] = 'ipython3'
    
    json.dump(data, open(out_nb, 'w'))
    
    json.dump(questions, open(out_questions, 'w'))
    json.dump(questions_with_answers, open(out_questions_answers, 'w'))
        
    execute('touch %s' % grading_info)
    
    execute('zip -q -r -j %s/%s.zip %s/Student' % (nb_name, nb_name, nb_name))
    
    print
    print(Fore.GREEN + ('Notebook "%s" has been processed.' % in_nb) + Style.RESET_ALL)
    print('The following directory structure has been created:')
    print
    print('-- %s/' % nb_name)
    print('--- Student/\t\t\t\t(contains student version and question definitions file)')
    print('--- Teacher/\t\t\t\t(contains the original template)')
    print('---- Grading/\t\t\t\t(place your post-exam submissions-folder in here)')
    print('--- %s.zip\t(a zip file that can be imported (see notebook-exam setup exam --help)' % nb_name)
    print