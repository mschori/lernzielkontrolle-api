# Tie-BE-Athena-API README

Herzlich willkommen zum tie-athena-api Projekt! Dieses README enthält wesentliche Informationen, um mit dem
Projekt zu beginnen.

## Projektübersicht

Dieses Django-Projekt dient als Backend für unsere Athena Webanwendung. Wir verwenden eine
PostgreSQL-Datenbank, um Daten zu speichern und zu verwalten. Sensible Schlüssel und Konfigurationen werden aus
Sicherheitsgründen in Umgebungsvariablen gespeichert.

### Technologien
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Erste Schritte

Folge diesen Anweisungen, um unser Athena Projekt lokal einzurichten und auszuführen.

### Voraussetzungen

Bevor du beginnst, stelle sicher, dass die folgenden Komponenten auf deiner Entwicklungsplattform installiert sind:

- [Python](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [PostgreSQL](https://www.postgresql.org/download/)

### Installation

1. Klone das Repository auf deine lokale Maschine:

   ```
   git clone <Repository-URL>
   cd tie-be-athena-api
   ```

2. Erstelle eine virtuelle Umgebung:

   ```
   virtualenv venv
   source venv/bin/activate
   ```

3. Installiere die Projektabhängigkeiten:

   ```
   pip install -r requirements.txt
   ```

4. Konfiguriere deine Umgebungsvariablen:
    - Erstelle eine `.env`-Datei im Hauptverzeichnis des Projekts.
    - Füge die erforderlichen Umgebungsvariablen für unser Projekt hinzu, einschliesslich der
      Datenbankanmeldeinformationen, des geheimen Schlüssels und anderer sensibler Informationen.

   Beispielhafte `.env`-Datei (.env.example):

   ```
   SECRET_KEY=***
   DEBUG=True
   ENABLE_HTTPS_REDIRECT=False
   DB_HOST=localhost
   DB_NAME=***
   DB_USER=***
   DB_PASSWORD=***
   DB_PORT=5432
   CORS_ORIGIN_WHITELIST=***
   FIREBASE_TYPE=***
   FIREBASE_PROJECT_ID=***
   FIREBASE_PRIVATE_KEY_ID=***
   FIREBASE_PRIVATE_KEY=***
   FIREBASE_CLIENT_EMAIL=***
   FIREBASE_CLIENT_ID=***
   FIREBASE_AUTH_URI=***
   FIREBASE_TOKEN_URI=***
   FIREBASE_AUTH_PROVIDER=***
   FIREBASE_CLIENT_CERT_URL=***
   ```

5. Wende Migrationen an, um die Datenbanktabellen zu erstellen:

   ```
   python manage.py migrate
   ```

6. Erstelle ein Superuser-Konto, um auf das Django-Admin-Panel zuzugreifen:

   ```
   python manage.py createsuperuser
   ```

7. Starte den Entwicklungsserver:

   ```
   python manage.py runserver
   ```

8. Öffne deinen Webbrowser und navigiere zu [http://localhost:8000/](http://localhost:8000/), um auf unser Projekt
   zuzugreifen.

## Projektstruktur

Die Projektstruktur deines Athena Backend-Projekts lässt sich grob wie folgt zusammenfassen:

**Hauptverzeichnis:**

- `README.md`: Dokumentationsdatei mit wichtigen Informationen zum Projekt.
- `manage.py`: Django-Management-Skript für verschiedene Projektaufgaben.
- `requirements.txt`: Liste der benötigten Python-Pakete und deren Versionen.

**tie-be-athena-api (Hauptverzeichnis des Django-Projekts):**

- `settings.py`: Konfigurationsdatei für das Django-Projekt, einschliesslich Datenbankverbindung und Einstellungen.
- `urls.py`: Definiert die URL-Routing-Regeln für das Projekt.
- `wsgi.py`: Konfigurationsdatei für den WSGI-Server (für die Bereitstellung).
- `asgi.py`: Konfigurationsdatei für den ASGI-Server (für asynchrone Anwendungen).

**templates:** Verzeichnis für HTML-Templates, die in den Ansichten verwendet werden (WIRD NICHT VERWENDET).

**users (Django-App für Benutzerverwaltung):**

- `models.py`: Definiert Datenbankmodelle für Benutzer und andere relevante Informationen.
- `views.py`: Enthält Ansichtsfunktionen, die aufgerufen werden, wenn Benutzer auf bestimmte URLs zugreifen.
- `admin.py`: Ermöglicht die Verwaltung von Benutzerdaten über das Django-Admin-Panel.

**Projektverzeichnisstruktur im Tree-Format:**

```
├── README.md
├── manage.py
├── requirements.txt
├── tie-be-athena-api
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── managers.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```


