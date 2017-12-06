# Stappen plan notebook exams

## 1 Maak en test het tentamen 

1. Maak het tentamen in een notebook met invulvragen en (open) programmeer en MarkDown vragen.
2. Zet eventuele data of andere files erbij.
3. Maak antwoordmodel, en test en run.
4. Geef elke vraag een aantal punten, wat je aangeeft in het `<antwoord>` veld met attribuut `p=REAL`.
3. Maak de bijbehorende "Docker file"
	4. Welke modules heb je nodig bovenop een stndaard Anaconda Python installatie?
	5. Wat moet er verder ingesteld worden?
	6. We kunnen de Docker file van te voren bekend maken via Dockerhub zodat men thuis alvast kan oefenen met de omgeving die je op het tentamen hebt.
4. *Test*
	5. peer review
	6. test om te zien hoeveel resources elke student moet krijgen tijdens tentamen

## 2 Set up servers

1. **Input**
	2. Datanose lijst?

## 3 Tentamen afnemen

1. Extra studenten toevoegen.
2. Login werkt niet
3. ...

## 4 Tentamen nakijken

We gaan uit van de volgende methode:

1. Nakijker doet run all cells in zelfde omgeving (gespcificeerd door dockerfile) als tentamen
2. Hierdoor worden de automatisch nagekeken vragen nagekeken.
3. Nu worden de open vragen met de hand nagekeken, en de score per vraag wordt ingevuld in het score-dict van die student.
	4. Hier moet iets handigs voor verzonnen worden. Liefst waarin je naast de score ook een opmerking per vraag/antwoord kunt plaatsen.
	
#### Gesloten vragen opnieuw draaien
1. Je wilt een histogram kunne zien van de antwoorden op de gesloten vragen (omgekeerd geordend op aantal voorkomens van een antwoord).
2. en op basis daarvan de antwoord test kunnen aanpassen,
3.  en de gesloten vragen opnieuw automatisch (met de nieuwe tests) nakijken

## 5 Tentamen stats

1. We zetten alles om naar een dataframe
2. berekenen stats per vraag en voor tentamen
3. berekenen een (gewogen) eindcijfer (weging via het aantal punten dat in de antwoord cellen is gegeven)
4. Pasen desnoods eea aan, en publiceren.  



