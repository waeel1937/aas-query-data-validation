# AAS JSON Validator and Classifier

Dieses Projekt enthält Python-Skripte zur Validierung und Klassifizierung von JSON-Objekten, die dem Asset Administration Shell (AAS)-Standard entsprechen, wie er z. B. in Eclipse BaSyx verwendet wird. Es bietet zwei Hauptfunktionen:

1. **Validierung:** Überprüfung der Struktur und Inhalte eines AAS-JSON-Objekts gegen vordefinierte Regeln.
2. **Klassifizierung:** Training eines maschinellen Lernmodells zur automatischen Erkennung von gültigen und ungültigen AAS-JSONs.

## Voraussetzungen

- Python 3.8 oder höher
- Erforderliche Bibliotheken:
  - `json` (standardmäßig enthalten)
  - `pandas` (für Datenverarbeitung beim Modelltraining)
  - `scikit-learn` (für maschinelles Lernen)

Installiere die Abhängigkeiten mit:
```bash
pip install pandas scikit-learn
