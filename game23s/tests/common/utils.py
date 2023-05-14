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
def containers_differs(scen_cont:tuple[str],
                       game_cont:tuple[INamed]) -> bool:
    """
    Porovná názvy v kontejneru scen_cont deklarované ve scénáři
    s názvy pojmenovaných objektů v kontejneru game_cont obdrženého od hry
    bez ohledu na velikost písmen.
    Budou-li se lišit, vrátí dvojici stringů s porovnávanými názvy,
    nebudou-li se lišit, vrátí False.
    Jako vedlejší efekt si funkce nastaví své atributy
    from_scenario a from_game, v nichž uchovává příslušné názvy.
    
    :param scen_cont:   Kontejner scénáře s názvy položek
    :param game_cont:   Kontejner hry s pojmenovanými objekty
    :return: Pokud se kontejnery liší, vrátí True, jinak vrátí False
    """
    if not ('__iter__' in dir(game_cont)):
        raise Exception('Testovaný objekt hry není kontejner')
    from_scenario = sorted([item     .lower() for item in scen_cont])
    from_game     = sorted([item.name.lower() for item in game_cont])
    result = False if from_scenario == from_game \
             else (f'{from_scenario}', f'{from_game}', )
    containers_differs.from_scenario = from_scenario
    containers_differs.from_game     = from_game
    return result



############################################################################
dbg.stop_mod(2, __name__)
