from ipywidgets import widgets
from IPython.display import display, Markdown, Latex
from IPython.core.display import HTML

display(HTML("""<style>
h4 {
    margin-top: 20px;
}
</style>"""))

def create_input(q):
    return widgets.Text(
        placeholder='Vul in...'
    )

questions = [
    'Wat is het kwadraat van 8?',
    'Wie is de docent van dit vak?'
]

fields = [ (q, create_input(q)) for q in questions ]

def get_answers():
	return { question: field.value for (question, field) in fields }


def ask():
	for i, (question, field) in enumerate(fields):
		question_heading = widgets.HTML(value='<h4>Vraag %d: %s</h4>' % (i + 1, question))
		field_with_question = widgets.VBox([question_heading, field])

		display(field_with_question)