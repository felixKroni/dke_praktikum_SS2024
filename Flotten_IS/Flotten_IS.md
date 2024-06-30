# Flotten IS - Projekt Setup
Folgen Sie diesen Schritten, um das Flotten_IS Projekt auf einem Linux-System einzurichten. Sollten Sie das Projektsetup bereits ausgeführt haben, können Sie direkt zum Punkt [Starten Sie die Anwendung](#starten-sie-die-anwendung) springen. Vergessen Sie nicht davor die [virtuelle Umgebung zu aktivieren](#aktivieren-sie-die-virtuelle-umgebung).


## Erstellen Sie eine virtuelle Umgebung
1. Navigieren Sie in das Verzeichnis `Flotten_IS` (Ausgehend vom Hauptverzeichnis des Projekts).
2. Führen Sie den folgenden Befehl aus, um eine virtuelle Umgebung namens `venv` zu erstellen:

```bash
python3 -m venv venv
```

## Aktivieren Sie die virtuelle Umgebung
Führen Sie den folgenden Befehl aus, um die virtuelle Umgebung zu aktivieren:
```bash
source venv/bin/activate
```

## Installieren Sie die Dependencies
Stellen Sie sicher, dass Sie sich im Hauptverzeichnis des Projekts befinden (dort, wo die requirements.txt Datei liegt). Führen Sie dann den folgenden Befehl aus, um die Anforderungen zu installieren:
```bash
pip install -r requirements.txt
```

## Starten Sie die Anwendung
Führen Sie den folgenden Befehl aus, um die Anwendung zu starten:
```bash
flask run --port=5002
```

## Account für den Login
Username: 
```bash
Admin
```
Password:
```bash
1234
```

# Dokumentation der Anwendung
Das Projekt ist eine Webanwendung, die mit dem Flask-Framework in Python erstellt wurde. Es verwendet SQLAlchemy als ORM (Object-Relational Mapper) für die Datenbankinteraktionen und Flask-Login für die Benutzerauthentifizierung.

## Mockup
Der Prototyp der Webanwendung mithilfe von Figma wurden erstellt: 

https://www.figma.com/design/ZxCk05vwXu4zcJQQzH3z5U/Untitled?node-id=0-1&t=99nz61oLgTt7cETS-0 

## Die Klassen
Die wichtigsten Klassen in diesem Projekt sind User, Wagen (Triebwagen und Personenwagen), Zug und Wartung, die in der `models.py` Datei definiert sind. Jede dieser Klassen repräsentiert eine Tabelle in der Datenbank.


#### 1. User

Diese Klasse repräsentiert einen Benutzer der Anwendung. Sie hat Attribute wie `username`, `email` und `password_hash`. Methoden zur Passwortüberprüfung und -setzung sind ebenfalls vorhanden. Außerdem kann ein Benutzer als Mitarbeiter Wartungen zugewiesen werden.

#### 2. Wagen
Diese abstrakte Klasse repräsentiert einen allgemeinen Wagen und dient als Basisklasse für spezifischere Wagengruppen. Sie hat Attribute wie `wagennummer` und `spurweite`.

#### 3. Triebwagen
Diese Klasse erbt von der Klasse `Wagen` und repräsentiert einen Triebwagen. Sie hat zusätzlich das Attribut `maxZugkraft`. Ein Triebwagen kann genau einem Zug zugeordnet werden.

#### 4. Personenwagen
Diese Klasse erbt ebenfalls von der Klasse `Wagen` und repräsentiert einen Personenwagen. Sie hat zusätzliche Attribute wie `sitzanzahl` und `maximalgewicht`. Ein Personenwagen kann einem Zug zugeordnet werden.

#### 5. Zug
Diese Klasse repräsentiert einen Zug und hat Attribute wie `zug_nummer`, `zug_name` und `triebwagen_nr`. Ein Zug besteht aus einem Triebwagen und mehreren Personenwagen. Ein Zug kann auch mehrere Wartungen haben.

#### 6. Wartung
Diese Klasse repräsentiert eine Wartung für einen Zug. Sie hat Attribute wie `wartung_nr`, `zug_nummer`, `start_time` und `end_time`. Eine Wartung kann mehreren Benutzern als Mitarbeiter zugewiesen werden und gehört zu einem Zug.

### Beziehungen zwischen den Klassen:
- **User als Mitarbeiter und Wartung:** Ein Benutzer kann mehreren Wartungen zugewiesen werden (many-to-many Beziehung).
- **Wagen und Triebwagen/Personenwagen:** Triebwagen und Personenwagen erben von Wagen (Vererbung).
- **Zug und Triebwagen:** Ein Zug hat genau einen Triebwagen (one-to-one Beziehung).
- **Zug und Personenwagen:** Ein Zug kann mehrere Personenwagen haben (one-to-many Beziehung).
- **Zug und Wartung:** Ein Zug kann mehrere Wartungen haben (one-to-many Beziehung).

## Die Datei `routes.py`
Die Datei `routes.py` ist ein zentraler Bestandteil des Projekts, da sie die Routen der Webanwendung definiert. Jede dieser Routen ist mit einer Funktion verbunden, die festlegt, welche Aktionen bei einem Aufruf der Route durchgeführt werden. Hier sind die wichtigsten Routen nach Administrator und Mitarbeiter Rechten kategorisiert: 

### Methoden für Administratoren

- **admin_required(f):**
Dekorator, der überprüft, ob der aktuelle Benutzer ein Administrator ist. Wenn nicht, wird eine Fehlermeldung angezeigt und der Benutzer zur Zugübersicht umgeleitet.

- **get_zug():**
API-Endpunkt, der eine Liste aller verfügbaren Züge zurückgibt. Züge, die sich in Wartung befinden, werden ausgeschlossen.

- **login():**
Behandelt das Einloggen. Wenn der Benutzer bereits eingeloggt ist, wird er zur Startseite umgeleitet. Ansonsten wird das Login-Formular angezeigt und bei erfolgreicher Validierung der Benutzer eingeloggt.

- **logout():**
Behandelt das Ausloggen des Benutzers und leitet ihn anschließend zur Login-Seite um.

- **userOverview():**
Zeigt eine Übersicht aller Benutzer an. 

- **wagenOverview():**
Zeigt eine Übersicht aller Wagen (Triebwagen und Personenwagen) an. 

- **zugOverview():**
Zeigt eine Übersicht aller Züge an. 

- **wartungOverview():**
Zeigt eine Übersicht aller Wartungen an. Administratoren können alle Wartungen sehen.

- **createUser():**
Ermöglicht es Administratoren, neue Benutzer zu erstellen. Bei erfolgreicher Erstellung wird der Benutzer zur Benutzerübersicht umgeleitet.

- **updateUser(user_id):**
Ermöglicht es Administratoren, Benutzerinformationen zu aktualisieren. 

- **deleteUser(user_id):**
Ermöglicht es Administratoren, Benutzer zu löschen. 

- **createWagen(typ):**
Ermöglicht es Administratoren, neue Wagen (Triebwagen oder Personenwagen) zu erstellen. Bei erfolgreicher Erstellung wird der Benutzer zur Wagenübersicht umgeleitet.

- **updateWagen(wagennummer):**
Ermöglicht es Administratoren, Wageninformationen zu aktualisieren. Bei erfolgreicher Aktualisierung wird der Benutzer zur Wagenübersicht umgeleitet.

- **deleteWagen(wagennummer):**
Ermöglicht es Administratoren, Wagen zu löschen. Es wird überprüft, ob der Wagen in einem Zug verwendet wird, bevor er gelöscht wird.

- **createZug():**
Ermöglicht es Administratoren, neue Züge zu erstellen. Bei erfolgreicher Erstellung wird der Benutzer zur Zugübersicht umgeleitet.

- **updateZug(zug_nummer):**
Ermöglicht es Administratoren, Zuginformationen zu aktualisieren. Bei erfolgreicher Aktualisierung wird der Benutzer zur Zugübersicht umgeleitet.

- **deleteZug(zug_nummer):**
Ermöglicht es Administratoren, Züge zu löschen. Es wird überprüft, ob der Zug in einer Wartung verwendet wird, bevor er gelöscht wird.

- **createWartung():**
Ermöglicht es Administratoren, neue Wartungen zu erstellen. Bei erfolgreicher Erstellung wird der Benutzer zur Wartungsübersicht umgeleitet.

- **updateWartung(wartung_nr):**
Ermöglicht es Administratoren, Wartungsinformationen zu aktualisieren. Bei erfolgreicher Aktualisierung wird der Benutzer zur Wartungsübersicht umgeleitet.

- **deleteWartung(wartung_nr):**
Ermöglicht es Administratoren, Wartungen zu löschen. Bei erfolgreicher Löschung wird der Benutzer zur Wartungsübersicht umgeleitet.

### Methoden für Mitarbeiter

- **login():**
Behandelt das Einloggen. Wenn der Benutzer bereits eingeloggt ist, wird er zur Startseite umgeleitet. Ansonsten wird das Login-Formular angezeigt und bei erfolgreicher Validierung der Benutzer eingeloggt.

- **logout():**
Behandelt das Ausloggen des Benutzers und leitet ihn anschließend zur Login-Seite um.

- **userOverview():**
Zeigt eine Übersicht aller Benutzer an. 

- **wagenOverview():**
Zeigt eine Übersicht aller Wagen (Triebwagen und Personenwagen) an. 

- **zugOverview():**
Zeigt eine Übersicht aller Züge an. 

- **wartungOverview():**
Zeigt eine Übersicht aller Wartungen an. Benutzer als Mitarbeiter kann nur ihre eigenen Wartungen sehen.

## Die Datei `forms.py`
Die forms.py Datei definiert verschiedene Formularklassen und Hilfsfunktionen für die Verwaltung von System. Jede Formularklasse erbt von FlaskForm und enthält Felder für spezifische Daten sowie Validatoren zur Sicherstellung der Datenintegrität.

Die Formularklassen umfassen:

- **LoginForm**: Sammelt Benutzerdaten für die Anmeldung mit Benutzername und Passwort.
  
- **CreateUserForm**: Erlaubt die Registrierung neuer Benutzer mit Validierung für eindeutige Benutzernamen und E-Mail-Adressen.
  
- **UpdateUserForm**: Ermöglicht die Aktualisierung von Benutzerinformationen, einschließlich Benutzername, E-Mail-Adresse und Administrationsrechten.
  
- **TriebwagenForm**: Erfasst Daten für Triebwagen mit Feldern wie Wagennummer, Spurweite und maximaler Zugkraft, einschließlich Validierung der Eindeutigkeit der Wagennummer.
  
- **PersonenwagenForm**: Analog zu TriebwagenForm, jedoch spezifisch für Personenwagen mit zusätzlichen Feldern für Sitzanzahl und maximales Gewicht.
  
- **UpdateTriebwagenForm** und **UpdatePersonenwagenForm**: Varianten der vorherigen Formulare zur Aktualisierung bestehender Wageninformationen unter Berücksichtigung der Eindeutigkeit der Wagennummer.
  
- **ZugForm**: Erfasst Daten für Züge, einschließlich Zugnummer, Zugname und Triebwagenzuweisung mit Validierung der Eindeutigkeit der Zugnummer.
  
- **UpdateZugForm**: Ermöglicht die Aktualisierung von Zuginformationen, einschließlich Validierung der Eindeutigkeit der Zugnummer und Triebwagenzuweisung.
  
- **WartungForm**: Erfasst Daten für Wartungsaktivitäten mit Feldern wie Wartungsnummer, beteiligte Mitarbeiter, zugewiesener Zug und Zeitrahmen der Wartung, inklusive Validierung der Eindeutigkeit der Wartungsnummer.
  
- **UpdateWartungForm**: Erlaubt die Aktualisierung von Wartungsdaten unter Berücksichtigung der Eindeutigkeit der Wartungsnummer, der beteiligten Mitarbeiter, des zugewiesenen Zugs sowie des Zeitrahmens.



