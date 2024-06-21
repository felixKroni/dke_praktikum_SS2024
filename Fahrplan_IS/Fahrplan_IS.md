# Fahrplan IS - Projekt Setup
Wichtig! Bevor sie dieses Setup ausführen, folgen Sie bitte den Anleitungen der anderen Applikationen (Strecken_IS und Flotten_IS) in diesem Projekt und stellen Sie sicher das diese auf den folgenden Ports laufen.
Strecken_IS: Port 5001
Flotten_IS: Port 5002
dadurch ändern sich commands zum starten der Applikationen folgend:
Strecken_IS: flask run --port=5001
Flotten_IS: flask run --port=5002


Folgen Sie diesen Schritten, um das Fahrplan_IS Projekt auf einem Linux-System einzurichten. Sollten Sie das Projektsetup bereits ausgeführt haben, können Sie direkt zum Punkt [Starten Sie die Anwendung](#starten-sie-die-anwendung) springen. Vergessen Sie nicht davor die [virtuelle Umgebung zu aktivieren](#aktivieren-sie-die-virtuelle-umgebung).

## Erstellen Sie eine virtuelle Umgebung

1. Navigieren Sie in das Verzeichnis `Fahrplan_IS` (Ausgehend vom Hauptverzeichnis des Projekts).
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
flask run --port=5000
```

Beim ersten Start wird automatisch ein Standard Admin generiert. 
Dieser hat folgende Zugangsdaten:
un: admin
pw: admin
Dies passiert außerdem jedesmal wenn die App gestartet wird und kein Admin Benutzer existiert.

## Erste Schritte
Öffnen Sie folgende Adresse in ihrem Browser nachdem der Befehl `flask run --port=5000` ausgeführt wurde: `http://127.0.0.1:5000/index`
Erster Login mit den Anmeldedaten wie oben beschrieben ist Benutzername: admin und Passwort: admin


# Dokumentation des Source Codes

Das Projekt ist eine Webanwendung, die mit dem Flask-Framework in Python erstellt wurde. Es verwendet SQLAlchemy als ORM (Object-Relational Mapper) für die Datenbankinteraktionen und Flask-Login für die Benutzerauthentifizierung.

Das zugrundeliegende Datenmodel und der Prototyp der Webanwendung wurden im Rahmen des Projekts entwickelt und im Ordnder `Modelle` abgelegt.

Die zentrale Datei des Projekts ist `routes.py`, die die Routen für die Webanwendung definiert. Jede Route ist mit einer Funktion verknüpft, die bestimmt, was passiert, wenn die Route aufgerufen wird. Hier eine Zusammenfassung der wichtigsten Routen:

### Home und Login
- `/` und `/index`: Startseite der Anwendung anzeigen.
- `/login`: Benutzeranmeldung durchführen.
- `/logout`: Benutzer abmelden.
- `/registerMitarbeiter`: Neuen Mitarbeiter registrieren (nur für Admins).
- `/mitarbeiterList`: Liste aller Mitarbeiter anzeigen (nur für Admins).
- `/deleteMitarbeiter/<int:id>`: Mitarbeiter löschen (nur für Admins).
- `/editMitarbeiter/<int:id>`: Mitarbeiterdaten bearbeiten (nur für Admins).

### Halteplan Verwaltung
- `/halteplanList`: Liste aller Haltepläne anzeigen (nur für Admins).
- `/createHalteplan`: Neuen Halteplan erstellen (nur für Admins).
- `/chooseHaltestellen`: Haltestellen für einen neuen Halteplan auswählen (nur für Admins).
- `/choosePrices/<int:halteplan_id>`: Preise für die Abschnitte eines Halteplans festlegen (nur für Admins).
- `/editHalteplan/<int:id>`: Bestehenden Halteplan bearbeiten (nur für Admins).
- `/deleteHalteplan/<int:id>`: Halteplan löschen (nur für Admins).

### Fahrplan Verwaltung
- `/createFahrplan`: Neuen Fahrplan erstellen (nur für Admins).
- `/specificDates/<int:fahrplanId>`: Spezifische Daten für Fahrtdurchführungen festlegen (nur für Admins).
- `/weeklyDays/<int:fahrplanId>`: Wöchentliche Tage für Fahrtdurchführungen festlegen (nur für Admins).
- `/specialPrices`: Spezialpreise für bestimmte Zeiten festlegen (nur für Admins).
- `/confirmFahrplan/<int:fahrplanId>`: Fahrplan bestätigen (nur für Admins).
- `/fahrplanList`: Liste aller Fahrpläne anzeigen.

### Fahrtdurchführung Verwaltung
- `/fahrtdurchfuehrungList`: Liste aller Fahrtdurchführungen anzeigen.
- `/ma_fahrtdurchfuehrungList/<int:ma_id>`: Fahrtdurchführungen eines bestimmten Mitarbeiters anzeigen.
- `/deleteFahrtdurchfuehrung/<int:id>`: Fahrtdurchführung löschen (nur für Admins).
- `/editFahrtdurchfuehrung/<int:id>`: Fahrtdurchführung bearbeiten (nur für Admins).

### REST-APIs und Hilfsfunktionen
- `/api/all_halteplaen_data`: Alle Halteplandaten als JSON abrufen.
- `get_strecken()`: Strecken von einer externen API abrufen.
- `get_all_haltepunkte_of_strecke(strecke_name)`: Alle Haltepunkte einer Strecke von einer externen API abrufen.
- `get_haltepunkte_names(strecke_name)`: Namen der Haltepunkte einer Strecke von einer externen API abrufen.
- `create_abschnitt(start_bahnhof, end_bahnhof, strecke_name, halteplan_id, reihung)`: Abschnitt für einen Halteplan erstellen.
- `get_date_of_next_weekday(start_date, weekday)`: Datum des nächsten bestimmten Wochentags berechnen.
- `weekday_converter(weekday)`: Wochentag in eine Zahl umwandeln.
- `serialize_halteplan(halteplan)`: Halteplan-Objekt serialisieren.
- `serialize_abschnitt_halteplan(abschnitt_halteplan)`: AbschnittHalteplan-Objekt serialisieren.
- `serialize_abschnitt(abschnitt)`: Abschnitt-Objekt serialisieren.
- `serialize_fahrplan(fahrplan)`: Fahrplan-Objekt serialisieren.
- `serialize_fahrtdurchfuehrung(fahrtdurchfuehrung)`: Fahrtdurchführung-Objekt serialisieren.
- `serialize_mitarbeiter_durchfuehrung(mitarbeiter_durchfuehrung)`: MitarbeiterDurchführung-Objekt serialisieren.
- `get_prices_accumulated(halteplan_id, multiplier=1)`: Gesamtpreis für die Abschnitte eines Halteplans berechnen.

### Entitätsklassen
Die Entitäsklassen sind im Folder `models` zu finden. Jedes Python File stellt außerdem eine Tabelle im Datenmodell dar welche mit SQL Alchemy als ORM übersetzt wird.

#### Abschnitt
- `Abschnitt`: Stellt einen Abschnitt zwischen zwei Bahnhöfen dar, inklusive Spurenweite und Nutzungsentgelt.

#### Halteplan
- `Halteplan`: Repräsentiert einen Halteplan, der aus mehreren Abschnitten besteht und einem Fahrplan zugeordnet werden kann.

#### AbschnittHalteplan
- `AbschnittHalteplan`: Verbindet Abschnitte und Haltepläne und gibt die Reihenfolge der Abschnitte innerhalb eines Halteplans an.

#### Fahrplan
- `Fahrplan`: Beschreibt einen Fahrplan mit Gültigkeitszeitraum und den zugehörigen Fahrtdurchführungen.

#### Mitarbeiter
- `Mitarbeiter`: Stellt einen Mitarbeiter dar, inklusive Benutzerinformationen und Berechtigungen.

#### MitarbeiterDurchfuehrung
- `MitarbeiterDurchfuehrung`: Verknüpft Mitarbeiter mit Fahrtdurchführungen und gibt die Einsatzzeiten der Mitarbeiter an.

#### Zug
- `Zug`: Repräsentiert einen Zug, inklusive Spurenweite und Reservierungsstatus.

#### Fahrtdurchfuehrung
- `Fahrtdurchfuehrung`: Beschreibt die Durchführung einer Fahrt zu einem bestimmten Zeitpunkt, inklusive Zug, Ausfall- und Verspätungsstatus sowie Preis.

## Datenbank
Als Datenbank wird SQL Lite verwendet als In-Memory Datenbank die aber regelmäßig in das file `database.db` gespeichert wird.

Initialisiert die Datenbankverbindung und ORM-Engine, erstellt alle Tabellen basierend auf den Modellen, verwaltet die Datenbank-Sitzungen und stellt Controller für verschiedene Entitäten bereit. Enthält Methoden zur Initialisierung der Engine, zum Einfügen von Testdaten und zum Abrufen verschiedener Controller.

#### get_controller
- `get_controller(name)`: Gibt den entsprechenden Controller basierend auf dem übergebenen Namen zurück. Unterstützt die Controller für Basisoperationen (`base`), Züge (`zug`), Mitarbeiter (`ma`), Haltepläne (`hp`), Abschnitte (`ab`), Fahrtdurchführungen (`df`) und Mitarbeiterdurchführungen (`ma_df`). 
Bei einem ungültigen Namen wird ein Fehler ausgelöst.


### DB Controller
Die DB Controller sorgen dafür das die Datenbank operationen klarer Strukturiert werden. 
Besonders hervorzuheben ist die Klasse BaseController.py bei der Datenbank Operationen auf alle Entitäten durchgeführt werden können und auch die Superklasse zu den anderen Controllern darstellt.
Die Subcontroller beeinhalten hauptsächlich spezialfälle für die jeweiligen Entitäten.
Ein Subcontroller kann durch die database.py Klasse geholt werden (Methode: get_controller).

#### AbschnittController
- `AbschnittController`: Verwaltet Operationen für Abschnitt-Entitäten.

#### AbschnittHalteplanController
- `AbschnittHalteplanController`: Verwaltet Operationen für AbschnittHalteplan-Entitäten.

#### BaseController
- `BaseController`: Bietet grundlegende Datenbankoperationen für alle Entitäten.

#### DurchfuehrungController
- `DurchfuehrungController`: Verwaltet Operationen für Fahrtdurchführung-Entitäten, einschließlich der zugehörigen Mitarbeiterdurchführungen.

#### HalteplanController
- `HalteplanController`: Verwaltet Operationen für Halteplan-Entitäten und deren Beziehungen zu Abschnitten.

#### MitarbeiterController
- `MitarbeiterController`: Verwaltet Operationen für Mitarbeiter-Entitäten, einschließlich der Suche nach Benutzernamen, E-Mail und Rolle.

#### MitarbeiterDurchfuehrungController
- `MitarbeiterDurchfuehrungController`: Verwaltet Operationen für MitarbeiterDurchführung-Entitäten.

#### ZugController
- `ZugController`: Verwaltet Operationen für Zug-Entitäten, einschließlich der Suche nach Zugnamen.


## User Interface
Das User Interface (UI) stellt sich aus den html Templates und den zugehörigen forms zusammen.
Wichtig zu wissen ist das `base.html` das Super-html file ist und alle anderen injezieren den code an folgender stelle: 
```html 
{% block content %}{% endblock %}  
```
Ind diesem File wird auch die Navigations leiste definiert damit diese auf allen Seiten gleich bleibt.
### Templates

#### base.html
- `base.html`: Grundgerüst und Layout für alle HTML-Seiten der Anwendung.

#### chooseDays.html
- `chooseDays.html`: Seite zur Auswahl von Wochentagen für Fahrtdurchführungen.

#### chooseHaltestellen.html
- `chooseHaltestellen.html`: Seite zur Auswahl der Haltestellen für einen Halteplan.

#### choosePrices.html
- `choosePrices.html`: Seite zur Festlegung der Preise für die Abschnitte eines Halteplans.

#### confirmFahrplan.html
- `confirmFahrplan.html`: Seite zur Bestätigung der Erstellung eines Fahrplans.

#### createFahrplan.html
- `createFahrplan.html`: Seite zur Erstellung eines neuen Fahrplans.

#### createHalteplan.html
- `createHalteplan.html`: Seite zur Erstellung eines neuen Halteplans.

#### editFahrtdurchfuehrung.html
- `editFahrtdurchfuehrung.html`: Seite zur Bearbeitung einer Fahrtdurchführung.

#### editHalteplan.html
- `editHalteplan.html`: Seite zur Bearbeitung eines Halteplans.

#### editMitarbeiter.html
- `editMitarbeiter.html`: Seite zur Bearbeitung der Mitarbeiterdaten.

#### fahrplanList.html
- `fahrplanList.html`: Seite zur Anzeige der Liste aller Fahrpläne.

#### fahrtdurchfuehrungList.html
- `fahrtdurchfuehrungList.html`: Seite zur Anzeige der Liste aller Fahrtdurchführungen.

#### halteplanList.html
- `halteplanList.html`: Seite zur Anzeige der Liste aller Haltepläne.

#### index.html
- `index.html`: Startseite der Anwendung.

#### login.html
- `login.html`: Seite zur Benutzeranmeldung.

#### ma_all_fahrtdurchfuehrungList.html
- `ma_all_fahrtdurchfuehrungList.html`: Seite zur Anzeige aller Fahrtdurchführungen für Mitarbeiter.

#### ma_fahrtdurchfuehrungList.html
- `ma_fahrtdurchfuehrungList.html`: Seite zur Anzeige der Fahrtdurchführungen eines bestimmten Mitarbeiters.

#### mitarbeiterList.html
- `mitarbeiterList.html`: Seite zur Anzeige der Liste aller Mitarbeiter.

#### registerMitarbeiter.html
- `registerMitarbeiter.html`: Seite zur Registrierung eines neuen Mitarbeiters.

#### specialPrices.html
- `specialPrices.html`: Seite zur Festlegung von Spezialpreisen für bestimmte Zeiten.

#### specificDates.html
- `specificDates.html`: Seite zur Auswahl spezifischer Daten für Fahrtdurchführungen.

#### weeklyDays.html
- `weeklyDays.html`: Seite zur Auswahl wöchentlicher Tage für Fahrtdurchführungen.


### Forms

#### SpecificDateForm
- `SpecificDateForm`: Formular zur Auswahl spezifischer Daten für Fahrtdurchführungen.

#### WeeklyDaysForm
- `WeeklyDaysForm`: Formular zur Auswahl wöchentlicher Tage für Fahrtdurchführungen.

#### ConfirmFahrplanForm
- `ConfirmFahrplanForm`: Formular zur Bestätigung der Erstellung eines Fahrplans.

#### FahrplanForm
- `FahrplanForm`: Formular zur Erstellung eines neuen Fahrplans.

#### SpecialPricesForm
- `SpecialPricesForm`: Formular zur Festlegung von Spezialpreisen für bestimmte Zeiten.

#### EditFahrtdurchfuehrungForm
- `EditFahrtdurchfuehrungForm`: Formular zur Bearbeitung einer Fahrtdurchführung.

#### HalteplanCreateForm
- `HalteplanCreateForm`: Formular zur Erstellung eines neuen Halteplans.

#### HalteplanChooseHaltepunktForm
- `HalteplanChooseHaltepunktForm`: Formular zur Auswahl der Haltepunkte für einen Halteplan.

#### HalteplanChoosePricesForm
- `HalteplanChoosePricesForm`: Formular zur Festlegung der Preise für die Abschnitte eines Halteplans.

#### HalteplanEditForm
- `HalteplanEditForm`: Formular zur Bearbeitung eines Halteplans.

#### LoginForm
- `LoginForm`: Formular zur Benutzeranmeldung.

#### MitarbeiterEditForm
- `MitarbeiterEditForm`: Formular zur Bearbeitung der Mitarbeiterdaten.

#### MitarbeiterRegistrationForm
- `MitarbeiterRegistrationForm`: Formular zur Registrierung eines neuen Mitarbeiters.

