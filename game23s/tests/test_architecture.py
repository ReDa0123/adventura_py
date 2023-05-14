#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_ILS/game23s/tests/test_architecture.py
"""
Definuje test základní architekturu hry, jenž prověřuje,
zda portál opravdu odkazuje na objekt implementující protokol 'IPortal'
a zda metody tohoto objektu vracejí požadované objekty.
"""
import dbg; dbg.start_mod(1, __name__)
###########################################################################q

from ..api              import BasicActions, BA_eq
from ..api.interfaces   import (IPortal, IGame, IBag, IWorld, IItem, INamed,
                                IItemContainer, IPlace)
from ..api.scen_types   import SubtypeOfStep, HAPPY_NAME, BASIC_NAME
from .                  import Level
from .common.texts      import *

PRINT_PAUSE = 0.1   # Počet sekund mezi tiskem zprávy a vyhozením výjimky

__all__ = ['test_architecture_from']


###########################################################################q

# @dbg.prSEd()
def test_architecture_from(portal:IPortal, level:Level) -> None:
    """Prověřuje architekturu hry se zadaným portálem.
    
    :param portal: Portál identifikující autora a objekty hry
    """
    global PORTAL, LEVEL, HAPPY, START_STEP, GAME
    PORTAL      = portal
    LEVEL       = level
    HAPPY       = portal.NAME_2_SCENARIO()[HAPPY_NAME]
    START_STEP  = HAPPY.steps[0]

    set_message_start(PORTAL)
    verify_portal_game()    # Prověří typ objektu hry a nastaví globální GAME
    # dbg.prIN(1, f'Po verify_portal_game(): {GAME = }')
    set_message_start(GAME)
    verify_is_alive()
    verify_basic_actions()
    verify_all_actions()
    verify_tests()
    verify_execute_command()
    verify_stop()
    verify_bag()
    # verify_world()
    
    print("Test architektury OK")



###########################################################################q

def set_message_start(obj:object) -> None:
    """Nastaví úvodní text chybových zpráv."""
    global msg_start
    name = obj.__name__ if ('__name__' in dir(obj)) else str(obj)
    msg_start = f'Test objektu: {name}\n'


def ERR(description) -> None:
    """Vypíše zprávu a vyhodí chybu."""
    message = f'{N_BEFORE_N}{msg_start}{description}{N_AFTER_N}'
    print(message)
    from time import sleep
    sleep(PRINT_PAUSE)
    raise ArchitectureError(message)


class ArchitectureError(Exception):
    """Výjimka vyhazovaná při testu architektury hry."""
    def __int__(self, message:str):
        __note__ = message


@dbg.prSEd()
def no_exception(mtd_name:str, ex:Exception):
    if isinstance(ex, ArchitectureError):  return
    ERR(f'Volání metody {mtd_name}() nesmí vyhazovat výjimku:\n{ex}')


###########################################################################q

# @dbg.prSEd()
def verify_portal_game() -> IGame:
    """Prověří, že portál vrací odkaz na hru."""
    global PORTAL, GAME
    try:
        GAME = PORTAL.GAME()
    except:
        raise ArchitectureError("Funkce GAME() nevrací odkaz na hru")
    if isinstance(GAME, IGame):  return
    needed   = [name for name in dir(IGame) if not name.startswith('_')]
    obtained = [name for name in dir(GAME)  if not name.startswith('_')]
    ERR(f'Metoda GAME() vrací objekt {GAME}\n'
        f'jenž neimplementuje protokol game23s.api.interfaces.IGame\n'
        f'{dbg.prIndLim("  Požadované atributy: ", needed)}\n'
        f'{dbg.prIndLim("  Obdržené atributy:   ", obtained)}')


# @dbg.prSEdr()
def verify_is_alive() -> None:
    # dbg.prIN(1, f'{GAME = }')
    correct = False
    try:
        # dbg.prIN(1, f'{GAME = }\n{dbg.prDict(GAME, prn=False)}')
        result = GAME.is_alive()
        correct = (result is not None)  and  (not result)
    except Exception as ex:
        no_exception('is_alive',ex)
    if correct: return
    ERR('Metoda isAlive() nevrací False oznamující, že hra neběží.\n'
        'Vracet None nestačí.')


# @dbg.prSEd()
def verify_basic_actions() -> None:
    ba = {}
    for step in PORTAL.NAME_2_SCENARIO()[BASIC_NAME].steps:
        command = step.command.strip()
        if not command: continue
        ba[step.typeOfStep.name] = command.split()[0]
    success = HAPPY.steps[-1].command.strip().lower()
    ba[HAPPY.steps[-1].typeOfStep.name] = success
    expected = BasicActions(MOVE_NAME=ba['tsGOTO'], END_NAME=ba['tsEND'],
               PUT_DOWN_NAME=ba['tsPUT_DOWN'], TAKE_NAME=ba['tsTAKE'],
               HELP_NAME=ba['tsHELP'], SUCCESS_NAME=ba['tsSUCCESS']
               )
    try:
        obtained = None
        obtained = GAME.basic_actions()
        if not BA_eq(expected, obtained):
        # if expected != obtained:
            ERR(f'Metoda basic_actions() nevrací správně názvy '
                                               f'základních akcí\n'
                f'{dbg.prIndLim("  Očekáváno: ", expected)}\n'
                f'{dbg.prIndLim("  Obdrženo:  ", obtained)}' )
    except Exception as ex:
        no_exception('basic_actions',ex)


def verify_all_actions() -> None:
    try:
        actions = GAME.all_actions()
    except Exception as ex:
        # Do hladiny MISTAKES je povolené vyvolání výjimky
        if LEVEL <= Level.MISTAKES:  return
        raise ex


def verify_tests() -> None:
    try:
        actions = GAME.tests()
    except Exception as ex:
        # Do hladiny RUNNING je povolené vyvolání výjimky
        if LEVEL < Level.RUNNING:  return
        raise ex


# @dbg.prSEd()
def verify_execute_command() -> None:
    start_err = "Odpověď hry po odstartování příkazem executeCommand('')\n"
    try:
        expected = START_STEP.message.lower()
        exp_len  = len(expected)
        answer   = GAME.execute_command('')
        if len(answer) < exp_len:
            ERR(start_err + 'je kratší než objednává scénář HAPPY')
        obtained = answer[:exp_len].lower()
        if expected == obtained:  return
        ERR(start_err + 'se liší od požadované')
    except Exception as ex:
        no_exception('execute_command', ex)


def verify_stop() -> None:
    try:
        GAME.stop()
    except Exception as ex:
        no_exception('stop', ex)


# @dbg.prSEd()
def verify_bag() -> None:
    try:
        bag  = GAME.bag()
        bag2 = GAME.bag()
        if bag is not bag2:
            ERR('Batoh vracený metodou bag() není jedináček')
    except Exception as ex:
        no_exception('bag', ex)
    if bag == None:
        ERR('Metoda bag() nevrací požadovaný batoh')
    # dbg.prIN(1, 'Jdu kontrolovat implementaci')
    # if not isinstance(bag, IBag):
    #     ERR('Třída batohů neimplementuje protokol IBag')
    # TODO Zkontrolovat, proč to nechodí
    # dbg.prIN(1, 'Implementace zkontrolována')
    
    set_message_start(bag)
    


# def verify_world() -> None:





###########################################################################q

PORTAL:IPortal          = None  # Testovaný portál
LEVEL:Level             = None  # Testovaná hladina rozpracovanosti
HAPPY:'Scenario'        = None  # Šťastný scénář testované aplikace
START_STEP:'ScenarioStep'=None  #Počáteční krok scénářů
msg_start:str           = ''    # Úvodní text chybových zpráv
GAME:IGame              = None  # Odkaz na testovanou hru



###########################################################################q
dbg.stop_mod(1, __name__)
