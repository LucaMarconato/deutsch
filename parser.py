import os
import datetime
import random
import re
from typing import List
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from metadaten_manager import Metadaten, Ergebnis

a = os.getenv('PYCHARM_HOSTED')
if a is not None:
    WIRD_AUSGEFÜHRT_IN_PYCHARM = int(a)
else:
    WIRD_AUSGEFÜHRT_IN_PYCHARM = False


class LernbaresObjekt:
    def __init__(self, deutsch, englisch):
        self.deutsch = deutsch
        self.englisch = englisch
        self.metadaten = None


class Sammlung:
    def __init__(self, titel):
        self.titel = titel
        self.objekte: List[LernbaresObjekt] = []

    def lernbares_objekt_anhängen(self, objekt):
        self.objekte.append(objekt)

    def ergebnis_aktualisieren(self, ergebnis: float, lernbares_objekt: LernbaresObjekt):
        wurzelverzeichnis = os.path.expanduser('~/Dropbox/org/notes/learning/german/')
        dateinamen = f'german_{self.titel}.org'
        dateipfad = os.path.join(wurzelverzeichnis, dateinamen)
        assert os.path.isfile(dateipfad)
        neue_zeilen = []
        gefundene_anzahl = 0
        with open(dateipfad) as f:
            zeilen = f.readlines()
            for zeile in zeilen:
                neue_zeilen.append(zeile)
                if zeile.startswith('+ [ ] '):
                    zeile = zeile.rstrip()
                    deutsch, englisch, metadaten = zeile_analysieren(zeile)
                    if deutsch == lernbares_objekt.deutsch and englisch == lernbares_objekt.englisch:
                        gefundene_anzahl += 1
                        terminzeit = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        neue_ergebnis = Ergebnis(terminzeit, ergebnis)
                        if metadaten is None:
                            metadaten = Metadaten()
                        MAXIMALE_CHRONOLOGISCHE_LÄNGE = 5
                        metadaten.chronologie.append(neue_ergebnis)
                        if len(metadaten.chronologie) > MAXIMALE_CHRONOLOGISCHE_LÄNGE:
                            del metadaten.chronologie[0]
                        del neue_zeilen[-1]
                        neue_hex = metadaten.zu_pickle()
                        if len(metadaten.chronologie) == MAXIMALE_CHRONOLOGISCHE_LÄNGE and all(
                                ergebnis.wert < 0.0001 for ergebnis in metadaten.chronologie):
                            gelernt = 'X'
                        else:
                            gelernt = ' '
                        neue_zeile = f'+ [{gelernt}] {deutsch}: {englisch} x"{neue_hex}"\n'
                        neue_zeilen.append(neue_zeile)
        s = ''.join(neue_zeilen)
        with open(dateipfad, 'w') as f:
            print(s, file=f)


def zeile_analysieren(zeile: str):
    teil = zeile.rstrip().split('+ [ ] ')[1]
    assert teil.count(':') == 1
    deutsch, englisch_und_metadaten = teil.split(': ')
    m = re.search(r' x"(.*?)"$', englisch_und_metadaten)
    if m is None:
        englisch = englisch_und_metadaten
        metadaten = None
    else:
        englisch = englisch_und_metadaten.split(' x"')[0]
        hex = m.group(1)
        metadaten = Metadaten.von_pickle(hex)
    return deutsch, englisch, metadaten


def objekte_analysieren() -> List[Sammlung]:
    wurzelverzeichnis = os.path.expanduser('~/Dropbox/org/notes/learning/german/')
    datein = [f for f in os.listdir(wurzelverzeichnis) if f.startswith('german_')]
    dateipfade = [os.path.join(wurzelverzeichnis, f) for f in datein]
    dateipfade = [f for f in dateipfade if os.path.isfile(f)]

    sammlungen = []

    for dateipfad in dateipfade:
        titel = os.path.basename(dateipfad).split('_')[1].split('.org')[0]
        sammlung = Sammlung(titel)
        sammlungen.append(sammlung)
        with open(dateipfad) as f:
            zeilen = f.readlines()
        for zeile in zeilen:
            if zeile.startswith('+ [ ] '):
                deutsch, englisch, metadaten = zeile_analysieren(zeile)
                objekt = LernbaresObjekt(deutsch, englisch)
                objekt.metadaten = metadaten
                sammlung.lernbares_objekt_anhängen(objekt)
    return sammlungen


def sammlung_auswählen() -> Sammlung:
    sammlungen = objekte_analysieren()
    alle_titel = [sammlung.titel for sammlung in sammlungen]

    if not WIRD_AUSGEFÜHRT_IN_PYCHARM:
        vervollständiger = WordCompleter(alle_titel, ignore_case=True)
        wahl = prompt(
            'Was möchtest du studieren? ',
            completer=vervollständiger,
            complete_style=CompleteStyle.MULTI_COLUMN,
        )
        if wahl == '':
            wahl = random.sample(alle_titel, 1)[0]
    else:
        wahl = alle_titel[1]
    ausgewählt = [sammlung for sammlung in sammlungen if sammlung.titel == wahl]
    assert len(ausgewählt) == 1
    return ausgewählt[0]
