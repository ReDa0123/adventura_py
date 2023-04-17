#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul s převodními funkcemi.
"""
import dbg
dbg.start_mod(2, __name__)
############################################################################
# Konverze znaků s diakritikou

CONVERSION = {
    "Á":"A",  "á":"a",    "Ä":"AE", "ä":"ae",
    "Č":"C",  "č":"c",
    "Ď":"D",  "ď":"d",
    "Ë":"E",  "ë":"e",
    "É":"E",  "é":"e",    "Ě":"E",  "ě":"e",
    "Í":"I",  "í":"i",    "Ï":"I",  "ï":"i",   # "Ï":"IE", "ï":"ie",
    "Ĺ":"L",  "ĺ":"l",    "Ľ":"L",  "ľ":"l",
    "Ň":"N",  "ň":"n",
    "Ó":"O",  "ó":"o",    "Ö":"O",  "ö":"o",   # "Ö":"OE", "ö":"oe",
    "Ô":"O",  "ô":"o",
    "Ŕ":"R",  "ŕ":"r",    "Ř":"R",  "ř":"r",
    "Š":"S",  "š":"s",
    "Ť":"T",  "ť":"t",
    "Ú":"U",  "ú":"u",    "Ü":"U",  "ü":"u",   # "Ü":"UE", "ü":"ue",
    "Ů":"U",  "ů":"u",
    "Ý":"Y",  "ý":"y",    "Ÿ":"Y",  "ÿ":"y",   # "Ÿ":"YE", "ÿ":"ye",
    "Ž":"Z",  "ž":"z",
    "ß":"ss",
    "„":"\"", "“":"\"",   "”":"\"",
    "‚":"\'", "‘":"\'",   "’":"\'",
    "×":"x",  "÷":":",
    "–":"-",  "—":"-",    # ndash, mdash
    "¦":"|",
    "‹":"<",  "›":">",    "«":"<<", "»":">>",
    "©":"(c)","®":"(R)",
    "\xA0":" ",           # nbsp
}

def uni2asc(text:str) -> str:
    """Převede zadaný text do ekvivalentního tvaru bez diakritických
    znamének a dalších ne-ASCII znaků přičemž používá i dvouznakové převody
    a převody na escape-sekvence.
    Znaky chybějící v převodní tabulce převede na odpovídající
    escape-sekvenci typu \\x, \\u, \\U.
    """
    result = []
    for c in text:
        if ord(c) < 128:
            result.append(c)
        elif c in CONVERSION:
            result.append(CONVERSION[c])
        else:
            result.append(ascii(c))
    return ''.join(result)



############################################################################
dbg.stop_mod(2, __name__)
