
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import uuid

def parse_input(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return next(reader)

def generate_eda_xml(data):
    ns = "http://www.egvp.de/Nachrichtentypen/EDA/1.4"
    ET.register_namespace('', ns)
    root = ET.Element(f"{{{ns}}}Mahnantrag")
    root.set("verfahrensart", "Mahn")
    root.set("version", "1.4")
    root.set("dateiID", str(uuid.uuid4()))
    root.set("erstellungszeitpunkt", datetime.now().isoformat())

    parteien = ET.SubElement(root, f"{{{ns}}}Parteien")
    g = ET.SubElement(parteien, f"{{{ns}}}Partei", parteiTyp="Antragsteller", parteiNr="G1")
    ET.SubElement(g, f"{{{ns}}}Name").text = data['glaeubiger_name']
    a = ET.SubElement(g, f"{{{ns}}}Anschrift")
    ET.SubElement(a, f"{{{ns}}}Strasse").text = data['glaeubiger_strasse']
    ET.SubElement(a, f"{{{ns}}}Hausnummer").text = data['glaeubiger_hausnummer']
    ET.SubElement(a, f"{{{ns}}}Postleitzahl").text = data['glaeubiger_plz']
    ET.SubElement(a, f"{{{ns}}}Ort").text = data['glaeubiger_ort']

    s = ET.SubElement(parteien, f"{{{ns}}}Partei", parteiTyp="Antragsgegner", parteiNr="S1")
    ET.SubElement(s, f"{{{ns}}}Name").text = data['schuldner_name']
    a2 = ET.SubElement(s, f"{{{ns}}}Anschrift")
    ET.SubElement(a2, f"{{{ns}}}Strasse").text = data['schuldner_strasse']
    ET.SubElement(a2, f"{{{ns}}}Hausnummer").text = data['schuldner_hausnummer']
    ET.SubElement(a2, f"{{{ns}}}Postleitzahl").text = data['schuldner_plz']
    ET.SubElement(a2, f"{{{ns}}}Ort").text = data['schuldner_ort']

    fds = ET.SubElement(root, f"{{{ns}}}Forderungen")
    f1 = ET.SubElement(fds, f"{{{ns}}}Forderung", forderungstyp="Hauptforderung", forderungID="F1")
    ET.SubElement(f1, f"{{{ns}}}GlaeubigerRef").text = "G1"
    ET.SubElement(f1, f"{{{ns}}}SchuldnerRef").text = "S1"
    ET.SubElement(f1, f"{{{ns}}}Betrag", waehrung="EUR").text = data['hauptforderung']
    ET.SubElement(f1, f"{{{ns}}}Gegenstand").text = data['gegenstand']

    verfahren = ET.SubElement(root, f"{{{ns}}}Verfahren")
    ET.SubElement(verfahren, f"{{{ns}}}Amtsgericht").text = data['amtsgericht']
    ET.SubElement(verfahren, f"{{{ns}}}Verfahrensgegenstand").text = "Mahnverfahren"
    ET.SubElement(verfahren, f"{{{ns}}}Verfahrensart").text = "Antrag auf Erlass eines Mahnbescheids"
    ET.SubElement(verfahren, f"{{{ns}}}Antragstyp").text = "NormalerMahnantrag"

    return ET.ElementTree(root)

def create_eda_zip(xml_tree, basename):
    from zipfile import ZipFile
    import os
    xml_path = f"/tmp/{basename}.xml"
    manifest_path = f"/tmp/EDA-INF/manifest.xml"
    os.makedirs("/tmp/EDA-INF", exist_ok=True)
    xml_tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(f"<manifest><filename>{basename}.xml</filename></manifest>")
    zip_path = f"/tmp/{basename}.zip"
    with ZipFile(zip_path, 'w') as zipf:
        zipf.write(xml_path, arcname=f"{basename}.xml")
        zipf.write(manifest_path, arcname="EDA-INF/manifest.xml")
    return zip_path
