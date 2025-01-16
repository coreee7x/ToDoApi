# Basis-Image
FROM python:3.10-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die notwendigen Dateien in das Arbeitsverzeichnis
COPY . /app

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Exponiere den Port für Flask
EXPOSE 5000

# Befehl zum Starten der Anwendung
CMD ["python", "app.py"]
