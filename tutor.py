import random
from prompt_toolkit import prompt
import colorama
from parser import sammlung_auswählen, Sammlung
from dienstprogramme import levenshtein_distanz


def fang_an_zu_studieren(sammlung: Sammlung):
    n = len(sammlung.objekte)
    while True:
        try:
            i = random.randint(0, n - 1)
            j = random.randint(0, 1)
            if j:
                gegeben = sammlung.objekte[i].deutsch
                erwartet = sammlung.objekte[i].englisch
                zielsprache = 'Englisch'
            else:
                gegeben = sammlung.objekte[i].englisch
                erwartet = sammlung.objekte[i].deutsch
                zielsprache = 'Deutsch'
            s = f'Bitte übersetzen Sie {colorama.Fore.YELLOW}{gegeben}{colorama.Fore.RESET} in {zielsprache}'
            print(s)
            übersetzung = prompt()
            # print(übersetzung)
            print(erwartet)
            if zielsprache == 'Deutsch':
                s0 = übersetzung
                s1 = erwartet
            else:
                s0 = übersetzung.lower()
                s1 = erwartet.lower()
            distanz = levenshtein_distanz(s0, s1)
            HÖCHSTE_ERGEBNIS = 4
            if len(übersetzung) == 0:
                ergebnis = HÖCHSTE_ERGEBNIS
            else:
                ergebnis = distanz / len(s0)
                ergebnis = max(ergebnis, HÖCHSTE_ERGEBNIS)
            if distanz == 0:
                print(f'{colorama.Style.BRIGHT}CORRECT!{colorama.Style.NORMAL}')
            elif distanz < 0.01:
                print(f'{colorama.Style.YELLOW}ALMOST CORRECT!{colorama.Style.NORMAL}')
            else:
                print(f'{colorama.Fore.RED}WRONG!{colorama.Fore.RESET} Ergebnis = {ergebnis}')
            sammlung.ergebnis_aktualisieren(ergebnis, sammlung.objekte[i])
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    while True:
        try:
            sammlung = sammlung_auswählen()
            fang_an_zu_studieren(sammlung)
            # for objekt in sammlung.objekte:
            #     print(objekt.deutsch, '|', objekt.englisch, '|', objekt.metadaten)
        except KeyboardInterrupt:
            break
