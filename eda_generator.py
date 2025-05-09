import json
import xml.etree.ElementTree as ET
from datetime import datetime
import uuid
import zipfile
from pathlib import Path

def parse_input(input_path):
    import csv
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return next(reader)

def generate_eda_xml(data):
    ns = "http://www.egvp.de/Nachrichtentypen/EDA/1.4"
    ET.register_namespace('', ns)
    root = ET.Element(f"{{{ns}}}Mahnantrag", verfahrensart="Mahn", version="1.4")
    root.set("dateiID", str(uuid.uuid4()))
    root.set("erstellungszeitpunkt", datetime.now().isoformat())

    parteien = ET.SubElement(root, f"{{{ns}}}Parteien")

    g = ET.SubElement(parteien, f"{{{ns}}}Partei", parteiTyp="Antragsteller", parteiNr="G1")
    ET.SubElement(g, f"{{{ns}}}Name").text = data['glaeubiger_name']
    ga = ET.SubElement(g, f"{{{ns}}}Anschrift")
    ET.SubElement(ga, f"{{{ns}}}Strasse").text = data['glaeubiger_strasse']
    ET.SubElement(ga, f"{{{ns}}}Hausnummer").text = data['glaeubiger_hausnummer']
    ET.SubElement(ga, f"{{{ns}}}Postleitzahl").text = data['glaeubiger_plz']
    ET.SubElement(ga, f"{{{ns}}}Ort").text = data['glaeubiger_ort']

    s = ET.SubElement(parteien, f"{{{ns}}}Partei", parteiTyp="Antragsgegner", parteiNr="S1")
    ET.SubElement(s, f"{{{ns}}}Name").text = data['schuldner_name']
    sa = ET.SubElement(s, f"{{{ns}}}Anschrift")
    ET.SubElement(sa, f"{{{ns}}}Strasse").text = data['schuldner_strasse']
    ET.SubElement(sa, f"{{{ns}}}Hausnummer").text = data['schuldner_hausnummer']
    ET.SubElement(sa, f"{{{ns}}}Postleitzahl").text = data['schuldner_plz']
    ET.SubElement(sa, f"{{{ns}}}Ort").text = data['schuldner_ort']

    forderungen = ET.SubElement(root, f"{{{ns}}}Forderungen")
    hf = ET.SubElement(forderungen, f"{{{ns}}}Forderung", forderungstyp="Hauptforderung", forderungID="F1")
    ET.SubElement(hf, f"{{{ns}}}GlaeubigerRef").text = "G1"
    ET.SubElement(hf, f"{{{ns}}}SchuldnerRef").text = "S1"
    ET.SubElement(hf, f"{{{ns}}}Betrag", waehrung="EUR").text = data['hauptforderung']
    ET.SubElement(hf, f"{{{ns}}}Gegenstand").text = data['gegenstand']

    verfahren = ET.SubElement(root, f"{{{ns}}}Verfahren")
    ET.SubElement(verfahren, f"{{{ns}}}Amtsgericht").text = data['amtsgericht']
    ET.SubElement(verfahren, f"{{{ns}}}Verfahrensgegenstand").text = "Mahnverfahren"

    return ET.ElementTree(root)

def create_eda_zip(tree, base_name):
    output_dir = Path("/tmp")
    xml_path = output_dir / f"{base_name}.xml"
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    manifest_path = output_dir / "manifest.xml"
    manifest_path.write_text(f"<manifest><file>{xml_path.name}</file></manifest>", encoding="utf-8")

    zip_path = output_dir / f"{base_name}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(xml_path, arcname=xml_path.name)
        zipf.write(manifest_path, arcname=manifest_path.name)

    return str(zip_path)
