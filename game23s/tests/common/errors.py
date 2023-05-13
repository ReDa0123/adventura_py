#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""\
Dokumentační komentář modulu.
"""
import dbg
dbg.start_mod(2, __name__)
############################################################################

from .texts import *

from ...api.interfaces  import INamed, IGame, IPortal
from ...api.scenario    import ScenarioStep, Scenario
from ...api import BasicActions, state_of



############################################################################

def error(reason:str, scenario:Scenario, step:ScenarioStep, game:IGame,
          expected:(tuple[str]|str), obtained:(list[INamed]|str)) -> None:
    """
    Zobrazí chybové hlášení upozorňující na příčinu chyby
    zapříčiněnou nesouhlasem objektů scénáře a hry.

    :param reason:   Text popisující důvod chyby
    :param scenario: Scénář, při jehož testování byla chyba objevena
    :param step:     Prověřovaný krok scénáře
    :param game:     Testovaná hra
    :param expected: Očekávaný stav hry
    :param obtained: Obdržený stav hry
    :return: Vyhodí výjimku
    """
    NL = '\n'
    message = (f'{3*(70*"E"+NL)}'
               f'Při vyhodnocování {step.index}. kroku scénáře '
               # f'{game.__package__.__name__} - '
               f'{scenario.name} byla odhalena chyba:\n{60*"-"}\n'
               f'Chybný objekt:    {reason}\n'
               f'Očekávaný objekt: {str(expected)}\n'
               f'Obdržený objekt:  {str(obtained)}\n\n')
    print(message)
    print(f'Očekávaný stav hry po provedení testovaného příkazu:\n'
          f'{step}')
    print(f'\nObdržený stav hry po provedení testovaného příkazu:')
    print(f'{state_of(game)}')
    from time import sleep
    sleep(.5)   # Půl vteřiny počká, aby doběhly ostatní tisky
    raise Exception(f'{scenario.name}: {reason}')



############################################################################

class CompareException:
    """Výjimka vyhazovaná při objevu závažných chyb v průběhu testování.
    """



############################################################################
#
# def clear_err_msgs():
#     """Vyčistí seznam chybových zpráv na počátku dalšího testu.
#     """
#     _ERR_MSGs.clear()
#
#
# def get_err_msgs():
#     """Vrátí kopii seznamu chybových zpráv.
#     """
#     return _ERR_MSGs[:]
#
#
# def add_err_msg(err_msg:str):
#     """Přidá do seznamu chybových zpráv další zprávu.
#     """
#     _ERR_MSGs.append(err_msg)
#



############################################################################

_ERR_MSGs:list[str] = []



############################################################################
dbg.stop_mod(2, __name__)
