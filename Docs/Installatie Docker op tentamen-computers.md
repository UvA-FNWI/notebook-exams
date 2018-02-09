## Installatie Docker op tentamen-computers

Docker is software waarmee applicaties gevirtualiseerd en in een eigen, afgesloten omgeving kunnen worden gedraaid. Docker kan voor het afnemen van notebook-tentamens een uitkomst bieden: de benodigde software (Python, Jupyter Notebooks, specifieke Python-modules) kunnen aangeboden worden in een zogenaamd Docker *image* en hoeven niet op de tentamen-computers geïnstalleerd te worden. Het programmeerwerk wordt dan ook binnen Docker gedaan en kan de tentamen-computer niet beïnvloeden.    

Docker kan out-of-the-box draaien op Windows 10. Echter draaien de tentamen-computers op Windows 7.

* Is het mogelijk om Windows 10 te draaien zodat Docker out-of-the-box werkt?
	* Zo ja, dan kan Docker geïnstalleerd worden met: [https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)
	* Zo nee, dan is de enige manier om Docker te draaien met Docker Toolbox. Dit kan geïnstalleerd worden m.b.v. het volgende stappenplan: [https://docs.docker.com/toolbox/toolbox\_install\_windows/](https://docs.docker.com/toolbox/toolbox_install_windows/)

Als Docker op één van bovenstaande manieren geïnstalleerd kan worden, is het draaien van een notebook-tentamen eenvoudig. De benodigde Docker-image (= de specificatie van de omgeving waarin de studenten moeten werken) is reeds beschikbaar en kan worden opgehaald met het volgende terminal-commando:

`docker pull notebookexams/uva-notebook`

Het ophalen van de image kan enkele minuten duren en enkele gigabytes aan schijfruimte in beslag nemen.

Elke student dient een voor hem/haar toegankelijke map te hebben; denk bijvoorbeeld aan de thuismap van de student. Dit is de map waar de student via Jupyter Notebook in zal werken.
In deze map dient het bestand `jupyter_config.py` te staan met de volgende inhoud:

```
c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = u''
c.NotebookApp.disable_check_xsrf = True
```

Hierna kan de Docker-container opgestart worden. Let op dat op de plek van `*STUDENT-MAP*` het pad naar de hierboven besproken student-map dient te staan.

```
docker run -d -p 8123:8888 -e STUDENT_QUESTIONS_FILE='questions.json' -e STUDENT_ANSWERS_FILE='answers.json' --mount type=bind,source=*STUDENT-MAP*,target=/var/host-files notebookexams/uva-notebook jupyter notebook --ip=0.0.0.0 --allow-root --config=/var/host-files/jupyter_config.py /var/host-files/
```

Als alles goed gaat kan vervolgens op `http://localhost:8123/` de notebook-omgeving geopend worden.

### Alternatief
Mocht het installeren van Docker op de tentamen-computers absoluut onmogelijk blijken, dan is het alternatief om de laatste versie van Anaconda te installeren. Anaconda is een gemakkelijke manier om Python en een flink aantal veelgebruikte modules op een gebruiksvriendelijke manier te installeren. In dat geval draait Python, en de code van studenten, dus wel direct op de tentamen-computer.

Anaconda voor Python 3.6 kan geïnstalleerd worden met: [https://repo.continuum.io/archive/Anaconda3-5.0.1-Windows-x86_64.exe](https://repo.continuum.io/archive/Anaconda3-5.0.1-Windows-x86_64.exe)
