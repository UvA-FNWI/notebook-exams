# Documentatie notebook-exams

Het _notebook-exams_-platform maakt het mogelijk om op een gestroomlijnde manier programmeertentamens af te nemen met Jupyter Notebooks. Vooralsnog kan in deze notebooks met de Python-kernel (v2.7 en v3) gewerkt worden, maar in de toekomst kan ook ondersteuning voor onder andere R-kernels toegevoegd worden.

### Versie 1.1

Met deze versie van het platform is het volgende mogelijk:

* **Notebook-tentamens voorbereiden**: vragen/antwoorden definiëren, te verdienen punten specificeren, eventueel automatisch nagekeken vragen toevoegen en tenslotte een studentversie maken.
* **Tentamen afnemen op de Hub**: tentamenbestanden overzetten, studentmappen aanmaken en na afloop ingezonden notebooks weer verzamelen op één plek.
* **Tentamen automatisch nakijken**: waar mogelijk antwoorden van studenten automatisch nakijken en hun scores opslaan in één bestand.
* **Virtuele notebook-omgeving lokaal draaien** 
* **Notebooks interactief nakijken** 

Voor meer informatie over toekomstige versies, zie de roadmap.

---

## Benodigdheden
Om alle benodigde software en modules te installeren dient het onderstaande commando uitgevoerd te worden in de terminal.

```
curl -s https://raw.githubusercontent.com/jessesar/notebook-exam-cli/master/install.sh?nocache | bash
```

_Dit installatiescript kan op dit moment alleen nog gebruikt worden op systemen met bash-ondersteuning, zoals Linux en Mac OS X._

Het notebook-exam-platform kan vervolgens worden aangesproken met het commando `notebook-exam`. Gebruik `notebook-exam --help` om meer informatie te krijgen over de beschikbare commando's.

## Voorbereiding
In deze sectie zal stap voor stap beschreven worden hoe een tentamen in zijn volledigheid kan worden afgenomen met behulp van het notebook-exam-platform.

### 1. Tentamen lokaal opstellen
1. Met het opstellen van een tentamen wordt het voorbereiden van de tentamen-notebook en het definiëren/specificeren van vragen en antwoorden bedoeld.
2. Om vragen/antwoorden te definiëren in een notebook, kan in een Markdown-cell gebruik worden gemaakt van de `<answer>`-tag. 
	* **Types:**
	* `oneliner` (standaard) – een invulveld van één regel
	* `long` – een invulveld van meerdere regels
	* `markdown` – geen invulveld, wel een punten-aanduiding. Bijvoorbeeld voor vragen die een antwoord in Markdown vereisen.
	* `code` – geen invulveld, maar voegt automatisch een code-cell er onder in.
	* **Attributen:**
	* `id` (verplicht) – een unieke (onzichtbare) naam voor de vraag
	* `points` (standaard `1`) – het aantal punten dat de vraag waard is
	* `auto-score` (`true` of `false`, standaard `false`) – of de vraag automatisch nagekeken dient te worden. Slechts `oneliner`-vragen kunnen automatisch nagekeken worden. 
	* **Inhoud van de tag:**
	* Wanneer auto-score `false` is, kan de inhoud van de `answer`-tag een richtlijn voor het antwoord zijn die bij het nakijken wordt weergegeven.
	* Wanneer auto-score `true` is, dient de inhoud van de `answer`-tag een specificatie van het antwoord te zijn: Python-code die evalueert naar `True` of `False`, waarin `X` het antwoord is.
   * **Voorbeelden:**
   * Simpele invulvraag, niet automatisch nagekeken, geen antwoord-richtlijn: `<answer id="vraag-1" />`
   * Simpele invulvraag, 3 punten, wel automatisch nagekeken: `<answer id="vraag-2" points="3" auto-score="true">X == 5</answer>`
	* Invulvraag met lang antwoord (meerdere regels): `<answer id="vraag-3" type="long" />`
	* Markdown-vraag: `<answer id="markdown-vraag" type="markdown" />`
	* Code-vraag, code-cell wordt automatisch ingevoegd: `<answer id="code-vraag" type="code" />` 
	
	* **Let er bij het specificeren van de antwoord-test op dat:**
		* ...het antwoord `X` een string is.
		* ...studenten mogelijk op verschillende manieren afronden of bijvoorbeeld een komma i.p.v. een punt gebruiken.
	* Te beperkt: `X == '0.2777'`
	* Beter: `float(X) == 0.2777`
	* Best: `round(float(X.replace(',', '.')), 3) == 0.277`
3. Stel volgens de syntax die hierboven is beschreven een tentamen op in een Jupyter Notebook.
4. Vervolgens kan dit notebook omgezet worden in een studentversie; daarin verschijnen dan ook de invulvelden die voortkomen uit de syntax hierboven.  
   * Het omzetten in een studentversie kan met het volgende commando gedaan worden: `notebook-exam prepare student-notebook NOTEBOOK_FILE.ipynb`
   * Na het uitvoeren van dit commando zal er een nieuwe map met de titel van het notebook gemaakt zijn. In deze map bevinden zich twee mappen: `Teacher` en `Student`.  
   * De map `Student` bevat alles wat de student nodig heeft om het tentamen te maken (de notebook en een bestand met vraag-definities, die later gebruikt wordt om de juiste invulvelden te weergeven).  
   * Ook is er een zip-bestand aangemaakt met de titel van het notebook; dit zip-bestand heeft dezelfde inhoud als de `Student`-map en kan later gebruikt worden voor het opzetten van het tentamen op de Hub of voor het aanleveren van het tentamen aan bijv. de tentamenzaal.
   * De map `Teacher` bevat het notebook dat hierboven is gebruikt als 'template', en een map genaamd `Grading`. Deze map bevat een map `submissions` met daarin het voor nakijken benodigde antwoordmodel. In deze submissions-map kunnen handmatige inzendingen afkomstig uit bijvoorbeeld Blackboard worden geplaatst. Dit komt later aan bod.
5. Tenslotte is het belangrijk om de studentversie te testen. Navigeer op de commandolijn naar de `Student`-map en start daar de virtuele notebook-omgeving: `notebook-exam notebook start`. Dit kan de eerste keer een aantal minuten in beslag nemen.
6. Een Jupyter notebook-omgeving opent in de browser; dit is de omgeving waar studenten ook in zullen werken. Hierin kan de studentversie van het tentamen geopend worden om te checken of alles correct werkt. Als er wijzigingen nodig zijn, begin dan weer bij stap 2.

---

## A. Tentamen lokaal afnemen

### A2. Tentamen afnemen
Het zip-bestand met de studentversie dat is voortgekomen uit stap 1.4 kan uitgepakt geplaatst worden op het systeem waar het tentamen op wordt afgenomen (bijv. de tentamencomputers). Na afloop van het tentamen kan verder gegaan worden bij stap 4.

## B. Tentamen afnemen op Hub

### B2. Tentamen opzetten

1. Tentamen opzetten: `notebook-exam setup exam EXAM_NAME EXAM_FILE`
	* Plaatst het tentamen op de hub, pakt het uit en slaat de tentamen-definitie op.
	* `EXAM_NAME` de korte naam van het tentamen (zonder spaties).
	* `EXAM_FILE` is het .zip-bestand met daarin het tentamen en eventueel questions.json (bijvoorbeeld zoals aangemaakt bij stap 1.4)

2. Checken: `notebook-exam list exams`
	* Geeft een overzicht van de tentamens die beschikbaar zijn op de hub.

3. Studenten opzetten: `notebook-exam setup students EXAM_NAME STUDENTS_FILE`
	* Zet de studentmappen op, voert permissies door en kopieert tentamenbestanden naar deze mappen.
	* `STUDENTS_FILE` is het excel bestand dat je van datanose download (moet dit formaat hebben)

4. Checken: `notebook-exam list students EXAM_NAME`

---

### B3. Tentamen afnemen

* Meer documentatie over cluster toevoegen
* Cluster opzetten: `notebook-exam provision cluster NUMBER_OF_WORKERS WORKER_FLAVOR`
	* **Dit kan een aantal minuten tot een uur duren.**
	* `WORKER_FLAVOR` is bijvoorbeeld `n1-standard-1`. Zie: https://cloud.google.com/compute/docs/machine-types

* Extra studenten toevoegen:
	* Op dit moment kan hiervoor gewoon `notebook-exam setup students EXAM_NAME STUDENTS_FILE` gebruikt worden. De bestaande studenten worden niet overschreven.

* Na afloop inzendingen van studenten verzamelen: `notebook-exam grade collect-submissions EXAM_NAME`
	* Alle notebooks en de DataFrame met antwoorden worden gedownload en in de map 'hub-submissions' geplaatst.

---

## Nakijken

### 4. Tentamen nakijken

1. Inzendingen verzamelen:
   * Bij handmatige afname (A) worden de inzendingen via bijvoorbeeld TestVision of Blackboard opgehaald. De notebook-bestanden, of mappen met daarin notebook-bestanden, kunnen in de `submissions`-map uit stap 1.4 geplaatst worden.
   * Bij afname via de Hub (B) zijn alle inzendingen in de vorige stap automatisch verzameld en in de map `hub-submissions` geplaatst.
2. Automatisch antwoorden nakijken (optioneel): `notebook-exam grade auto-score SUBMISSIONS_FOLDER ANSWER_MODEL_FILE`
	* `ANSWER_MODEL_FILE` is het bestand `answer-model.json` dat zich in de inzendingen-map zal bevinden.
	* Scores worden automatisch bepaald aan de hand van het antwoordmodel en de scores worden opgeslagen.
3. Inzendingen over nakijkers verdelen: `notebook-exam grade divide-submissions SUBMISSIONS_FOLDER GRADERS`
	* `SUBMISSIONS_FOLDER` is de map met inzendingen. Dit is dus `submissions` in het geval van handmatige afname (A) of `hub-submissions` in het geval van afname via de Hub (B).
	* `GRADERS` is een komma-gescheiden lijst van nakijkers. Voorbeeld: jantje,pietje
	* Er wordt een nieuwe map gemaakt (`divided-submissions`) met daarin één map voor iedere nakijker.
	* Elke nakijkmap bevat alles wat voor nakijken nodig is: een deel van de notebooks, antwoordbestanden en het eventuele antwoordmodel. Een nakijker kan met slechts zijn of haar nakijkmap in bezit dus gewoon nakijken.
4. Er kan nu worden nagekeken in de notebooks. Dit wordt ook gedaan met de notebook-omgeving uit stap 1.5.
	* Navigeer naar je eigen nakijk-map en voer uit: `notebook-exam notebook start`
	* De notebook-omgeving start in een nieuw venster.
	* Het is belangrijk om altijd eerst de cell met `import questions` te draaien (meestal de bovenste); door dit te doen worden de antwoorden en scores van de student ingeladen.
	* Hierna zal het systeem proberen het studentnummer dat bij de inzending hoort te herkennen. Controleer dit en corrigeer het waar nodig.
	* Scores die worden ingevuld worden automatisch opgeslagen.
	* Eventuele automatische scores kunnen overschreven worden.
	* Alle scores worden opgeslagen in `student-answers.csv`.
5. Na het nakijken kunnen de resultaten van de verschillende nakijkers (de losse `student-answers.csv`-bestanden) weer verzameld en samengevoegd worden: `notebook-exam grade merge-results divided-submissions`
	* `divided-submissions` is de map met inzendingen verdeeld over nakijkers. Zorg dat al het nagekeken werk daar nog/opnieuw in staat.
	* De resultaten worden opgeslagen in `all-results.csv`. Hierop kan verdere analyse plaatsvinden.
6. Als laatste stap kunnen de cijfers berekend worden: `notebook-exam grade calculate-grades RESULTS_FILE MAXIMUM_SCORE`
	* `RESULTS_FILE` is het resultatenbestand uit de vorige stap.
	* `MAXIMUM_SCORE` is de hoogste haalbare score.
 



