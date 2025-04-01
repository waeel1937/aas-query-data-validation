# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 13:58:52 2025

@author: waeel
"""

import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from typing import Dict
 

# Beispiel-Datensatz (manuell erstellt, erweitere ihn mit deinen Daten)
data = [
    {"json": '{"assetInformation": {"assetKind": "Instance", "globalAssetId": "urn:test"}, "submodels": [], "modelType": "AssetAdministrationShell", "id": "urn:test", "idShort": "Test"}', "valid": 1},
    {"json": '{"assetInformation": {"assetKind": "Invalid"}, "modelType": "Wrong"}', "valid": 0},
    {"json": '{"assetInformation": {"assetKind": "Instance", "globalAssetId": "urn:test2"}, "submodels": [{"keys": [{"type": "Submodel", "value": "urn:sub"}] }], "modelType": "AssetAdministrationShell", "id": "urn:test2", "idShort": "Test2"}', "valid": 1},
    {"json": '{"id": "urn:test3"}', "valid": 0}
]

# Feature-Extraktion
def extract_features(json_str: str) -> Dict[str, int]:
    try:
        data = json.loads(json_str)
        features = {
            "has_assetInformation": int("assetInformation" in data),
            "has_submodels": int("submodels" in data),
            "has_modelType": int("modelType" in data and data["modelType"] == "AssetAdministrationShell"),
            "has_id": int("id" in data),
            "has_idShort": int("idShort" in data),
            "submodel_count": len(data.get("submodels", [])),
            "has_valid_assetKind": int(data.get("assetInformation", {}).get("assetKind") in ["Instance", "Type"])
        }
    except json.JSONDecodeError:
        features = {key: 0 for key in ["has_assetInformation", "has_submodels", "has_modelType", "has_id", "has_idShort", "submodel_count", "has_valid_assetKind"]}
    return features

# Daten vorbereiten
features_list = [extract_features(item["json"]) for item in data]
labels = [item["valid"] for item in data]
df = pd.DataFrame(features_list)
df["valid"] = labels

# Features und Labels trennen
X = df.drop("valid", axis=1)
y = df["valid"]

# Daten in Trainings- und Testset aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell trainieren
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Modell evaluieren
accuracy = model.score(X_test, y_test)
print(f"Modellgenauigkeit: {accuracy:.2f}")

# Beispiel-Validierung mit dem Modell
new_json = '''


'''
new_features = extract_features(new_json)
prediction = model.predict(pd.DataFrame([new_features]))[0]
print(f"Vorhersage für neues JSON: {'Gültig' if prediction == 1 else 'Ungültig'}")