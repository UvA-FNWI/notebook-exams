# Documentatie notebook-exams

Het _notebook-exams_-platform maakt het mogelijk om op een gestroomlijnde manier programmeertentamens af te nemen met Jupyter Notebooks. Vooralsnog kan in deze notebooks met de Python-kernel (v2.7 en v3) gewerkt worden, maar in de toekomst kan ook ondersteuning voor onder andere R-kernels toegevoegd worden.

### Versie 1.0

Met deze versie van het platform is het volgende mogelijk:

* **Notebook-tentamens voorbereiden**: vragen/antwoorden definiëren, te verdienen punten specificeren, eventueel automatisch nagekeken vragen toevoegen en tenslotte een studentversie maken.
* **Tentamen afnemen op de Hub**: tentamenbestanden overzetten, studentmappen aanmaken en na afloop ingezonden notebooks weer verzamelen op één plek.
* **Tentamen automatisch nakijken**: waar mogelijk antwoorden van studenten automatisch nakijken en hun scores opslaan in één bestand.

## Roadmap
### Versie 1.1 (januari 2018)
* **Virtuele notebook-omgeving lokaal draaien**  
  Door middel van een Docker-image kan een student of docent op een eigen computer exact dezelfde omgeving opstarten als op de Hub. Dit biedt voor de studenten de volgende mogelijkheden:
  * De student kan voorafgaand aan een tentamen al bekend raken met aspecten van de omgeving waarin gewerkt dient te worden, zoals de module-versies die beschikbaar zijn.
  * Een volgende stap is dat de studenten hun wekelijkse opdrachten voor het vak standaard al binnen deze omgeving maken.  

  Voor de docent is het waardevol om notebooks van studenten na te kijken in exact dezelfde omgeving als waarin de studenten de notebooks hebben geschreven, aangezien zo fouten door bijvoorbeeld verschil in module-versies worden voorkomen.
  
  De beschikbaarheid van deze virtuele notebook-omgeving maakt het ook mogelijk om tentamens niet op de Hub, maar op tentamencomputers van de UvA of laptops van studenten af te nemen.
  
* **Notebooks interactief nakijken**  
  Wanneer een notebook-tentamen op de juiste manier is opgesteld, kunnen docenten en assistenten direct vanuit het notebook van een student punten toekennen aan antwoorden. Punten van automatisch nagekeken vragen kunnen eventueel overschreven worden. Na afloop kunnen alle scores per vraag en totaalscores in één bestand verzameld worden. 
  
* **Tentamen-resultaten uitgebreid inzien**  
  In het verlengde van het vorige punt wordt het mogelijk om de resultaten van het tentamen, die gebaseerd zijn op de automatisch gescoorde antwoorden en de handmatig toegekende scores, te genereren en in te zien. Hierbij kunnen automatisch statistieken per vraag worden opgesteld.

---

## Benodigdheden
Om alle benodigde software en modules te installeren dient het onderstaande commando uitgevoerd te worden in de terminal.

```
curl -q https://raw.githubusercontent.com/jessesar/notebook-exam-cli/master/install.sh?nocache | bash
```

_Dit installatiescript kan op dit moment alleen nog gebruikt worden op systemen met bash-ondersteuning, zoals Linux en Mac OS X._

Het notebook-exam-platform kan vervolgens worden aangesproken met het commando `notebook-exam`. Gebruik `notebook-exam --help` om meer informatie te krijgen over de beschikbare commando's.

## Stap voor stap een tentamen afnemen
In deze sectie zal stap voor stap beschreven worden hoe een tentamen in zijn volledigheid kan worden afgenomen met behulp van het notebook-exam-platform.

### 1. Tentamen voorbereiden
1. Met het voorbereiden van een tentamen wordt het voorbereiden van de tentamen-notebook en het definiëren/specificeren van vragen en antwoorden bedoeld.
2. Om vragen/antwoorden te definiëren in een notebook, kan in een Markdown-cell gebruik worden gemaakt van de `<answer>`-tag. De inhoud van de tag kan leeg zijn (niet automatisch nagekeken) of Python-code die evalueert naar `True` of `False`, waarin `X` het antwoord is. Op de plek van de tag verschijnt een invoermogelijkheid voor de student (mits het geen open vraag is).  
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

---

### 2. Tentamen opzetten

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

---

### 3. Tentamen afnemen

* Meer documentatie over cluster toevoegen
* Cluster opzetten: `notebook-exam provision cluster NUMBER_OF_WORKERS WORKER_FLAVOR`
	* **Dit kan een aantal minuten tot een uur duren.**
	* `WORKER_FLAVOR` is bijvoorbeeld `n1-standard-1`. Zie: https://cloud.google.com/compute/docs/machine-types

* Extra studenten toevoegen:
	* Op dit moment kan hiervoor gewoon `notebook-exam setup students EXAM_NAME STUDENTS_FILE` gebruikt worden. De bestaande studenten worden niet overschreven.

---

### 4. Tentamen nakijken

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
 



