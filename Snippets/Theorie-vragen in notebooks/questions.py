from ipywidgets import widgets
from IPython.display import display, Markdown, Latex
from IPython.core.display import HTML

import os.path
import json

display(HTML("""<style>
h4 {
    margin-top: 20px;
}

.widget-area .prompt .close {
    display: none !important;
}
</style>"""))

def create_input(q):
    w = widgets.Text(
        placeholder='Vul in...',
        value=answers[q]
    )
    
    w.question = q
    w.observe(answer_changed)
    
    return w

def answer_changed(change):
    if change['name'] == 'value':
        q = change.owner.question
        answers[q] = change.new
        
        save_answers()
        
def save_answers():
    with open(answer_file, 'w') as f:
        json.dump(answers, f)
    
answer_file = 'answers.json'

questions = [
    'Wat is het kwadraat van 8?',
    'Wie is de docent van dit vak?'
]

if os.path.isfile('answers.json'):
    with open(answer_file) as f:
        answers = json.load(f)
else:
    answers = { q: '' for q in questions }
    
    save_answers()
    
fields = [ (q, create_input(q)) for q in questions ]

def get_answers():
	return answers

def pretty_print_answers():
    for i, (q, a) in enumerate(answers.items()):
        display(Markdown('#### '+ str(i + 1) +'. '+ q))
        display(Markdown('*'+ a +'*'))

def ask():
	for i, (question, field) in enumerate(fields):
		question_heading = widgets.HTML(value='<h4>Vraag %d: %s</h4>' % (i + 1, question))
		field_with_question = widgets.VBox([question_heading, field])

		display(field_with_question)