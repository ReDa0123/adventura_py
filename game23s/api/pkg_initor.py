#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/api/pkg_initor.py
"""
Modul deklaruje metody požadované od modulů odevzdávaných jako
realizace konkrétní hry. Tyto metody mají za úkol identifikovat autora
a zprostředkovat komunikaci s klíčovými objekty dané aplikace.

Místo tohoto komentáře sem pište své dotazy a připomínky.
Nemáte-li je, napište: Žádné
"""
import dbg; dbg.start_pkg(2, __name__)
###########################################################################q

# Login autora/autorky programu zadaný VELKÝMI PÍSMENY
AUTHOR_ID = 'NEZADÁNO'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
# tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
# u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
# Má-li autor programu více křestních jmen, může je uvést všechna.
AUTHOR_NAME = 'NEZADÁNO'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní
# zapsané v jeho/jejím rodném jazyce
AUTHOR_NATIVE_NAME = 'NEZADÁNO'

# Čas začátku kroužku, který navštěvujete
GROUP_TIME = '0000'  # Zadejte čtyřčíslí odpovídající času začátku kroužku



###########################################################################q

def NAME_2_SCENARIO(self):
    """Vrátí odkaz na slovník převádějící názvy scénářů na dané scénáře
    Scénáře musejí být instancemi třídy `game23s.api.scenario.Scenario`
    """


def GAME(self):
    """Vrátí odkaz na hru, která musí implementovat protokol
    `game23s.api.interfaces.IGame`
    """


###########################################################################q
# Testy

def self_test():
    """Otestuje, zda stav projektu odpovídá zadané hladině.
    """
    from importlib import import_module
    me = import_module(__package__)   # Importuje modul svého balíčku
    test(me, LEVEL)         # Testuje implementaci na nastavené hladině


# Přípustné hladiny - na dané hladině se testuje:
# PORTAL       Jenom initor balíčku
# HAPPY         Jen šťastný scénář
# SCENARIOS     Čtyři základní scénáře: startovní, šťastný,
#               chybový a chybový scénář nadstandardních akcí
# ARCHITECTURE  Přítomnost požadovaných objektů a metod
# START         Hra úspěšně odstartuje
# WORLD         Hra úspěšně vybuduje svůj svět
# BASIC         Zprovoznění základních akcí
# MISTAKES      Základní akce jsou navržené robustní
# WHOLE         Úspěšné zprovoznění celé hry

# Nastavení hladiny rozpracovanosti aplikace
from game23s.tests import Level, test
LEVEL = Level.HAPPY


# Test spustíte nastavením požadované hladiny a zadáním příkazů:
# import game23s.název_vašeho_balíčku as at; at.self_test()



###########################################################################q
dbg.stop_pkg(2, __name__)
