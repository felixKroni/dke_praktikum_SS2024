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
flask run --port=5001
```

# Dokumentation der Anwendung

