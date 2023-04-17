#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Dokumentační komentář modulu.
"""
import dbg
dbg.start_mod(2, __name__)
############################################################################

from ...api.interfaces import INamed



############################################################################

# TODO Porovnat sloučení s containers_differs v modulu test_game
# @dbg.prSEdr(msg='from tests.common.utils')
def containers_differs(str_cont:tuple[str], named_cont:tuple[INamed]):
    """Porovná názvy v kontejneru str_cont s názvy objektů
    v kontejneru named_cont bez ohledu na velikost písmen.
    Budou-li se lišit, vrátí dvojici stringů s jejich obsahy,
    nebudou-li se lišit, vrátí False.
    Jako vedlejší efekt si funkce nastaví své atributy
    from_scenario a from_game, v nichž uchovává příslušné názvy.
    """
    if not ('__iter__' in dir(named_cont)):
        raise Exception('Testovaný objekt hry není kontejner')
    from_scenario = sorted([item     .lower() for item in str_cont])
    from_game     = sorted([item.name.lower() for item in named_cont])
    result = False if from_scenario == from_game \
             else (f'{from_scenario}', f'{from_game}', )
    containers_differs.from_scenario = from_scenario
    containers_differs.from_game     = from_game
    return result



############################################################################
dbg.stop_mod(2, __name__)
