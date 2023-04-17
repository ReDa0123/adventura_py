#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Balíček se společnými pomocnými programy pro testy hry.¤
"""
import dbg
dbg.start_pkg(2, __name__, __doc__)
############################################################################

ERRORS:list[str] = []       # Seznam chyb odhalených při testu



############################################################################
# Odebrání diakritiky

# Převody UNICODE znaků na jejich ASCII ekvivalenty.
pairs = {
    'Á': 'A',    'á': 'a',    'Ä': 'A',   'ä': 'a',
    'Č': 'C',    'č': 'c',
    'Ď': 'D',    'ď': 'd',
    'Ë': 'E',    'ë': 'e',
    'É': 'E',    'é': 'e',    'Ě': 'E',    'ě': 'e',
    'Í': 'I',    'í': 'i',    'Ï': 'I',   'ï': 'i',
    'Ĺ': 'L',    'ĺ': 'l',    'Ľ': 'L',    'ľ': 'l',
    'Ň': 'N',    'ň': 'n',
    'Ó': 'O',    'ó': 'o',    'Ö': 'O',   'ö': 'o',
    'Ô': 'O',    'ô': 'o',
    'Ŕ': 'R',    'ŕ': 'r',    'Ř': 'R',    'ř': 'r',
    'Š': 'S',    'š': 's',
    'Ť': 'T',    'ť': 't',
    'Ú': 'U',    'ú': 'u',    'Ü': 'U',   'ü': 'u',
    'Ů': 'U',    'ů': 'u',
    'Ý': 'Y',    'ý': 'y',    'Ÿ': 'Y',   'ÿ': 'y',
    'Ž': 'Z',    'ž': 'z',
}

def to_ascii(text:str) -> str:
    """Převede zadaný kód z unikódu do ASCII,
    přičemž přehlasovaná písmena převádí znak na znak.
    Narazí-li na znak, který není ani v ASCII ani v tabulce, ohlásí chybu.
    """
    result = []
    for c in text:
        if ord(c) < 128:
            result.append(c)
        elif c in pairs:
            result.append(pairs[c])
        else:
            raise Exception(f'Nepřevoditelný znak »{c}« s kódem {ord(c)}')
    return ''.join(result)



############################################################################
dbg.stop_pkg(2, __name__)
