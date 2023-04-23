# Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul obsahující akce hry.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

from typing import Callable
from .world import ANamed
from .patm03_scenarios import START_STEP


def execute_command(command: str) -> str:
    """Zpracuje zadaný příkaz a vrátí odpověď hry.
    Zadaný příkaz zanalyzuje a v závislosti na aktuální aktivitě hry
    rozhodne, která akce dostane na starost jeho zpracování.
    Vrátí odpověď hry na zadaný příkaz.
    """
    command_split = command.split()
    if len(command_split) == 0:
        return command_name_2_action[''].execute([])

    action_name = command_split[0]
    if action_name not in command_name_2_action:
        return f"Tento příkaz neznám: {action_name}"

    return command_name_2_action[action_name].execute(command_split[1:])


def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra živá = aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return alive


def conditions() -> dict[str, object]:
    """Vrátí slovník s aktuálním nastavením příznaků.
    """
    return _flags


def _initialize():
    """V rámci startu hry inicializuje všechny potřebné objekty.
    """
    global _flags, alive
    _flags = START_STEP.sets
    alive = True

def stop() -> None:
    """Ukončí hru.
    Zadáním prázdného příkazu lze následně spustit hru znovu.
    """
    global alive
    alive = False


############################################################################


class Action(ANamed):
    """Společná rodičovská třída všech akcí.
    """

    def __init__(self, name: str, description: str,
                 execute: Callable[[list[str]], str]):
        """Vytvoří instanci, která si zapamatuje
        název dané akce a její popis.
        """
        super().__init__(name=name)
        self._description = description
        self.execute = execute

    @property
    def description(self) -> str:
        """Vrátí popis příkazu s vysvětlením jeho funkce,
        významu jednotlivých parametrů a možností (resp. účelu) použití
        daného příkazu. Tento popis tak může sloužit jako nápověda
        k použití daného příkazu.
        """
        return self._description

    execute: Callable[[list[str]], str] = None
    """Metoda realizující reakci hry na zadání daného příkazu.
    Předávané pole je vždy neprázdné, protože jeho nultý prvek
    je zadaný název vyvolaného příkazu. Počet argumentů je závislý
    na konkrétním akci, ale pro každou akci je konstantní.
    """


_flags: dict[str, object] = dict()
alive: bool = False


# Jednotlivé akce hry

# Akce startu hry
def _start_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz startu hry.
    """
    if is_alive():
        return "Hra již byla spuštěna."
    _initialize()

    from .world import initialize as world_initialize
    world_initialize()

    return START_STEP.message


Start_action = Action(
    name="",
    description="Zapne hru, pokud je vypnutá",
    execute=_start_action_execute
)

# Akce

# Slovník přiřazující názvy příkazů akcím
command_name_2_action: dict[str, "Action"] = {
    "": Start_action,
}

###########################################################################q
dbg.stop_mod(1, __name__)
