"""
Phase1_LinguisticAnalyzer – Fáza 1: Jazyková a štruktúrna analýza
"""
import spacy
from src.ae_parser import main as ae_parser_main

class Phase1LinguisticAnalyzer:
    def __init__(self):
        self.nlp = spacy.blank('xx')  # Základný multijazykový model, vymeniť za sk_core_news_sm pre slovenčinu
        # self.ae_parser = ae_parser_main  # Príprava na AST validáciu

    def process(self, input_path):
        # TODO: Rozpoznať typ vstupu (HTML/JSON), extrahovať bloky
        # TODO: Validovať JSON bloky cez ae_parser
        # TODO: Čistiť a normalizovať text
        # TODO: Tokenizácia, lemmatizácia, POS tagging, NER, syntaktický parsing
        # TODO: Identifikovať štruktúry (otázky, rozhodnutia, hypotézy, emócie)
        # Návratová štruktúra: list blokov s lingvistickými atribútmi
        return []
