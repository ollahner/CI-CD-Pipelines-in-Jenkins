Dokumentation
Projekt: einfache Python Flask API mit Jenkins CI/CD Pipeline.

Die API ist erreichbar unter:

http://localhost:5556/api/hello

Sie liefert eine JSON-Antwort mit:

message: Hello Spencer
counter: wird bei jedem Aufruf erhöht
status: success

Pipeline Ablauf

Source → Build → Test → Deployment

Source

Jenkins holt den Source Code aus dem GitHub Repository.

Build

Docker baut aus dem Projekt ein Image.

Befehl in der Pipeline:

docker build -t "$IMAGE_NAME" .

Test

Die Unit-Tests werden im Docker-Container ausgeführt.

Befehl in der Pipeline:

docker run --rm "$IMAGE_NAME" python -m pytest tests/test_hello.py -v

Deployment

Die Anwendung wird lokal als Docker-Container gestartet.

Befehl in der Pipeline:

docker run -d --name "$APP_NAME" -p "$APP_PORT:$APP_PORT" "$IMAGE_NAME"

Integration Test

Nach dem Deployment testet Jenkins die laufende API.

Befehl in der Pipeline:

docker run --rm --network "container:$APP_NAME" "$IMAGE_NAME" python tests/test_api.py

Verwendete Dateien

Jenkinsfile
Dockerfile
requirements.txt
src/hello.py
tests/test_hello.py
tests/test_api.py

Jenkins Setup

Jenkins wurde als Docker-Container gestartet.

Dabei wurde der Docker-Socket vom Host eingebunden, damit Jenkins Docker-Befehle ausführen kann.

Jenkins läuft unter:

http://localhost:8080

Im Jenkins-Container wurde Docker geprüft mit:

docker --version

Jenkins Job

In Jenkins wurde ein Pipeline Job erstellt.

Name: hello-spencer-pipeline
Typ: Pipeline
Definition: Pipeline script from SCM
SCM: Git
Repository: GitHub Repository
Branch: main
Script Path: Jenkinsfile

Ergebnis

Der Jenkins Build läuft erfolgreich durch.

Source: erfolgreich
Build: erfolgreich
Test: erfolgreich
Deployment: erfolgreich
Integration Test: erfolgreich

Die Anwendung läuft danach lokal als Docker-Container.

Container: hello-spencer
Port: 5556:5556