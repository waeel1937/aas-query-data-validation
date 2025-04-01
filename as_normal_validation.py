import json
from typing import Dict, List, Optional

# Beispiel-JSON (kann durch dein JSON ersetzt werden)
example_json = '''
{
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:org.eclipse.basyx:assets:GIMAT_pH722Z1:1.0.0"
  },
  "submodels": [
    {
      "keys": [
        {
          "type": "Submodel",
          "value": "urn:org.eclipse.basyx:submodels:GIMAT_Identification:1.0.0"
        }
      ],
      "type": "ModelReference",
      "submodel": {
        "submodelElements": [
          {"idShort": "SerialNumber", "kind": "Instance", "modelType": "Property", "valueType": "string", "value": "XYZ123"},
          {"idShort": "Model", "kind": "Instance", "modelType": "Property", "valueType": "string", "value": "pH 722 Z1-Gel"}
        ],
        "id": "urn:org.eclipse.basyx:submodels:GIMAT_Identification:1.0.0",
        "modelType": "Submodel",
        "kind": "Instance",
        "idShort": "GIMAT_Identification"
      }
    }
  ],
  "modelType": "AssetAdministrationShell",
  "id": "urn:org.eclipse.basyx:shells:GIMAT_pH722Z1_AAS:1.0.0",
  "idShort": "GIMAT_pH722Z1_AAS"
}
'''

def validate_aas_json(json_str: str) -> Dict[str, bool]:
    """Validiert ein AAS-JSON-Objekt gegen definierte Regeln."""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {"valid": False, "error": "Invalid JSON syntax"}

    result = {"valid": True, "errors": []}

    # Pflichtfelder für AssetAdministrationShell
    required_aas_fields = ["assetInformation", "submodels", "modelType", "id", "idShort"]
    for field in required_aas_fields:
        if field not in data or not data[field]:
            result["valid"] = False
            result["errors"].append(f"Missing or empty required field: {field}")

    # Validierung von assetInformation
    if "assetInformation" in data:
        ai = data["assetInformation"]
        if "assetKind" not in ai or ai["assetKind"] not in ["Instance", "Type"]:
            result["valid"] = False
            result["errors"].append("assetInformation.assetKind must be 'Instance' or 'Type'")
        if "globalAssetId" not in ai or not isinstance(ai["globalAssetId"], str):
            result["valid"] = False
            result["errors"].append("assetInformation.globalAssetId must be a string")

    # Validierung von modelType
    if data.get("modelType") != "AssetAdministrationShell":
        result["valid"] = False
        result["errors"].append("modelType must be 'AssetAdministrationShell'")

    # Validierung der Submodels
    if "submodels" in data and isinstance(data["submodels"], list):
        for submodel_ref in data["submodels"]:
            if "keys" not in submodel_ref or "type" not in submodel_ref:
                result["valid"] = False
                result["errors"].append("Submodel reference must have 'keys' and 'type'")
            if submodel_ref.get("type") != "ModelReference":
                result["valid"] = False
                result["errors"].append("Submodel type must be 'ModelReference'")
            if "submodel" in submodel_ref:
                submodel = submodel_ref["submodel"]
                required_submodel_fields = ["submodelElements", "id", "modelType", "kind", "idShort"]
                for field in required_submodel_fields:
                    if field not in submodel:
                        result["valid"] = False
                        result["errors"].append(f"Submodel missing required field: {field}")
                if submodel.get("modelType") != "Submodel":
                    result["valid"] = False
                    result["errors"].append("Submodel.modelType must be 'Submodel'")
                if "submodelElements" in submodel:
                    for element in submodel["submodelElements"]:
                        if not all(k in element for k in ["idShort", "kind", "modelType", "valueType", "value"]):
                            result["valid"] = False
                            result["errors"].append(f"SubmodelElement {element.get('idShort', 'unknown')} missing required fields")
                        if element.get("modelType") != "Property":
                            result["valid"] = False
                            result["errors"].append(f"SubmodelElement {element['idShort']} must have modelType 'Property'")

    return result

# Testen der Validierung
validation_result = validate_aas_json(example_json)
if validation_result["valid"]:
    print("JSON ist gültig!")
else:
    print("JSON ist ungültig. Fehler:")
    for error in validation_result["errors"]:
        print(f"- {error}")