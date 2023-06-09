# Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul obsahující akce hry.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

from typing import Callable
from . import world
from .patm03_scenarios import *


def execute_command(command: str) -> str:
    """Zpracuje zadaný příkaz a vrátí odpověď hry.
    Zadaný příkaz zanalyzuje a v závislosti na aktuální aktivitě hry
    rozhodne, která akce dostane na starost jeho zpracování.
    Vrátí odpověď hry na zadaný příkaz.
    """
    command_split = command.lower().split()
    all_actions = \
        [f"'{x}'" for x in sorted(list(command_name_2_action.keys())[1:])]
    if len(command_split) == 0:
        return command_name_2_action[''].execute([]) + \
            f"\n§Dosud nezadáno: [{', '.join(all_actions)}]"

    action_name = command_split[0]

    global _used_actions
    _used_actions.add(action_name)
    used_actions_in_parentheses = {f"'{x}'" for x in _used_actions}

    not_used_actions_str = \
        ', '.join(sorted(list(set(all_actions) - used_actions_in_parentheses)))
    second_part = f"\n§Dosud nezadáno: [{not_used_actions_str}]"

    if not is_alive():
        from .patm03_scenarios import WRONG_START
        return WRONG_START.message + second_part

    if action_name not in command_name_2_action:
        return f"Tento příkaz neznám: {action_name}" + second_part

    return command_name_2_action[action_name].execute(command_split[1:]) \
        + second_part


def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra živá = aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return _alive


def conditions() -> dict[str, object]:
    """Vrátí slovník s aktuálním nastavením příznaků.
    """
    return _flags


def _initialize():
    """V rámci startu hry inicializuje všechny potřebné objekty.
    """
    from .world import initialize as world_initialize
    world_initialize()

    global _flags, _alive, _used_actions
    _flags = get_initial_sets()
    _alive = True
    _used_actions = set()


def stop() -> None:
    """Ukončí hru.
    Zadáním prázdného příkazu lze následně spustit hru znovu.
    """
    global _alive
    _alive = False


def tests() -> dict[str, object]:
    """Vrátí slovník jehož hodnotami jsou testovací funkce
    ověřující platnost vstupních podmínek pomocných akcí.
    """
    return _tests_dict


def get_usable_in_dict() -> dict[str, str]:
    """
    Vrátí slovník názvů předmětů a místnosti použití.
    """
    return _flags.get('usable_in', {})


def get_combinable_sets() -> tuple[frozenset, ...]:
    """
    Vrátí seznam dvojic předmětů, které je možné kombinovat.
    """
    return _flags.get('combinable', ())


############################################################################


class Action(world.ANamed):
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


_flags: dict[str, object] = START_STEP.sets
_alive: bool = False


# Jednotlivé akce hry

# Akce startu hry
def _start_action_execute(_: list[str]) -> str:
    """Zpracuje příkaz startu hry. Pokud je hra již spuštěna,
    vrátí chybovou hlášku. Jinak inicializuje všechny potřebné objekty.
    """
    if is_alive():
        return "Prázdný příkaz lze použít pouze pro start hry"
    _initialize()

    return START_STEP.message


_Start_action: Action = Action(
    name="",
    description="Zapne hru, pokud je vypnutá",
    execute=_start_action_execute
)


# Akce sebrání předmětu
def _take_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz sebrání předmětu. Zkontroluje počet parametrů,
    zda je zadaný předmět v aktuálním prostoru, zda je předmět přenositelný a
    zda se vejde do batohu.
    Pokud je vše v pořádku, předmět se sebere do batohu.
    """
    if len(args) == 0:
        return ('Nevím, co mám zvednout.\n'
                'Je třeba zadat název zvedaného objektu.')

    if len(args) > 1:
        return 'Příkaz zvedni má pouze jeden parametr'

    item_name = args[0]
    item = world.current_place().item(item_name)
    if item is None:
        return f'Zadaný objekt v prostoru není: {item_name}'

    if not item.movable:
        return f'Zadaný objekt není možno zvednout: {item_name}'

    if not world.BAG.add_item(item):
        return f'Zadaný objekt se už do batohu nevejde: {item_name}'

    world.current_place().remove_item(item_name)

    return get_take_message(item_name, item.weight)


_Take_action: Action = Action(
    name="vezmi",
    description="Zvedne zadaný předmět a vloží jej do batohu.",
    execute=_take_action_execute
)


# Akce přechodu do jiného prostoru
def _move_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz přechodu do jiného prostoru.
    Zkontroluje počet parametrů a zda je zadaný prostor sousedem aktuálního.
    Pokud je vše v pořádku, přesune hráče do zadaného prostoru.
    """
    if len(args) == 0:
        return ('Nevím, kam mám jít.\n'
                'Je třeba zadat název cílového prostoru.')

    if len(args) > 1:
        return 'Příkaz jdi má pouze jeden parametr'

    place_name = args[0]
    place = world.current_place().name_2_neighbor(place_name)
    if place is None:
        return f'Do zadaného prostoru se odsud jít nedá: {place_name}'

    world.set_current_place(place)
    return goto_first_part + place_details[place_name]


_Move_action: Action = Action(
    name="jdi",
    description="Přesune hráče do zadaného sousedního prostoru.",
    execute=_move_action_execute
)


def _put_down_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz položení předmětu. Zkontroluje počet parametrů,
    zda je zadaný předmět v batohu. Pokud je vše v pořádku, předmět se položí
    do aktuálního prostoru.
    """
    if len(args) == 0:
        return ('Nevím, co mám položit.\n'
                'Je třeba zadat název pokládaného objektu.')

    if len(args) > 1:
        return 'Příkaz polož má pouze jeden parametr'

    item_name = args[0]
    item = world.BAG.item(item_name)
    if item is None:
        return f'Zadaný objekt v batohu není: {item_name}'

    world.current_place().add_item(world.BAG.remove_item(item_name))

    return get_drop_message(item_name)


_Put_down_action: Action = Action(
    name="polož",
    description="Položí zadaný předmět do aktuálního prostoru.",
    execute=_put_down_action_execute
)


# Akce nápovědy
def _help_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz nápovědy. Vypíše nápovědu k použití hry.
    """
    if len(args) > 0:
        return 'Příkaz ? nemá žádné parametry.'

    return HELP


_Help_action: Action = Action(
    name="?",
    description="Vypíše nápovědu k použití hry.",
    execute=_help_action_execute
)


# Akce ukončení hry
def _end_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz ukončení hry. Ukončí hru.
    """
    if len(args) > 0:
        return 'Příkaz konec nemá žádné parametry.'

    stop()
    return 'Ukončil si hru.'


_End_action: Action = Action(
    name="konec",
    description="Ukončí hru.",
    execute=_end_action_execute
)


# Akce prozkoumání
def _search_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz prozkoumání. Zkontroluje počet parametrů,
    zde jsou skryté předměty v aktuálním prostoru a zda už je hráč
    prozkoumal. Pokud je vše v pořádku, předměty se přidají do aktuálního
    prostoru. Změní také příznak prostoru.
    """
    if len(args) > 0:
        return 'Příkaz prozkoumej nemá žádné parametry.'

    current_place = world.current_place()
    current_place_secret_items = current_place.secret_items
    if current_place_secret_items is None:
        return 'V daném prostoru nejsou žádné skryté předměty'

    if current_place_secret_items == ():
        return 'Daný prostor si již prozkoumal'

    return_message = 'Našel jsi na zemi '

    for item in current_place_secret_items:
        item_to_add = (
            world.Item(name=item,
                       movable=True,
                       usable_in=get_usable_in_dict().get(item, None),
                       weight=world.items_weights.get(item, 0)
                       ))
        current_place.add_item(item_to_add)
        return_message += f'{item_to_add.name} (váha {item_to_add.weight}kg), '

    current_place.clear_secret_items()
    global _flags
    _flags[f'{_place_translate[current_place.name]}.searched'] = True
    return return_message[:-2]


_Search_action: Action = Action(
    name="prozkoumej",
    description="Prozkoumá daný prostor a odhalí skryté předměty.",
    execute=_search_action_execute
)


# Akce použití předmětu
def _use_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz použití předmětu. Zkontroluje počet parametrů,
    zda je zadaný předmět v batohu a zda je možné ho použít v aktuálním
    prostoru. Pokud je vše v pořádku, předmět se použije a zavolá se
    funkce pro zpracování použití předmětu. Změní se také příznak braní.
    """
    if len(args) == 0:
        return 'Nevím, co chceš použít'

    if len(args) > 1:
        return 'Příkaz použij má pouze jeden parametr'

    item_name = args[0]
    item = world.BAG.item(item_name)
    if item is None:
        return f'Daný předmět nemáš v batohu: {item_name}'

    if item.usable_in is None:
        return f'Daný předmět se nedá použít: {item_name}'

    if item.usable_in.lower() != world.current_place().name.lower():
        return f'Daný předmět zde nemůžeš použít: {item_name}'

    world.BAG.remove_item(item_name)
    global _flags
    _flags['items.used'] += 1
    return _item_use_fns[item_name]()


_Use_action: Action = Action(
    name="použij",
    description="Použije zadaný předmět.",
    execute=_use_action_execute
)


# Akce kombinace předmětů
def _combine_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz kombinace předmětů. Zkontroluje počet parametrů,
    zda nejsou zadané dva stejné předměty, zda jsou předměty v batohu a
    jestli se dají spolu zkombinovat. Pokud je vše v pořádku, předměty
    se zkombinují, odeberou se z batohu a přidá se nový předmět do batohu.
    Změní se také příznak kombinace.
    """
    if len(args) != 2:
        return "Zadej dva předměty, které chceš zkombinovat"

    item_name1 = args[0]
    item_name2 = args[1]

    if item_name1 == item_name2:
        return "Zadej dva různé předměty"

    item1 = world.BAG.item(item_name1)
    item2 = world.BAG.item(item_name2)

    if item1 is None:
        return f"Předmět nemáš v batohu: {item_name1}"

    if item2 is None:
        return f"Předmět nemáš v batohu: {item_name2}"

    combine_set = frozenset({item_name1, item_name2})
    if combine_set not in get_combinable_sets():
        return ("Dané předměty se nedají zkombinovat: "
                f"{item_name1}, {item_name2}")

    world.BAG.remove_item(item_name1)
    world.BAG.remove_item(item_name2)
    new_item_name = _combine_items_names[combine_set]
    new_item = world.Item(name=new_item_name,
                          movable=True,
                          usable_in=get_usable_in_dict().get(new_item_name,
                                                             None),
                          weight=world.items_weights.get(new_item_name, 0))
    world.BAG.add_item(new_item)
    global _flags
    _flags['items.created'] += 1

    return (f'Zkombinoval si {item_name1} a {item_name2}:\n'
            'Vytvořil si nový předmět: '
            f'{new_item_name} (váha {new_item.weight}kg)')


_Combine_action: Action = Action(
    name="zkombinuj",
    description="Zkombinuje dva předměty.",
    execute=_combine_action_execute
)


# Akce výhry
def _win_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz výhry. Zkontroluje počet parametrů a zda je hráč
    u auta a má u sebe v batohu kanystr. Pokud je vše v pořádku, hra hončí
    a hráč vyhrál.
    """
    if len(args) > 0:
        return 'Příkaz naplň nemá žádné parametry.'

    if world.current_place().name != world.CAR_NAME:
        return "Nejsi u auta."

    if world.BAG.item("kanystr") is None:
        return "Ještě nemáš benzín."

    stop()
    return ('Naplnil si auto benzínem a s parťákem odjíždíte.\n'
            'Gratuluji, vyhrál jsi hru!')


_Fill_action: Action = Action(
    name="naplň",
    description="Naplní auto benzínem a vyhraje hru.",
    execute=_win_action_execute
)

# Slovník přiřazující názvy příkazů akcím
command_name_2_action: dict[str, Action] = {
    "": _Start_action,
    "vezmi": _Take_action,
    "jdi": _Move_action,
    "polož": _Put_down_action,
    "?": _Help_action,
    "konec": _End_action,
    "prozkoumej": _Search_action,
    "použij": _Use_action,
    "zkombinuj": _Combine_action,
    "naplň": _Fill_action,
}


# Akce použití předmětu
def _use_crowbar() -> str:
    """Zpracuje použití páčidla. Přidá do aktuálního prostoru sousední
    prostor s názvem "tunel".
    """
    world.current_place().add_neighbor(world.place(world.TUNNEL_NAME))
    return ('Páčidlo se rozpadlo na kousky, ale otevřel si dveře do '
            'tunelu.\n'
            'ztratil si páčidlo')


def _use_ladder() -> str:
    """Zpracuje použití žebříku. Přidá do aktuálního prostoru sousední
    prostor s názvem "benzínka".
    """
    world.current_place().add_neighbor(world.place(world.GAS_STATION_NAME))
    return ('Použil si žebřík:\n'
            'Nyní se můžeš dostat zpět z kanálu.\n'
            'ztratil si žebřík')


def _use_rope_with_hook() -> str:
    """Zpracuje použití lana s hákem. Přidá do aktuálního prostoru sousední
    prostor s názvem "autoopravna".
    """
    world.current_place().add_neighbor(world.place(world.CAR_REPAIR_SHOP_NAME))
    return ('Použil si lano_s_hákem:\n'
            'Nyní se můžeš přehoupnout přes rozpadlý most.\n'
            'ztratil si lano_s_hákem')


def _use_rocket_launcher() -> str:
    """Zpracuje použití nabitý raketomet. Přidá do aktuálního prostoru sousední
    prostor s názvem "balkon".
    """
    world.current_place().add_neighbor(world.place(world.BALCONY_NAME))
    return ('Použil si nabitý_raketomet:\n'
            'Rozbil si dveře na balkon.\n'
            'ztratil si nabitý_raketomet')


_item_use_fns: dict[str, Callable[[], str]] = {
    "páčidlo": _use_crowbar,
    "žebřík": _use_ladder,
    "lano_s_hákem": _use_rope_with_hook,
    "nabitý_raketomet": _use_rocket_launcher
}

_combine_items_names: dict[frozenset[str, ...], str] = {
    frozenset({"hák", "lano"}): "lano_s_hákem",
    frozenset({"raketa", "raketomet"}): "nabitý_raketomet",
}


# Pomocné testy

def _hidden_items_present(_: tuple[str, ...]) -> bool:
    """Zjistí, zda jsou v současném prostoru skryté předměty."""
    hidden_items = world.current_place().secret_items
    return hidden_items is not None and len(hidden_items) > 0


def _first_argument_in_bag(args: tuple[str, ...]) -> bool:
    """Zjistí, zda je první argument v batohu."""
    return world.BAG.item(args[1].lower()) is not None


def _second_argument_in_bag(args: tuple[str, ...]) -> bool:
    """Zjistí, zda je druhý argument v batohu."""
    return world.BAG.item(args[2].lower()) is not None


def _argument_usable(args: tuple[str, ...]) -> bool:
    """Zjistí, zda je první argument použitelný"""
    return get_usable_in_dict().get(args[1].lower(), None) is not None


def _argument_usable_in(args: tuple[str, ...]) -> bool:
    """Zjistí, zda je druhý argument použitelný v prostoru."""
    return world.current_place().name == get_usable_in_dict().get(
        args[1].lower(), None)


def _arguments_not_same(args: tuple[str, ...]) -> bool:
    """Zjistí, zda se argumenty nerovnají."""
    return args[1].lower() != args[2].lower()


def _arguments_combinable(args: tuple[str, ...]) -> bool:
    """Zjistí, zda jsou argumenty kombinovatelné."""
    return frozenset(map(str.lower, args[1:])) in _combine_items_names


def _in_car(_: tuple[str, ...]) -> bool:
    """Zjistí, zda je hráč v autě."""
    return world.current_place().name == world.CAR_NAME


def _has_gas(_: tuple[str, ...]) -> bool:
    """Zjistí, zda má hráč kanystr."""
    return world.BAG.item("kanystr") is not None


_tests_dict: dict[str, Callable[[tuple[str, ...]], bool]] = dict(
    hidden_items_present=_hidden_items_present,
    first_argument_in_bag=_first_argument_in_bag,
    second_argument_in_bag=_second_argument_in_bag,
    argument_usable=_argument_usable,
    argument_usable_in=_argument_usable_in,
    arguments_not_same=_arguments_not_same,
    arguments_combinable=_arguments_combinable,
    in_car=_in_car,
    has_gas=_has_gas,
)

_place_translate: dict[str, str] = dict(smetiště="junkyard", tunel="tunnel")

_used_actions: set[str] = set()
###########################################################################q
dbg.stop_mod(1, __name__)
