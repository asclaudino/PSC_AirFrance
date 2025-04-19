import xmltodict
import json

# Chemins des fichiers
xml_file = "Ressources/Export20PN.xml"
json_file = "Export20PN.json"

# Lire le fichier XML
with open(xml_file, "r", encoding="utf-8") as file:
    xml_content = file.read()

# Convertir le XML en un dictionnaire Python
data_dict = xmltodict.parse(xml_content)

# Convertir le dictionnaire en JSON
json_content = json.dumps(data_dict, indent=4, ensure_ascii=False)

# Sauvegarder le contenu JSON dans un fichier
with open(json_file, "w", encoding="utf-8") as file:
    file.write(json_content)

print(f"Conversion réussie ! Le fichier JSON est sauvegardé sous : {json_file}")