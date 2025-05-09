import pdfplumber

def extract_invoice_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Einfache heuristische Extraktion (kann angepasst werden)
    data = {
        'glaeubiger_name': 'Beispiel GmbH',
        'glaeubiger_strasse': 'Musterweg',
        'glaeubiger_hausnummer': '1',
        'glaeubiger_plz': '12345',
        'glaeubiger_ort': 'Musterstadt',
        'schuldner_name': 'Max Mustermann',
        'schuldner_strasse': 'Beispielstraße',
        'schuldner_hausnummer': '2',
        'schuldner_plz': '54321',
        'schuldner_ort': 'Beispieldorf',
        'hauptforderung': '1234.56',
        'gegenstand': 'Lieferung laut Rechnung',
        'amtsgericht': 'AG Musterstadt'
    }

    # Beispielsuche (je nach Layout anpassen)
    lines = text.splitlines()
    for line in lines:
        if 'Rechnungsbetrag' in line or 'Gesamtbetrag' in line:
            try:
                betrag = ''.join(filter(str.isdigit, line.replace(",", ".")))
                data['hauptforderung'] = str(float(betrag) / 100)
            except:
                pass
        if 'Herr' in line or 'Frau' in line:
            data['schuldner_name'] = line.strip()

    return data