from ipywidgets import widgets
from IPython.display import display, Markdown, Latex
from IPython.core.display import HTML

import re

import os
import json

def load():
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
    </style>

    <script>
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
        $('.widget-text input[type="text"]').unbind('keydown')
        $('.widget-text input[type="text"]').on('keydown', function(e) {
            if((e.metaKey || e.ctrlKey) && e.keyCode == 83) {
                IPython.notebook.save_checkpoint()

                e.preventDefault();
                return false;
            }
        })
    }, 5000)
    </script>"""))

def create_input(q):
    w = widgets.Text(
        placeholder='Vul in...',
        value=answers[q]['answer']
    )
    
    w.question = q
    w.observe(answer_changed)
    
    return w

def answer_changed(change):
    if change['name'] == 'value':
        q = change.owner.question
        answers[q]['answer'] = change.new
        
        save_answers()

def score_changed(change):
    if change['name'] == 'value':
        q = change.owner.question

        if len(str(change.new)):
            try:
                new = float(change.new)
            except:
                new = 0

            answers[q]['score'] = new
        else:
            answers[q]['score'] = 0
        
        save_answers()
        
def save_answers():
    with open(answer_file, 'w') as f:
        json.dump(answers, f)

def get_answers():
	return answers

def pretty_print_answers():
    for i, (q, a) in enumerate(answers.items()):
        display(Markdown('#### '+ str(i + 1) +'. '+ q))
        display(Markdown('*'+ a['answer'] +'*'))

def ask(qid):
    question = questions_map[qid]

    if 'answer-spec' in question and not ('type' in question['properties'] and question['properties']['type'] == 'open'):
        X = answers[qid]['answer']

        r = False
        try:
            r = eval(question['answer-spec'])
        except:
            pass

        if r:
            if 'points' in question['properties']:
                points = float(question['properties']['points'])
            else:
                points = 1

            answers[qid]['score'] = points
            color = 'green'
        else:
            answers[qid]['score'] = 0
            color = 'red'

        save_answers()

        spec_label = 'Test'

        spec_html = '''<div style="margin-bottom: 13px;"><span class="spec-label">'''+ spec_label +'''</span>:&nbsp;&nbsp;<pre style="display: inline; color: '''+ color +'''">'''+ question['answer-spec'] +'''</pre></div>'''

        answer_spec = widgets.HTML(value=spec_html)
        score_description = 'Automatische score:'
    else:
        color = 'black'
        answer_spec = None

        if 'points' in question['properties']:
            score_description = 'Score (maximaal '+ str(question['properties']['points']) +'):'
        else:
            score_description = 'Score:'

    if role == 'teacher':
        score_field = widgets.Text(
            description=score_description,
            placeholder='0',
            value=str(answers[qid]['score'])
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

    if 'type' in question['properties'] and question['properties']['type'] == 'open':

        if 'answer-spec' in question:
            spec_label = 'Richtlijn'
            spec_html = '''<div style="margin-top: 6px;"><span class="spec-label">'''+ spec_label +'''</span>:&nbsp;&nbsp;<pre style="display: inline;">'''+ question['answer-spec'] +'''</pre></div>'''

            widget = widgets.HBox([widgets.HTML(value=spec_html), score_flex])
            widget.layout.justify_content = 'space-between'
        else:
            widget = widgets.HBox([answer_spec_score])
            widget.layout.justify_content = 'flex-end'

    else:
        field = create_input(qid)

        widget = widgets.HBox([field, answer_spec_score])
        widget.layout.justify_content = 'space-between'

    display(widget)

if 'STUDENT_QUESTIONS_FILE' in os.environ:
    questions_file = os.environ['STUDENT_QUESTIONS_FILE']
else:
    questions_file = 'questions.json'

if 'STUDENT_ANSWERS_FILE' in os.environ:
    answer_file = os.environ['STUDENT_ANSWERS_FILE']
else:
    answer_file = 'answers.json'

if 'TEACHER_ANSWER_MODEL' in os.environ:
    questions_answers_file = os.environ['TEACHER_ANSWER_MODEL']
else:
    questions_answers_file = 'questions-answers.json'

if os.path.isfile(questions_answers_file):
    questions = json.load(open(questions_answers_file))

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

if os.path.isfile('answers.json'):
    with open(answer_file) as f:
        answers = json.load(f)
else:
    answers = { q['id']: { 'answer': '', 'score': 0 } for q in questions }
    
    save_answers()
    
# fields = [ (q, create_input(q)) for q in questions ]