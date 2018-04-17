# Howto: notebook-omgeving opstarten

In dit document wordt uitgelegd hoe je een notebook-omgeving in Docker kan opstarten. Dit is dezelfde omgeving die bij het tentamen gebruikt zal worden. Door nu al van deze omgeving gebruik te maken kan je er alvast bekend mee raken.

1. Download en installeer Docker:
	* **Mac OS X**: [https://download.docker.com/mac/stable/Docker.dmg](https://download.docker.com/mac/stable/Docker.dmg)
	* **Windows 10**: [https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)
	* **Linux**: gebruik dit commando in de terminal: `curl -fsSL get.docker.com | bash`

2. Installeer de `uva-notebook`-module met: `sudo pip install uva-notebook`
3. Zorg dat Docker draait en start de notebook-omgeving in de folder waarin je met Python wil gaan werken met: `uva-notebook start`
