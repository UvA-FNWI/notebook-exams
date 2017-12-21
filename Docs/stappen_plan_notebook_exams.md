# Stappen plan notebook exams

## 0. Work in progress

WORK IN PROGRESS  

1. Maak de bijbehorende "Docker file"
	1. Welke modules heb je nodig bovenop een stndaard Anaconda Python installatie?
	5. Wat moet er verder ingesteld worden?
	6. We kunnen de Docker file van te voren bekend maken via Dockerhub zodat men thuis alvast kan oefenen met de omgeving die je op het tentamen hebt.

## 1. Tentamen voorbereiden
1. Om vragen/antwoorden te definiëren in een notebook, kan in een Markdown-cell gebruik worden gemaakt van de `<answer>`-tag. De inhoud van de tag kan leeg zijn (niet automatisch nagekeken) of Python-code die evalueert naar `True` of `False`, waarin `X` het antwoord is. Op de plek van de tag verschijnt een invoermogelijkheid voor de student (mits het geen open vraag is).  
   * **Voorbeelden:**
	* Automatisch nagekeken vraag (twee punten): `<answer id="vraag-1" points="2">X == 'juiste antwoord'</answer>`
	* Niet automatisch nagekeken vraag: `<answer id="vraag-2" />`
	* Vraag met lang antwoord (meerdere regels): `<answer id="vraag-3" type="long" />`
	* Open vraag (bijv. code): `<answer id="code-vraag" type="open" />`
	* Bij het weglaten van het `points`-attribuut is de vraag standaard één punt waard.  
	
	* **Let er bij het specificeren van de antwoord-test op dat:**
		* ...het antwoord `X` een string is.
		* ...studenten mogelijk op verschillende manieren afronden of bijvoorbeeld een komma i.p.v. een punt gebruiken.
	* Te beperkt: `X == '0.2777'`
	* Beter: `float(X) == 0.2777`
	* Best: `round(float(X.replace(',', '.')), 3) == 0.277`



## 2. Tentamen opzetten

1. Tentamen opzetten: `notebook-exam setup exam EXAM_NAME EXAM_FILE`
	* Plaatst het tentamen op de hub, pakt het uit en slaat de tentamen-definitie op.
	* `EXAM_NAME` de korte naam van het tentamen (zonder spaties).
	* `EXAM_FILE` is het .zip-bestand met daarin het tentamen en eventueel questions.json

2. Checken: `notebook-exam list exams`
	* Geeft een overzicht van de tentamens die beschikbaar zijn op de hub.

3. Studenten opzetten: `notebook-exam setup students EXAM_NAME STUDENTS_FILE`
	* Zet de studentmappen op, voert permissies door en kopieert tentamenbestanden naar deze mappen.
	* `STUDENTS_FILE` is het excel bestand dat je van datanose download (moet dit formaat hebben)

4. Checken: `notebook-exam list students EXAM_NAME`

## 3. Tentamen afnemen

* Meer documentatie over cluster toevoegen
* Cluster opzetten: `notebook-exam provision cluster NUMBER_OF_WORKERS WORKER_FLAVOR`
	* **Dit kan een aantal minuten tot een uur duren.**
	* `WORKER_FLAVOR` is bijvoorbeeld `n1-standard-1`. Zie: https://cloud.google.com/compute/docs/machine-types

* Extra studenten toevoegen:
	* Op dit moment kan hiervoor gewoon `notebook-exam setup students EXAM_NAME STUDENTS_FILE` gebruikt worden. De bestaande studenten worden niet overschreven.

## 4. Tentamen nakijken

1. Inzendingen van studenten verzamelen: `notebook-exam grade collect-submissions EXAM_NAME`
	* Alle notebooks en de DataFrame met gesloten antwoorden worden gedownload en in de map 'all-submissions' geplaatst.
2. Inzendingen over nakijkers verdelen: `notebook-exam grade divide-submissions SUBMISSIONS_FOLDER GRADERS`
	* `SUBMISSIONS_FOLDER` is de map die in de vorige stap is aangemaakt.
	* `GRADERS` is een komma-gescheiden lijst van nakijkers. Voorbeeld: jantje,pietje
3. Voor het nakijken is een answer-model.json-bestand nodig. Dit bestand komt voort uit `notebook-exam prepare student-notebook`. Het bestand dient geplaatst te worden in de `SUBMISSIONS_FOLDER`.
3. Automatisch antwoorden nakijken (optioneel): `notebook-exam grade auto-score SUBMISSIONS_FOLDER ANSWER_MODEL_FILE`
	* `ANSWER_MODEL_FILE` is het hierboven genoemde answer-model.json
4. Er kan nu worden nagekeken in de notebooks.
	* Het is belangrijk om altijd eerst de cell met `import questions` te draaien (meestal de bovenste); door dit te doen worden de antwoorden en scores van de student ingeladen.
	* Scores die worden ingevuld worden automatisch opgeslagen.
	* Eventuele automatische scores kunnen overschreven worden.
5. Na het nakijken kunnen de resultaten van de verschillende nakijkers weer verzameld worden: `notebook-exam grade merge-results SUBMISSIONS_FOLDER`
	* De resultaten worden opgeslagen in all-results.csv. Hierop kan verdere analyse plaatsvinden.
6. Als laatste stap kunnen de cijfers berekend worden: `notebook-exam grade calculate-grades RESULTS_FILE MAXIMUM_SCORE`
	* `RESULTS_FILE` is het resultatenbestand uit de vorige stap.
	* `MAXIMUM_SCORE` is de hoogste haalbare score.
	
#### Analyse op antwoorden en resultaten
1. Je wilt een histogram kunne zien van de antwoorden op de gesloten vragen (omgekeerd geordend op aantal voorkomens van een antwoord).
2. en op basis daarvan de antwoord test kunnen aanpassen,
3.  en de gesloten vragen opnieuw automatisch (met de nieuwe tests) nakijken

## 5 Tentamen stats

1. We zetten alles om naar een dataframe: `nog aan te vullen`
2. berekenen stats per vraag en voor tentamen
3. berekenen een (gewogen) eindcijfer (weging via het aantal punten dat in de antwoord cellen is gegeven)
4. Pasen desnoods eea aan, en publiceren.  



