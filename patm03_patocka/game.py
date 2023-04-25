# Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul obsahující základ hry.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

from game23s.api import BasicActions
from game23s.api.interfaces import IAction, IBag, IWorld

from . import actions
from . import world as w


def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
       Spuštěnou hru není možno pustit znovu.
       Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return actions.is_alive()


def execute_command(command: str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """
    return actions.execute_command(command)


def stop() -> None:
    """Ukončí hru a uvolní alokované prostředky.
       Zadáním prázdného příkazu lze následně spustit hru znovu.
    """
    actions.stop()


def all_actions() -> tuple[IAction]:
    """Vrátí n-tici všech akcí použitelných ve hře.
    """
    return tuple(actions.command_name_2_action.values())


def basic_actions() -> BasicActions:
    """Vrátí přepravku s názvy povinných akcí.
    """
    return BasicActions(
        MOVE_NAME='jdi',
        PUT_DOWN_NAME='polož',
        TAKE_NAME='vezmi',
        HELP_NAME='?',
        END_NAME='konec',
        SUCCESS_NAME='naplň',
    )


def bag() -> IBag:
    """Vrátí odkaz na batoh, do nějž bude hráč ukládat sebrané objekty.
    """
    return w.BAG


def world() -> IWorld:
    """Vrátí odkaz na svět hry.
    """
    return w


def conditions() -> dict[str, object]:
    """Vrátí slovník s aktuálním nastavením příznaků.
    """
    return actions.conditions()


def tests() -> dict[str, object]:
    """Vrátí slovník jehož hodnotami jsou testovací funkce
        ověřující platnost vstupních podmínek pomocných akcí.
        """
    return {}


###########################################################################q
dbg.stop_mod(1, __name__)
