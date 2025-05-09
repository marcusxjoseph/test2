# utils.py
import pdfplumber

def extract_invoice_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Beispielhafte Extraktion: Du kannst RegEx oder NLP verwenden
    data = {
        'glaeubiger_name': 'Beispiel GmbH',
        'glaeubiger_strasse': 'Musterstraße',
        'glaeubiger_hausnummer': '1',
        'glaeubiger_plz': '12345',
        'glaeubiger_ort': 'Musterstadt',
        'schuldner_name': 'Max Mustermann',
        'schuldner_strasse': 'Beispielweg',
        'schuldner_hausnummer': '2',
        'schuldner_plz': '54321',
        'schuldner_ort': 'Beispieldorf',
        'hauptforderung': '1234.56',
        'gegenstand': 'Lieferung laut Rechnung',
        'amtsgericht': 'AG Musterstadt'
    }

    # Du kannst hier echte Parsing-Logik basierend auf dem Text einbauen
    return data
