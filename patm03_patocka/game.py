# Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul obsahující základ hry.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

from game23s.api import BasicActions
from game23s.api.interfaces import IAction, IBag, IWorld


def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
       Spuštěnou hru není možno pustit znovu.
       Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return False


def execute_command(command: str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """
    from .patm03_scenarios import START_STEP
    return START_STEP.message


def stop() -> None:
    """Ukončí hru a uvolní alokované prostředky.
       Zadáním prázdného příkazu lze následně spustit hru znovu.
    """


def all_actions() -> tuple[IAction]:
    """Vrátí n-tici všech akcí použitelných ve hře.
    """
    raise Exception(f'Ještě není plně implementováno')


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
    from .world import BAG
    return BAG


def world() -> IWorld:
    """Vrátí odkaz na svět hry.
    """
    raise Exception(f'Ještě není plně implementováno')


def conditions() -> dict[str, object]:
    """Vrátí slovník s aktuálním nastavením příznaků.
    """
    from .patm03_scenarios import START_STEP
    return START_STEP.sets


def tests() -> dict[str, object]:
    """Vrátí slovník jehož hodnotami jsou testovací funkce
        ověřující platnost vstupních podmínek pomocných akcí.
        """
    raise Exception(f'Ještě není plně implementováno')


###########################################################################q
dbg.stop_mod(1, __name__)
