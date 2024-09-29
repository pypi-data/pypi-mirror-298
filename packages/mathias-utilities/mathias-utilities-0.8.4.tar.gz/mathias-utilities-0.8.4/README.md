# Mathias Extension

mathias-ext ist ein privates Console-Tool, das die Verwaltung und Bearbeitung von Webprojekten sowie Dateien und Ordnern vereinfacht.


## Installation

```bash
pip install mathias-ext
```


## Verwendung

Verwende die folgenden Befehle in der Konsole, um verschiedene Funktionen der Extension zu nutzen.


### Befehle:

| Befehl                              | Beschreibung                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| `createweb PROJEKTNAME`             | Erstellt ein neues Webprojekt mit den Dateien `index.html`, `style.css`, `script.js`. |
| `deleteweb PROJEKTNAME`             | Löscht ein Webprojekt und alle enthaltenen Dateien.                         |
| `listprojects`                      | Listet alle Webprojekte im aktuellen Verzeichnis auf.                       |
| `addfile PROJEKTNAME DATEINAME`     | Fügt eine neue Datei zu einem bestehenden Projekt hinzu.                    |
| `renameproject OLD_NAME NEW_NAME`   | Benennt ein Projekt um.                                                     |
| `viewfile [PROJEKTNAME DATEINAME]`  | Zeigt den Inhalt einer Datei an.                                             |
| `clearproject PROJEKTNAME`          | Löscht alle Dateien im Projekt, behält aber das Verzeichnis.                |
| `backup PROJEKTNAME [CUSTOM_NAME]`  | Erstellt ein Backup eines Projekts.                                          |
| `restore BACKUPNAME`                | Stellt ein Projekt aus einem Backup wieder her.                             |
| `listbackups`                       | Listet alle verfügbaren Backups auf.                                        |
| `zip PROJEKTNAME [ZIP_NAME]`        | Archiviert ein Projekt oder einen Ordner in eine ZIP-Datei.                 |
| `search WORT [FOLDER]`              | Durchsucht alle Dateien in einem Projekt oder Ordner nach einem bestimmten Begriff. |
| `open PATH/FOLDERNAME`              | Öffnet eine Datei oder einen Ordner im Dateisystem.                         |
| `openvs FILE/FOLDER/PATH`           | Öffnet eine Datei oder einen Ordner in Visual Studio Code.                  |
| `help` / `?`                        | Zeigt eine Hilfe mit allen verfügbaren Befehlen an.                         |


### Voraussetzungen:

- Python 3.x


## Support:

Für Hilfe und Support:
- Discord: [https://discord.gg/HPMPbtSnKj](https://discord.gg/HPMPbtSnKj)


## Lizenz:

Dieses Projekt steht unter der folgender [Lizenz](LICENSE).