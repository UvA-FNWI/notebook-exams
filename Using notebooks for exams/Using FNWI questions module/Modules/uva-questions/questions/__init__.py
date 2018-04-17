from ipywidgets import widgets
from IPython.display import display, display_javascript, Markdown, Latex
from IPython.core.display import HTML, Javascript

import re

import os
import json
import requests
import sys

import time

import IPython
from IPython.lib import kernel
from notebook.notebookapp import list_running_servers

def get_notebook_info():
    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
    
    servers = list(list_running_servers())
    
    nb_name = None
    student_id = None
    metadata = None
    
    for s in servers:
        if s['hostname'] == '0.0.0.0' and s['base_url'].startswith('/user/'):
            # Hub
            s['url'] = s['url'].replace('0.0.0.0', )
    
        try:
            sessions = requests.get('%sapi/sessions?token=%s' % (s['url'], s['token'])).json()
        except:
            continue
            
        for sess in sessions:
            if sess['kernel']['id'] == kernel_id:
                metadata = json.load(open(os.path.basename(sess['path'])))['metadata']
                if 'uva_student_id' in metadata:
                    student_id = metadata['uva_student_id']
            
                nb_name = os.path.basename(sess['notebook']['path'])
                break
            
    return (nb_name, student_id, metadata)

def get_answers_df(f):
    df = pd.read_csv(f, dtype={ 'student': str })
        
    df.set_index(['student', 'question'], inplace=True)
    df.sort_index(level=0, inplace=True)

    return df
    
def save_answers_df(f, df):
    df.to_csv(f, encoding='utf8')

def load():
    global student_id
    
    try:
        nb_name, nb_student_id, metadata = get_notebook_info()
    
        if nb_student_id:
            student_id = nb_student_id
        else:
            student_id = ''
        
    except:
        student_id = ''

    display(widgets.HTML('<div class="exam-message" style="margin-top: 10px; padding-bottom: 0px;"><strong>Vul hieronder je UvAnetID in en klik op Opslaan, anders kan je tentamen niet worden nagekeken.</strong></div>'))
    
    global student_id_field
    
    student_id_field = widgets.Text(
        placeholder='UvAnetID',
        value=student_id
    )
    
    student_id_field.observe(new_student_id_changed)
    
    global student_id_save_button
    
    student_id_save_button = widgets.Button(
        description='Opslaan',
        disabled=True,
        button_style='success', # 'success', 'info', 'warning', 'danger' or ''
        icon='check'
    )
    
    student_id_save_button.on_click(save_student_id)
    
    display(widgets.HBox([student_id_field, student_id_save_button]))  
    
    display(HTML("""<style>
        h4 {
            margin-top: 20px;
        }
    
        .widget-area .prompt .close {
            display: none !important;
        }
    
        .widget-label, .spec-label {
            color: #666;
            font-weight: bold;
            
            min-width: 180px !important;
        }
        
        .widget-textarea {
            width: 750px;
        }
        
        .teacher-answer {
            font-size: 14pt;
            color: #134596;
        }
        
        .jupyter-widgets-view {
            /*border-top: 1px solid #ccc;*/
            /*border-bottom: 1px solid #ccc;*/
        }
        
        .exam-message {
            font-size: 12pt;
            line-height: 1.2; 
            
            padding-top: 10px;
            padding-bottom: 10px;
        }
        
        .exam-message small {
            font-size: 10pt;
        }
        </style>"""))
    
    if not fail:
        display(HTML("""<script>
        var executed = false
    
        var runAndHide = function() {
            var q_indexes = []
            $('.input_area').each(function(i, area) {
                area = $(area)
    
                if(area.text().indexOf('questions.ask') > -1) {
                    area.parents('.input').hide()
    
                    if(!executed) {
                        var index = $('.cell').index(area.parents('.cell'))
    
                        if(index != -1) {
                            q_indexes.push(index)
                        }
                    }
                }
            })
    
            if(!executed) {
                IPython.notebook.execute_cells(q_indexes)
                executed = true
            }
        }
    
        runAndHide()
    
        setInterval(runAndHide, 200)
    
        setInterval(function() {
            $('.widget-text input[type="text"], .widget-textarea textarea').unbind('keydown')
            $('.widget-text input[type="text"], .widget-textarea textarea').on('keydown', function(e) {
                if((e.metaKey || e.ctrlKey) && e.keyCode == 83) {
                    IPython.notebook.save_checkpoint()
    
                    e.preventDefault();
                    return false;
                }
            })
        }, 5000)
        
        saveTimers = {}
        </script>"""))

def create_input(q, textarea=False, code=False):
    if role == 'student':
        if not code:
            if textarea:
                w = widgets.Textarea(
                    placeholder='Vul in...',
                    value=answers[q]['answer']
                )
            else:
                w = widgets.Text(
                    placeholder='Vul in...',
                    value=answers[q]['answer']
                )
            
            w.question = q
            w.observe(answer_changed)
        else:
            w = widgets.HTML('')
    else:
        if len(answers[q]['answer'].strip()):
            answer = answers[q]['answer'].replace('\n', '<br />')
        else:
            if code:
                answer = '<em style="color: #ccc; font-size: 12pt; margin-bottom: -2px;">Code:</em>'
            else:
                answer = '<em style="color: #ccc;">Geen antwoord</em>'
        
        w = widgets.HTML("<span class='teacher-answer'>%s</span>" % answer)

    return w

def answer_changed(change):
    if change['name'] == 'value':
        q = change.owner.question
        answers[q]['answer'] = change.new
        
        save_answers()
        
        set_metadata_answer(q, change.owner)

def score_changed(change):
    if role == 'teacher':
        if change['name'] == 'value':
            q = change.owner.question
            
            if len(str(change.new)):
                new = change.new.replace(',', '.')
            
                try:
                    new = float(new)
                except:
                    new = 0.0
            else:
                new = 0.0
                
            answers[q]['score'] = new
            answers_df = get_answers_df(student_answers)
            
            #answers_df.set_value((student_id, q), 'score', new)
            answers_df.at[(student_id, q), 'score'] = new
            
            save_answers_df(student_answers, answers_df)
        
def save_answers():
    if answer_file:
        with open(answer_file, 'w') as f:
            json.dump(answers, f)

def get_answers():
	return answers

def pretty_print_answers():
    for i, (q, a) in enumerate(answers.items()):
        display(Markdown('#### '+ str(i + 1) +'. '+ q))
        display(Markdown('*'+ a['answer'] +'*'))

def ask(qid):
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    question = questions_map[qid]

    if 'type' not in question['properties']:
        question_type = 'oneliner'
    else:
        question_type = question['properties']['type']

    if question_type == 'oneliner':
        field = create_input(qid)
    elif question_type == 'long':
        field = create_input(qid, textarea=True)
    elif question_type == 'markdown':
        field = widgets.HTML('<strong style="color: #666;">Jouw antwoord:</strong>')
    elif question_type == 'code':
        field = widgets.HTML('<strong style="color: #666;">Jouw code:</strong>')

    # and not ('type' in question['properties'] and question['properties']['type'] == 'open')
    if 'answer-spec' in question and 'auto-score' in question['properties'] and question['properties']['auto-score'].lower() == 'true':
        X = answers[qid]['answer']

        r = False
        try:
            r = eval(question['answer-spec'])
        except:
            pass

        if r:
            color = 'green'
        else:
            color = 'red'

        spec_label = 'Test'

        spec_html = '''<div style="margin-top: -3px;"><span class="spec-label">'''+ spec_label +'''</span>:&nbsp;&nbsp;<pre style="display: inline; color: '''+ color +'''">'''+ question['answer-spec'] +'''</pre></div>'''

        answer_spec = widgets.HTML(value=spec_html)
        
        if 'points' in question['properties']:
            score_description = 'Score (maximaal '+ str(question['properties']['points']) +'):'
        else:
            score_description = 'Score (maximaal 1):'
    else:
        color = 'black'
        answer_spec = None

        if 'points' in question['properties']:
            score_description = 'Score (maximaal '+ str(question['properties']['points']) +'):'
        else:
            score_description = 'Score (maximaal 1):'

    if role == 'teacher':
        if len(str(answers[qid]['score'])):
            if int(answers[qid]['score']) != float(answers[qid]['score']):
                score = str(float(answers[qid]['score']))
            else:
                score = str(int(answers[qid]['score']))
        else:
            score = ''
    
        score_field = widgets.Text(
            description=score_description,
            placeholder='0',
            value=score
        )
        score_field.question = qid
        score_field.observe(score_changed)

        score_field.layout.width = '235px'
        score_flex = widgets.HBox([score_field])
        score_flex.layout.justify_content = 'flex-end'

        if answer_spec:
            answer_flex = widgets.HBox([answer_spec])
            answer_flex.layout.justify_content = 'flex-end'

            answer_spec_score = widgets.VBox([answer_flex, score_flex])
        else:
            answer_spec_score = score_flex
    else:
        if 'points' in question['properties']:
            points = question['properties']['points']
        else:
            points = '1'

        answer_spec_score = widgets.HTML(value='<span style="color: #666;"><strong>%s</strong> / %d punten</span>' % (points, total_points))

    if 'answer-spec' in question:
        if 'auto-score' not in question['properties'] \
            or ('auto-score' in question['properties'] and question['properties']['auto-score'].lower() == 'false'):

            spec_label = 'Richtlijn'
            spec_html = '''<div style="margin-top: 6px;"><span class="spec-label">'''+ spec_label +'''</span>:&nbsp;&nbsp;<pre style="display: inline;">'''+ question['answer-spec'] +'''</pre></div>'''

            widget = widgets.HBox([field, widgets.VBox([widgets.HTML(value=spec_html), score_flex])])
            widget.layout.justify_content = 'space-between'
        else:
            widget = widgets.HBox([field, answer_spec_score])
            widget.layout.justify_content = 'space-between'
    else:
        widget = widgets.HBox([field, answer_spec_score])
        widget.layout.justify_content = 'space-between'

    display(widget)
    
def set_metadata_answer(question, field):
    q = str(question)
    answer = field.value
    
    display_javascript(Javascript("if('%s' in saveTimers) { clearTimeout(saveTimers['%s']); } saveTimers['%s'] = setTimeout(function() { if(!('uva_answers' in IPython.notebook.metadata)) { IPython.notebook.metadata['uva_answers'] = {} } IPython.notebook.metadata['uva_answers']['%s'] = '%s'; IPython.notebook.save_checkpoint(); }, 500)" % (q, q, q, q, str(answer))))
    
def save_student_id(e):
    if not student_id_save_button.disabled:
        global student_id
        global role
        
        old_student_id = str(student_id)
        student_id = str(student_id_field.value)
        
        if role == 'teacher':
            answers_df = get_answers_df(student_answers)
            answers_df = answers_df.reset_index().replace(old_student_id, student_id).set_index(['student', 'question']).sort_index(level=0)
            
            save_answers_df(student_answers, answers_df)
        
        student_id_save_button.disabled = True
        
        display_javascript(Javascript("if(!('uva_student_id' in IPython.notebook.metadata) || ('uva_student_id' in IPython.notebook.metadata && IPython.notebook.metadata['uva_student_id'] != '%s')) { IPython.notebook.metadata['uva_student_id'] = '%s'; IPython.notebook.save_checkpoint(); }" % (str(student_id), str(student_id))))
 
def new_student_id_changed(change):
    if change['name'] == 'value':
        global student_id
        
        student_id_save_button.disabled = (str(change.new) == str(student_id))
        

if 'STUDENT_QUESTIONS_FILE' in os.environ:
    questions_file = os.environ['STUDENT_QUESTIONS_FILE']
elif os.path.exists('questions.json'):
    questions_file = 'questions.json'
else:
    questions_file = None

if 'STUDENT_ANSWERS_FILE' in os.environ:
    answer_file = os.environ['STUDENT_ANSWERS_FILE']
elif os.path.exists('answers.json'):
    answer_file = 'answers.json'
else:
    answer_file = 'answers.json'

if 'TEACHER_ANSWER_MODEL' in os.environ:
    answer_model = os.environ['TEACHER_ANSWER_MODEL']
elif os.path.exists('answer-model.json'):
    answer_model = 'answer-model.json'
elif os.path.exists('../answer-model.json'):
    answer_model = '../answer-model.json'
else:
    answer_model = None
    
if os.path.exists('student-answers.csv'):
    student_answers = 'student-answers.csv'
else:
    student_answers = None
  
fail = False  
if answer_model and not student_answers:
    display(widgets.HTML('<div class="exam-message"><strong style="color: darkred;">Er is een antwoordmodel gevonden, maar geen bestand met antwoorden van studenten.</strong><br /><small>Er kan niet worden nagekeken.</small></div>'))
    
    fail = True

if student_answers and not answer_model:
    display(widgets.HTML('<div class="exam-message"><strong style="color: darkred;">Er is een bestand met antwoorden van studenten gevonden, maar geen antwoordmodel.</strong><br /><small>Er kan niet worden nagekeken.</small></div>'))
    
    fail = True

if not fail:
    if answer_model:
        questions = json.load(open(answer_model))
    
        role = 'teacher'
    else:
        questions = json.load(open(questions_file))
    
        role = 'student'
    
    questions_map = { q['id']: q for q in questions }
    
    total_points = 0
    for q in questions:
        if 'points' in q['properties']:
            total_points += float(q['properties']['points'])
        else:
            total_points += 1
    
    if student_answers:
        import pandas as pd
        import numpy as np
    
        student_answers_df = get_answers_df(student_answers)
        
        try:
            nb_name, nb_student_id, metadata = get_notebook_info()
        
            if nb_student_id:
                student_id = nb_student_id
            else:
                student_id = nb_name.split('.')[0].split('_')[-1]
            
        except:
            student_id = ''
    
        # display(widgets.HTML('<div class="exam-message">Het volgende student ID is gedetecteerd: <strong>%s</strong><br /><small>Verifi&euml;er of dit correct is.</small></div>' % student_id))
        display(widgets.HTML('<div class="exam-message" style="padding-bottom: 0px; margin-bottom: -5px;">Het volgende student ID is gedetecteerd:</div>'))
        
        global student_id_field
        
        student_id_field = widgets.Text(
            placeholder='Student ID',
            value=student_id
        )
        
        student_id_field.observe(new_student_id_changed)
        
        student_id_save_button = widgets.Button(
            description='Opslaan',
            disabled=True,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Dit overschrijft het studentnummer in het antwoordbestand.',
            icon='check'
        )
        
        student_id_save_button.on_click(save_student_id)
        
        display(widgets.HBox([student_id_field, student_id_save_button]))
        
        display(widgets.HTML('<div class="exam-message" style="padding-top: 0px; margin-top: -5px;"><small>Verifi&euml;er of dit correct is en pas zo nodig aan.</small></div>'))
        
        auto_qs = [ q for q in questions if 'auto-score' in q['properties'] and q['properties']['auto-score'].lower() == 'true' ]
        manual_qs = [ q for q in questions if 'auto-score' not in q['properties'] or ('auto-score' in q['properties'] and q['properties']['auto-score'].lower() == 'false') ]
        
        display(widgets.HTML('<div class="exam-message" style="margin-top: -10px; padding-top: 0px; padding-bottom: 0px; color: #666; line-height: 1.4;"><small><li>%d automatisch nakijkbare vragen</li><li>%d handmatig nakijkbare vragen</li></small></div>' % (len(auto_qs), len(manual_qs))))
        
        if os.path.exists('auto-scoring-done'):
            display(widgets.HTML('<div class="exam-message"><strong style="color: darkgreen;">Auto-scoring is uitgevoerd.</strong><br /><small>Automatisch ingevulde scores mogen overschreven worden.</small></div>'))
        elif len(auto_qs) > 0:
            display(widgets.HTML('<div class="exam-message"><strong style="color: darkred;">Auto-scoring is nog niet uitgevoerd.</strong></div>'))
        
        if student_id not in student_answers_df.index:
            for q in questions:
                student_answers_df.loc[(student_id, q['id']), 'score'] = 0.0
                student_answers_df.loc[(student_id, q['id']), 'answer'] = None
            
            save_answers_df(student_answers, student_answers_df)
        
        answers = student_answers_df.loc[student_id].fillna('').to_dict(orient='index')
    else:
        # 
        try: 
            nb_name, nb_student_id, metadata = get_notebook_info()
        except:
            metadata = None
    
        if metadata and 'uva_answers' in metadata:
            answers = { q: { 'answer': a } for q, a in metadata['uva_answers'].items() }
        elif os.path.isfile(answer_file):
            with open(answer_file) as f:
                answers = json.load(f)
        else:
            answers = { q['id']: { 'answer': '' } for q in questions }
            
            #save_answers()