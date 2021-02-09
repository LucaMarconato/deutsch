import hashlib
import sqlite3
import pickle
import os
import re
from typing import List

PICKLE_VERZEICHNIS = 'pickles'
os.makedirs(PICKLE_VERZEICHNIS, exist_ok=True)


class Ergebnis:
    def __init__(self, terminzeit, wert=-1):
        self.terminzeit = terminzeit
        self.wert = -1


class Metadaten:
    def __init__(self):
        self.chronologie: List[Ergebnis] = []

    def hash_berechnen(self):
        h = hashlib.sha256()
        for ergebnis in self.chronologie:
            s = ergebnis.terminzeit + '_' + str(ergebnis.wert)
            h.update(s.encode('utf-8'))
        hex = h.hexdigest()
        return hex[:10]

    def zu_pickle(self):
        hex_ = self.hash_berechnen()
        dateipfad = os.path.join(PICKLE_VERZEICHNIS, hex)
        pickle.dump(self.chronologie, open(dateipfad, 'wb'))
        return hex_

    @classmethod
    def von_pickle(cls, hex):
        dateipfad = os.path.join(PICKLE_VERZEICHNIS, hex)
        assert os.path.isfile(dateipfad)
        chronologie = pickle.load(open(dateipfad, 'rb'))
        metadaten = Metadaten()
        metadaten.chronologie = chronologie
        return metadaten


# def metadaten_einfügen()
# def metadaten_initialisieren():


def verlassen_pickles_reinigen():
    alle_pickles = [p.split('.pickle')[0] for p in os.listdir(PICKLE_VERZEICHNIS) if p.endswith('.pickle')]

    wurzelverzeichnis = os.path.expanduser('~/Dropbox/org/notes/learning/german/')
    dateien = [d for d in os.listdir(wurzelverzeichnis) if d.startswith('german_')]
    dateipfade = [os.path.join(wurzelverzeichnis, d) for d in dateien]
    dateipfade = [d for d in dateipfade if os.path.isfile(d)]
    aktiv_pickles = []
    for dateipfad in dateipfade:
        with open(dateipfad) as f:
            zeilen = f.readlines()
            for zeile in zeilen:
                if zeile.startswith('+ [ ] '):
                    zeile = zeile.rstrip()
                    m = re.search(r'hex:"(.*?)"$', zeile)
                    if m is not None:
                        hex_ = m.group(1)
                        aktiv_pickles.append(hex_)
    zu_reinigen = set(alle_pickles).difference(aktiv_pickles)
    print('inaktiv pickles:', zu_reinigen)


if __name__ == '__main__':
    verlassen_pickles_reinigen()
    pass

# DATENBANKDATEI = './metadaten.sqlite'
# def verbindung_herstellen():
#     conn = None
#     try:
#         conn = sqlite3.connect(DATENBANKDATEI)
#     except sqlite3.Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()
