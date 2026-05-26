# CI/CD Pipeline in Jenkins - Hello Spencer

Dieses Projekt ist eine kleine Flask-API fuer die Jenkins-CI/CD-Uebung.
Die Pipeline enthaelt die geforderten Schritte:

1. Source: Repository wird von GitHub ausgecheckt.
2. Build: Docker-Image der Applikation wird gebaut.
3. Test: Unit-Tests laufen im gebauten Docker-Image.
4. Deployment: Die Anwendung wird lokal als Docker-Container gestartet.
5. Integration Test: Die laufende API wird ueber `/api/hello` getestet.

## Anwendung lokal starten

```powershell
docker build -t hello-spencer:local .
docker rm -f hello-spencer
docker run -d --name hello-spencer -p 5556:5556 hello-spencer:local
curl http://localhost:5556/api/hello
```

Erwartete Antwort:

```json
{
  "counter": 1,
  "message": "Hello Spencer",
  "status": "success"
}
```

## Tests lokal ausfuehren

Ohne lokale Python-Abhaengigkeiten:

```powershell
docker build -t hello-spencer:test .
docker run --rm hello-spencer:test python -m pytest tests/test_hello.py -v
```

Integrationstest gegen einen laufenden Container:

```powershell
docker run --rm --network container:hello-spencer hello-spencer:test python tests/test_api.py
```

## Jenkins einrichten

Jenkins mit Docker-Socket starten:

```powershell
docker volume create jenkins_home
docker run -u root -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:latest
```

Initiales Admin-Passwort auslesen:

```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Danach in Jenkins unter `http://localhost:8080`:

1. Suggested Plugins installieren.
2. Admin-User anlegen.
3. Zusaetzlich Docker-relevante Plugins installieren, falls sie nicht vorhanden sind.
4. Pruefen, ob Docker im Jenkins-Container verfuegbar ist:

```powershell
docker exec -it jenkins bash
docker --version
```

Falls `docker: command not found` erscheint, im Jenkins-Container die Docker-CLI installieren:

```bash
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y docker-ce-cli
```

## Jenkins Pipeline Job

1. In Jenkins `New Item` waehlen.
2. `Pipeline` auswaehlen.
3. Unter `Build Triggers` optional `GitHub hook trigger for GITScm polling` aktivieren.
4. Unter `Pipeline` die Option `Pipeline script from SCM` waehlen.
5. SCM: `Git`.
6. Repository URL: eigenes GitHub-Repository eintragen.
7. Branch: `main`.
8. Script Path: `Jenkinsfile`.
9. Speichern und `Build Now` ausfuehren.

Fuer automatische Builds nach GitHub-Commits brauchst du zusaetzlich einen GitHub Webhook:

- Payload URL: `http://<deine-jenkins-url>/github-webhook/`
- Content type: `application/json`
- Event: `Just the push event`

Bei lokalem Jenkins auf dem Notebook ist ein echter GitHub-Webhook nur moeglich, wenn Jenkins von GitHub erreichbar ist, zum Beispiel ueber ngrok oder einen Server.

## Brauche ich eine zweite Person?

Technisch brauchst du keine zweite Person, um Jenkins, Docker, Tests und Deployment umzusetzen.
In der Bewertung steht aber `Gruppengroesse: 2 Personen`. Das ist organisatorisch gemeint: Die Abgabe soll vermutlich in Zweiergruppen erfolgen. Wenn du alleine abgeben willst, solltest du kurz bei der Lehrperson nachfragen.

Sinnvolle Aufteilung in einer Zweiergruppe:

- Person 1: Jenkins Setup, GitHub Webhook, Pipeline-Konfiguration.
- Person 2: Flask-App, Unit-Tests, Dockerfile, Deployment-Test.
