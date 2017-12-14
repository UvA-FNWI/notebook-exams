import json
import sys
import os
from shutil import copyfile

from xml.etree import ElementTree as ET
import xml
from slugify import slugify

def check_and_create(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)

in_nb = sys.argv[1]
nb_name = os.path.splitext(in_nb)[0]

out_nb = nb_name +'/Voor student/'+ os.path.basename(in_nb)

out_questions = nb_name +'/Voor student/questions.json'
out_questions_answers = nb_name +'/Voor docent/answer-model.json'

check_and_create(nb_name)
check_and_create(os.path.dirname(out_nb))
check_and_create(os.path.dirname(out_questions))
check_and_create(os.path.dirname(out_questions_answers))

copyfile(in_nb, nb_name +'/Voor docent/'+ nb_name +'.template.ipynb')

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

json.dump(data, open(out_nb, 'w'))

json.dump(questions, open(out_questions, 'w'))
json.dump(questions_with_answers, open(out_questions_answers, 'w'))