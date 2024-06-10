# Strecken IS - Projekt Setup

Folgen Sie diesen Schritten, um das Strecken_IS Projekt auf einem Linux-System einzurichten.

## Erstellen Sie eine virtuelle Umgebung

1. Navigieren Sie zu dem Verzeichnis, in dem Sie die virtuelle Umgebung erstellen möchten.
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
flask run --port:5001
```
## Dokumentation der Anwendung

Das Projekt ist eine Webanwendung, die mit dem Flask-Framework in Python erstellt wurde. Es verwendet SQLAlchemy als ORM (Object-Relational Mapper) für die Datenbankinteraktionen und Flask-Login für die Benutzerauthentifizierung.

Die zentrale Datei des Projekts ist `routes.py`, die die Routen für die Webanwendung definiert. Jede Route ist mit einer Funktion verknüpft, die bestimmt, was passiert, wenn die Route aufgerufen wird. Hier eine Zusammenfassung der wichtigsten Routen:

- [`index()`](#index): Diese Methode ist für die Hauptseite der Anwendung zuständig. Sie holt alle Bahnhöfe, Abschnitte, Strecken und Warnungen aus der Datenbank und gibt sie an die index.html Vorlage weiter.
- [`login()`](#login): Diese Methode ist für die Anmeldeseite zuständig. Sie überprüft, ob der Benutzer bereits angemeldet ist, und leitet ihn in diesem Fall zur Hauptseite weiter. Andernfalls überprüft sie die Anmeldedaten des Benutzers und leitet ihn bei erfolgreicher Anmeldung zur Hauptseite weiter.
- [`logout()`](#logout): Diese Methode meldet den Benutzer ab und leitet ihn zur Hauptseite weiter.
- [`register()`](#register): Diese Methode ist für die Registrierungsseite zuständig. Sie erstellt einen neuen Benutzer in der Datenbank, wenn die Registrierungsdaten gültig sind.
- [`bahnhof()`](#bahnhof): Diese Methode ist für die Bahnhofsseite zuständig. Sie erstellt einen neuen Bahnhof in der Datenbank, wenn die Bahnhofsdaten gültig sind.
- [`edit_bahnhof(name)`](#edit_bahnhof): Diese Methode ist für die Bearbeitungsseite eines Bahnhofs zuständig. Sie aktualisiert die Daten eines Bahnhofs in der Datenbank, wenn die Bahnhofsdaten gültig sind.
- [`delete_bahnhof(name)`](#delete_bahnhof): Diese Methode löscht einen Bahnhof aus der Datenbank.
- [`abschnitt()`](#abschnitt): Diese Methode ist für die Abschnittsseite zuständig. Sie erstellt einen neuen Abschnitt in der Datenbank, wenn die Abschnittsdaten gültig sind.
- [`edit_abschnitt(abschnitt_id)`](#edit_abschnitt): Diese Methode ist für die Bearbeitungsseite eines Abschnitts zuständig. Sie aktualisiert die Daten eines Abschnitts in der Datenbank, wenn die Abschnittsdaten gültig sind.
- [`delete_abschnitt(abschnitt_id)`](#delete_abschnitt): Diese Methode löscht einen Abschnitt aus der Datenbank.
- [`warnungen()`](#warnungen): Diese Methode ist für die Warnungsseite zuständig. Sie erstellt eine neue Warnung in der Datenbank, wenn die Warnungsdaten gültig sind.
- [`edit_warnung(warnung_id)`](#edit_warnung): Diese Methode ist für die Bearbeitungsseite einer Warnung zuständig. Sie aktualisiert die Daten einer Warnung in der Datenbank, wenn die Warnungsdaten gültig sind.
- [`delete_warnung(warnung_id)`](#delete_warnung): Diese Methode löscht eine Warnung aus der Datenbank.
- [`strecke()`](#strecke): Diese Methode ist für die Streckenseite zuständig. Sie erstellt eine neue Strecke in der Datenbank, wenn die Streckendaten gültig sind.
- [`delete_strecke(name)`](#delete_strecke): Diese Methode löscht eine Strecke aus der Datenbank.
- [`internal_error(error)`](#internal_error): Diese Methode wird aufgerufen, wenn ein interner Serverfehler auftritt. Sie leitet den Benutzer zur Hauptseite weiter und zeigt eine Fehlermeldung an.
- [`get_strecken_sortiert(strecke_name)`](#get_strecken_sortiert): Diese Methode gibt eine sortierte Liste von Abschnitten für eine bestimmte Strecke zurück.
- [`get_strecken_namen()`](#get_strecken_namen): Diese Methode gibt eine Liste aller Streckennamen zurück.

Die wichtigsten Klassen in diesem Projekt sind `User`, `Bahnhof`, `Abschnitt`, `Warnung` und `Strecke`, die in der `models.py` Datei definiert sind. Jede dieser Klassen repräsentiert eine Tabelle in der Datenbank.


1. `User`: Diese Klasse repräsentiert einen Benutzer der Anwendung. Sie hat Attribute wie `username`, `email` und `password_hash` und Methoden zur Passwortüberprüfung und -setzung.


2. `Bahnhof`: Diese Klasse repräsentiert einen Bahnhof. Sie hat Attribute wie `name`, `adresse`, `latitude` und `longitude`.



3. `Abschnitt`: Diese Klasse repräsentiert einen Abschnitt zwischen zwei Bahnhöfen. Sie hat Attribute wie `startbahnhof_id`, `endbahnhof_id`, `maximale_geschwindigkeit`, `maximale_spurweite`, `nutzungsentgelt` und `distanz`.



4. `Warnung`: Diese Klasse repräsentiert eine Warnung für einen bestimmten Abschnitt. Sie hat Attribute wie `abschnitt_id_warnung`, `titel`, `gueltigkeitsdatum` und `beschreibung`.


5. `Strecke`: Diese Klasse repräsentiert eine Strecke, die aus mehreren Abschnitten besteht. Sie hat ein Attribut `name`.

### Weitere wichtige Klassen, Methoden und Funktionen in diesem Projekt sind:

#### `validate_strecke` Methode

Die `validate_strecke` Methode ist eine Methode der `Strecke` Klasse. Sie validiert und sortiert die Abschnitte einer Strecke. Die Methode überprüft zunächst, ob die Strecke Abschnitte hat. Wenn die Strecke keine Abschnitte hat oder nur einen Abschnitt hat, gibt die Methode eine leere Liste zurück.

Die Methode sucht dann den Startabschnitt der Strecke, der der Abschnitt ist, dessen Startbahnhof nicht als Endbahnhof eines anderen Abschnitts auf der Strecke erscheint. Wenn kein solcher Abschnitt gefunden wird, gibt die Methode `None` zurück.

Die Methode initialisiert eine Liste `sorted_abschnitte` mit dem Startabschnitt und fügt dann die Abschnitte hinzu, die an den Endbahnhof des zuletzt hinzugefügten Abschnitts anschließen. Dieser Schritt wird wiederholt, bis alle Abschnitte der Strecke in der Liste sind.

Wenn zu irgendeinem Zeitpunkt kein nächster Abschnitt gefunden wird oder mehr als ein nächster Abschnitt gefunden wird, gibt die Methode `None` zurück, da die Strecke in diesem Fall nicht gültig ist.

Wenn alle Abschnitte erfolgreich hinzugefügt wurden, gibt die Methode die sortierte Liste der Abschnitte zurück.

#### `index.html` Datei

Die `index.html` Datei verwendet die Leaflet JavaScript-Bibliothek, um eine interaktive Karte zu erstellen und auf der Webseite anzuzeigen. Die Karte zeigt die Abschnitte zwischen den Bahnhöfen an, die in der Datenbank gespeichert sind.

Zunächst wird eine neue Karte erstellt und auf eine bestimmte geographische Position zentriert. Dann wird ein Tile Layer zur Karte hinzugefügt, der die visuellen Daten für die Karte bereitstellt.

Die Abschnitte werden aus der Flask-Anwendung in das JavaScript übertragen und in der Variable `abschnitte` gespeichert. Für jeden Abschnitt wird ein Start- und Endmarker erstellt und zur Karte hinzugefügt. Außerdem wird eine Linie zwischen den Start- und Endpunkten des Abschnitts gezeichnet. Jeder Marker und jede Linie hat ein Popup, das Informationen über den Abschnitt anzeigt, wenn der Benutzer darauf klickt.

Die Abschnitte werden in Layer-Gruppen organisiert, die nach den Strecken-IDs benannt sind. Diese Layer-Gruppen können vom Benutzer ein- und ausgeblendet werden, um die verschiedenen Strecken auf der Karte anzuzeigen oder zu verbergen.

#### `forms.py` Datei

Die `forms.py` Datei definiert verschiedene Formularklassen und Hilfsfunktionen. Jede Formularklasse erbt von `FlaskForm` und definiert die Felder, die im Formular enthalten sein sollen, sowie die Validatoren, die auf diese Felder angewendet werden.

Die Formularklassen sind:

- `LoginForm`: Sammelt Benutzerdaten für die Anmeldung.
- `RegistrationForm`: Sammelt Benutzerdaten für die Registrierung und validiert den Benutzernamen und die E-Mail-Adresse.
- `BahnhofForm`: Sammelt Daten für einen Bahnhof.
- `AbschnittForm`: Sammelt Daten für einen Abschnitt und validiert den Endbahnhof.
- `WarnungForm`: Sammelt Daten für eine Warnung.
- `StreckeForm`: Sammelt Daten für eine Strecke.

Die Hilfsfunktionen `get_bahnhof_choices`, `get_abschnitt_choices` und `get_strecke_choices` generieren die Auswahlmöglichkeiten für die entsprechenden SelectField-Felder in den Formularen.