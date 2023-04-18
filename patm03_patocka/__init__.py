#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
NIC
"""
import dbg; dbg.start_pkg(1, __name__)
###########################################################################q

# Login autora/autorky programu zadaný VELKÝMI PÍSMENY
AUTHOR_ID = 'PATM03'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní,
# tj. nejprve příjmení psané velkými písmeny a za ním křestní jméno,
# u nějž bude velké pouze první písmeno a ostatní písmena budou malá.
# Má-li autor programu více křestních jmen, může je uvést všechna.
AUTHOR_NAME = 'PATOCKA Martin'

# Jméno autora/autorky programu ve formátu PŘÍJMENÍ Křestní
# zapsané v jeho/jejím rodném jazyce
AUTHOR_NATIVE_NAME = 'PATOČKA Martin'

# Čas začátku kroužku, který navštěvujete
GROUP_TIME = '2_0915'  # Zadejte čtyřčíslí odpovídající času začátku kroužku



###########################################################################q

def NAME_2_SCENARIO():
    """Vrátí odkaz na slovník převádějící názvy scénářů na dané scénáře
    Scénáře musejí být instancemi třídy `game23s.api.scenario.Scenario`
    """
    from . import patm03_scenarios
    return patm03_scenarios.NAME_2_SCENARIO


def GAME():
    """Vrátí odkaz na hru, která musí implementovat protokol
    `game23s.api.interfaces.IGame`
    """
    from . import game
    return game



###########################################################################q
# Testy

# Definované hladiny - na dané hladině se testuje:
# PORTAL      = 0 #_ Jenom initor balíčku
# HAPPY       = 1 #a Jen šťastný scénář
# SCENARIOS   = 2 #b Čtyři základní scénáře: 1. šťastný, 2. startovní,
#                 #c 3. chybový a 4. chybový scénář nestandardních akcí
# ARCHITECTURE= 3 #d Přítomnost požadovaných objektů a metod
# START       = 4 #e Hra úspěšně odstartuje
# WORLD       = 5 #f Hra úspěšně vybuduje svůj svět
# BASIC       = 6 #g Zprovoznění základních akcí při korektním zadání
# MISTAKES    = 7 #h Základní akce jsou navržené robustní
# RUNNING     = 8 #i Zprovoznění všech akcí při korektním zadání
# WHOLE       = 9 #j Úspěšné zprovoznění hry, všechny akce jsou robustní
# MODIFIED    =10 #k Aplikace s nadstavbovými úpravami pro obhajobu
# EXTENDED    =11 #l Aplikace upravená pro obhajobu s dalším scénářem


def self_test():
    """
    Otestuje, zda stav projektu odpovídá zadané hladině rozpracovanosti.
    """
    import game23s.tests as gt
    LEVEL = gt.Level.ARCHITECTURE  # Nastavení hladiny rozpracovanosti aplikace

    # Hladiny SUMMARY=0, DETAILS=1, STEPS=2, STEP_ATTR=3
    gt.VERBOSITY = gt.Verbosity.STEP_ATTR

    from importlib import import_module
    me = import_module(__package__)   # Importuje modul svého balíčku
    gt.test(me, LEVEL)        # Testuje implementaci na nastavené hladině


# Test spustíte nastavením požadované hladiny a zadáním příkazů:
# import a1b_all as m; m.self_test()


###########################################################################q
dbg.stop_pkg(1, __name__)
