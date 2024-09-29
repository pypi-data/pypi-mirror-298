import os
import sys
import shutil
from datetime import datetime
import subprocess


backup_base_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'mathias-ext', 'Backups')

os.makedirs(backup_base_dir, exist_ok=True)

def create_web_project(project_name):
    os.makedirs(project_name, exist_ok=True)
    files = {
    "index.html": f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style.css">
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        <script src="script.js"></script>
        <title>{project_name}</title>
    </head>
    <body>
        <div class="container">
            <h1>Willkommen auf {project_name}</h1>
        </div>
    </body>
</html>
            """,
            "style.css": """body {
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; 
  background-color: #141414;
  font-family: 'Inter', sans-serif;
  color: white;
}

.text {
  color: #333;
  text-align: center;
  margin-top: 50px;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #505050;
  width: 50%;;
}
            """,
                "script.js": f"console.log('Willkommen auf {project_name}');"
            }

    
    for file_name, content in files.items():
        file_path = os.path.join(project_name, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
    
    print(f"Projekt '{project_name}' wurde erfolgreich erstellt mit den Dateien: {', '.join(files.keys())} unter {os.path.abspath(project_name)}")

def delete_web_project(project_name):
    if os.path.exists(project_name):
        shutil.rmtree(project_name)
        print(f"Projekt '{project_name}' wurde gelöscht.")
    else:
        print(f"Projekt '{project_name}' wurde nicht gefunden.")

def list_projects():
    projects = [name for name in os.listdir('.') if os.path.isdir(name)]
    if projects:
        print("Vorhandene Projekte:")
        for project in projects:
            print(f"- {project}")
    else:
        print("Keine Projekte gefunden.")

def add_file_to_project(project_name, file_name):
    if not os.path.exists(project_name):
        print(f"Projekt '{project_name}' existiert nicht.")
        return

    file_path = os.path.join(project_name, file_name)
    with open(file_path, 'w') as file:
        file.write(f"// {file_name} - hinzugefügt zu {project_name}")
    
    print(f"Datei '{file_name}' wurde zu '{project_name}' hinzugefügt.")

def rename_project(old_name, new_name):
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"Projekt '{old_name}' wurde in '{new_name}' umbenannt.")
    else:
        print(f"Projekt '{old_name}' wurde nicht gefunden.")



def open_in_vscode(target):
    vscode_path = shutil.which("code")  
    
    if vscode_path is None:
        print("VS Code 'code' Befehl wurde nicht gefunden. Bitte stelle sicher, dass VS Code installiert ist und der 'code' Befehl im PATH enthalten ist.")
        return
    
    if os.path.exists(target):
        try:
            subprocess.run([vscode_path, target, "--new-window"]) 
            print(f"'{target}' wurde in einem neuen Visual Studio Code Fenster geöffnet.")
        except Exception as e:
            print(f"Fehler beim Öffnen von '{target}' in VSCode: {e}")
            print({target})
    else:
        print(f"'{target}' existiert nicht.")

def view_file(project_name=None, file_name=None):
    if project_name and file_name:  
        file_path = os.path.join(project_name, file_name)
    elif file_name:  
        file_path = file_name
    else:
        print("Verwendung: mathias viewfile PROJEKTNAME DATEINAME oder mathias viewfile DATEIPFAD")
        return

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            print(file.read())
    else:
        print(f"Datei '{file_path}' wurde nicht gefunden.")


def remove_readonly(func, path, exc_info):
    """Versucht, schreibgeschützte Dateien zu entfernen."""
    os.chmod(path, 0o777)  
    func(path)


def clear_project(project_name):
    if os.path.exists(project_name):
        for file_name in os.listdir(project_name):
            file_path = os.path.join(project_name, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Alle Dateien im Projekt '{project_name}' wurden gelöscht.")
    else:
        print(f"Projekt '{project_name}' wurde nicht gefunden.")


def backup_project(project_name, custom_name=None):
    if not os.path.exists(project_name):
        print(f"Projekt '{project_name}' existiert nicht.")
        return

    if custom_name:
        backup_name = custom_name
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{project_name}_backup_{timestamp}"

    backup_path = os.path.join(backup_base_dir, backup_name)

    shutil.copytree(project_name, backup_path)
    
    print(f"Backup von '{project_name}' wurde erfolgreich in '{backup_path}' erstellt.")

def archive_project_or_folder(target, zip_name=None):
    if os.path.exists(target):
        if zip_name is None:
            zip_name = os.path.basename(target) 

        shutil.make_archive(zip_name, 'zip', target)
        print(f"'{target}' wurde erfolgreich als '{zip_name}.zip' archiviert.")
    else:
        print(f"'{target}' existiert nicht.")

def restore_project(backup_name):
    backup_path = os.path.join(backup_base_dir, backup_name)

    if not os.path.exists(backup_path):
        print(f"Backup '{backup_name}' existiert nicht im Backup-Verzeichnis.")
        return

    project_name = backup_name.split('_backup_')[0]

    if os.path.exists(project_name):
        shutil.rmtree(project_name) 
        print(f"Projekt '{project_name}' wurde gelöscht, um das Backup wiederherzustellen.")

    try:
        shutil.copytree(backup_path, project_name)  
        print(f"Projekt '{project_name}' wurde erfolgreich aus dem Backup '{backup_name}' wiederhergestellt.")
    except PermissionError as e:
        print(f"Fehler beim Wiederherstellen des Projekts '{project_name}': {e}")


def search_in_project_or_folder(target, search_term):
    if not os.path.exists(target):
        print(f"'{target}' existiert nicht.")
        return

    found = False
    if os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        for line_number, line in enumerate(f, start=1):
                            if search_term in line:
                                print(f"'{search_term}' gefunden in: {file_path}, Zeile {line_number}: {line.strip()}")
                                found = True
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei '{file_path}': {e}")
    else:
        try:
            with open(target, 'r', errors='ignore') as f:
                for line_number, line in enumerate(f, start=1):
                    if search_term in line:
                        print(f"'{search_term}' gefunden in: {target}, Zeile {line_number}: {line.strip()}")
                        found = True
        except Exception as e:
            print(f"Fehler beim Lesen der Datei '{target}': {e}")

    if not found:
        print(f"'{search_term}' wurde in '{target}' nicht gefunden.")

def open_path_or_folder(target):
    if os.path.exists(target):
        if os.path.isdir(target):
            try:
                if sys.platform == "win32":
                    os.startfile(target)  # Windows
                elif sys.platform == "darwin":
                    subprocess.run(["open", target])  # macOS
                else:
                    subprocess.run(["xdg-open", target])  # Linux
                print(f"'{target}' wurde geöffnet.")
            except Exception as e:
                print(f"Fehler beim Öffnen von '{target}': {e}")
        elif os.path.isfile(target):
            try:
                if sys.platform == "win32":
                    os.startfile(target)  # Windows
                elif sys.platform == "darwin":
                    subprocess.run(["open", target])  # macOS
                else:
                    subprocess.run(["xdg-open", target])  # Linux
                print(f"Datei '{target}' wurde geöffnet.")
            except Exception as e:
                print(f"Fehler beim Öffnen der Datei '{target}': {e}")
        else:
            print(f"'{target}' ist kein gültiger Pfad.")
    else:
        print(f"'{target}' existiert nicht.")

def list_backups():
    if os.path.exists(backup_base_dir):
        backups = [name for name in os.listdir(backup_base_dir) if os.path.isdir(os.path.join(backup_base_dir, name))]
        if backups:
            print("Verfügbare Backups:")
            for backup in backups:
                print(f"- {backup}")
        else:
            print("Keine Backups gefunden.")
    else:
        print(f"Backup-Verzeichnis '{backup_base_dir}' existiert nicht.")

def show_help(command=None):
    if command == "commands":
        print("""
        Verfügbare Befehle:
        -------------------------
        createweb PROJEKTNAME                       - Erstellt ein neues Webprojekt mit dem angegebenen Namen.
        listprojects                                - Listet alle erstellten Projekte auf.
        addfile PROJEKTNAME DATEINAME               - Fügt eine neue Datei zu einem bestehenden Projekt hinzu.
        renameproject OLD_NAME NEW_NAME             - Benennt ein Projekt um.
        viewfile [PROJEKTNAME DATEINAME]/[PATH]     - Zeigt den Inhalt einer Datei an.
        clearproject PROJEKTNAME                    - Löscht alle Dateien in einem Projekt, behält aber das Verzeichnis.
        backup PROJEKTNAME [CUSTOM_NAME]            - Erstellt ein Backup eines Projekts.
        restore BACKUPNAME                          - Stellt ein Projekt aus einem Backup wieder her.
        listbackups                                 - Listet alle verfügbaren Backups auf.
        zip PROJEKTNAME [ZIP_NAME] / [PFAD]         - Archiviert ein Projekt oder einen Ordner in ein ZIP-Archiv.
        search WORT [FOLDER]                        - Durchsucht alle Dateien in einem Projekt oder Verzeichnis nach dem angegebenen Wort.
        open PATH/FOLDERNAME                        - Öffnet eine Datei oder einen Ordner im Dateisystem.
        openvs FILE/FOLDER/PATH                     - Öffnet eine Datei oder einen Ordner in einem neuen Visual Studio Code Fenster.
        help | ?                                    - Zeigt diese Hilfe an.
        """)
    elif command == "support":
        print(""" 
        Support Befehle:
        -------------------------
        Discord: https://discord.gg/HPMPbtSnKj
        """)
    else:
        print("""
        Mathias Ext - Hilfe:
              
              Author: Mathias
              version: 0.8.4
              
        -------------------------
        Benutze 'mathias help commands', um eine Liste der verfügbaren Befehle zu erhalten.
        Benutze 'mathias help support', um eine Liste von Kontaktmöglichkeiten zu erhalten.
        """)



def main():
    if len(sys.argv) == 1:
        show_help()  
        sys.exit(0)

    command = sys.argv[1]

    if command == "help":
        if len(sys.argv) > 2:
            show_help(sys.argv[2])  
        else:
            show_help()  
        sys.exit(0)
    
    if command == 'createweb':
        if len(sys.argv) < 3:
            print("Verwendung: mathias createweb PROJEKTNAME")
            sys.exit(1)
        project_name = sys.argv[2]
        create_web_project(project_name)

    elif command == 'openvs':
        if len(sys.argv) < 3:
            print("Verwendung: mathias openvs FILE/FOLDER/PATH")
            sys.exit(1)
        target = sys.argv[2]
        open_in_vscode(target)

    elif command == 'listprojects':
        list_projects()

    elif command == 'addfile':
        if len(sys.argv) < 4:
            print("Verwendung: mathias addfile PROJEKTNAME DATEINAME")
            sys.exit(1)
        project_name = sys.argv[2]
        file_name = sys.argv[3]
        add_file_to_project(project_name, file_name)

    elif command == 'open':
            if len(sys.argv) < 3:
                print("Verwendung: mathias open PATH/FOLDERNAME")
                sys.exit(1)
            target = sys.argv[2]
            open_path_or_folder(target)

    elif command == 'renameproject':
        if len(sys.argv) < 4:
            print("Verwendung: mathias renameproject OLD_NAME NEW_NAME")
            sys.exit(1)
        old_name = sys.argv[2]
        new_name = sys.argv[3]
        rename_project(old_name, new_name)

    elif command == 'viewfile':
        if len(sys.argv) < 3:
            print("Verwendung: mathias viewfile PROJEKTNAME DATEINAME oder mathias viewfile DATEIPFAD")
            sys.exit(1)
        if os.path.isfile(sys.argv[2]):
            file_path = sys.argv[2]
            view_file(file_name=file_path)
        else:
            project_name = sys.argv[2]
            if len(sys.argv) < 4:
                print("Verwendung: mathias viewfile PROJEKTNAME DATEINAME")
                sys.exit(1)
            file_name = sys.argv[3]
            view_file(project_name, file_name)

    elif command == 'search':
        if len(sys.argv) < 3:
            print("Verwendung: mathias search WORT oder mathias search WORT FOLDER")
            sys.exit(1)

        search_term = sys.argv[2]

        if len(sys.argv) == 3:
            current_dir = os.getcwd() 
            search_in_project_or_folder(current_dir, search_term)
        else:
            target = sys.argv[3]
            search_in_project_or_folder(target, search_term)


    elif command == 'clearproject':
        if len(sys.argv) < 3:
            print("Verwendung: mathias clearproject PROJEKTNAME")
            sys.exit(1)
        project_name = sys.argv[2]
        clear_project(project_name)

    elif command == 'zip':
        if len(sys.argv) < 3:
            print("Verwendung: mathias archive PROJEKTNAME [ZIP_NAME] oder mathias archive PFAD")
            sys.exit(1)

        target = sys.argv[2]
        zip_name = sys.argv[3] if len(sys.argv) > 3 else None
        archive_project_or_folder(target, zip_name)


    elif command == 'backup':
        if len(sys.argv) < 3:
            print("Verwendung: mathias backup PROJEKTNAME [CUSTOM_NAME]")
            sys.exit(1)
        project_name = sys.argv[2]
        custom_name = sys.argv[3] if len(sys.argv) > 3 else None
        backup_project(project_name, custom_name)

    elif command == 'listbackups':
        list_backups()

    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Verwendung: mathias restore BACKUPNAME")
            sys.exit(1)
        backup_name = sys.argv[2]
        restore_project(backup_name)

    else:
        print(f"Unbekannter Befehl: {command}")
        show_help()
        sys.exit(1)



if __name__ == "__main__":
    main()
