import pdfplumber
import re

def extract_invoice_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    def find(pattern, default=''):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else default

    return {
        'glaeubiger_name': find(r'Gläubiger[:\s]+(.+?)\n'),
        'glaeubiger_strasse': find(r'Straße[:\s]+(.+?)\n'),
        'glaeubiger_hausnummer': find(r'Hausnummer[:\s]+(.+?)\n'),
        'glaeubiger_plz': find(r'PLZ[:\s]+(\d{5})'),
        'glaeubiger_ort': find(r'Ort[:\s]+(.+?)\n'),
        'schuldner_name': find(r'Schuldner[:\s]+(.+?)\n'),
        'schuldner_strasse': find(r'Schuldnerstraße[:\s]+(.+?)\n'),
        'schuldner_hausnummer': find(r'Schuldnerhausnummer[:\s]+(.+?)\n'),
        'schuldner_plz': find(r'Schuldner-PLZ[:\s]+(\d{5})'),
        'schuldner_ort': find(r'Schuldner-Ort[:\s]+(.+?)\n'),
        'hauptforderung': find(r'Betrag[:\s]+([\d\.,]+)').replace(',', '.'),
        'gegenstand': find(r'Leistungsgegenstand[:\s]+(.+?)\n'),
        'amtsgericht': find(r'Amtsgericht[:\s]+(.+?)\n')
    }
