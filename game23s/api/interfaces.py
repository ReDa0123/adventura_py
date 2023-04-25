#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/api/interfaces.py
"""
Protokoly deklarující povinné atributy klíčových objektů
v odevzdaných semestrálních pracech.
Nebude-li některý z nich definován jako instance běžné třídy,
ale jako modul, odebere se ze seznamu parametrů parametr self.

Definované protokoly:
    INamed(Protocol)
    IItem(INamed)
    IItemContainer(Protocol)
    IBag(IItemContainer)
    IPlace(IItemContainer, INamed)
    IWorld(Protocol)
    IAction(Protocol)
    IGame(Protocol)

Definované třídy
    BasicActions

"""
import dbg; dbg.start_mod(2, __name__)
############################################################################

from typing   import Callable, Protocol, runtime_checkable
from ..api    import BasicActions



############################################################################

@runtime_checkable
class INamed(Protocol):
    """Instance představují objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Inicializuje objekt zadaným názvem.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def name(self) -> str:
        """Vrátí název daného objektu.
        """
        raise Exception(f'Ještě není plně implementováno')


    def __str__(self) -> str:
        """Vrátí uživatelský textový podpis jako název dané instance.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IItem(INamed, Protocol):
    """Instance představují h-objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Vytvoří h-objekt se zadaným názvem.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IItemContainer(Protocol):
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names:tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """
        raise Exception(f'Ještě není plně implementováno')


    def initialize(self) -> None:
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def items(self) -> list[IItem]:
        """Vrátí n-tici objektů v daném kontejneru.
        """
        raise Exception(f'Ještě není plně implementováno')


    def item(self, name:str) -> IItem:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """
        raise Exception(f'Ještě není plně implementováno')


    def add_item(self, item:IItem) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        raise Exception(f'Ještě není plně implementováno')


    def remove_item(self, item_name:str) -> IItem:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru.
        Vrátí odkaz na zadaný objekt nebo None.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IBag(IItemContainer, Protocol):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    def __init__(self, initial_item_names:tuple[str]):
        """Definuje batoh jako kontejner h-objektů s omezenou kapacitou.
        """
        raise Exception(f'Ještě není plně implementováno')


    def initialize(self) -> None:
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IPlace(INamed, IItemContainer, Protocol):
    """Instance představují prostory, mezi nimiž hráč přechází.
    Prostory jsou definovány jako pojmenované kontejnery objektů.
    Prostory mohou obsahovat různé objekty,
    které mohou hráči pomoci v dosažení cíle hry.
    Každý prostor zná své aktuální bezprostřední sousedy
    a ví, jaké objekty se v něm v daném okamžiku nacházejí.
    Sousedé daného prostoru i v něm se nacházející objekty
    se mohou v průběhu hry měnit.
    """

    def __init__(self, name:str, description:str,
                 initial_neighbor_names:tuple[str],
                 initial_item_names    :tuple[str]
        ):
        raise Exception(f'Ještě není plně implementováno')


    def initialize(self) -> None:
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def description(self) -> str:
        """Vrátí stručný popis daného prostoru.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def neighbors(self) -> tuple['IPlace']:
        """Vrátí n-tici aktuálních sousedů daného prostoru,
        tj. prostorů, do nichž je možno se z tohoto prostoru přesunout
        příkazem typu `TypeOfStep.GOTO`.
        """
        raise Exception(f'Ještě není plně implementováno')


    def name_2_neighbor(self, name: str) -> 'IPlace':
        """Vrátí odkaz na souseda se zadaným názvem.
        Není-li takový, vrátí `None`.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IWorld(Protocol):
    """Instance vystupuje v roli správce světa hry a jeho prostorů.
    Má na starosti vzájemné propojení jednotlivých prostorů
    a udržuje informaci o tom, ve kterém z nich se hráč právě nachází.
    Vzájemné uspořádání prostorů se může v průběhu hry měnit –
    prostory mohou v průběhu hry získávat a ztrácet sousedy.
    Ve hře musí být tento objekt definován jako jedináček,
    což lze snadno dosáhnout definujeme-li jej jako modul.
    """

    def initialize(self) -> None:
        """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
        propojení jednotlivých prostorů a jejich výchozí obsah,
        nastaví výchozí aktuální prostor a inicializuje batoh.
        """
        raise Exception(f'Ještě není plně implementováno')


    def current_place(self) -> IPlace:
        """Vrátí odkaz na aktuální prostor,
        tj. na prostor, v němž se hráč pravé nachází.
        """
        raise Exception(f'Ještě není plně implementováno')


    def places(self) -> tuple[IPlace]:
        """Vrátí n-tici odkazů na všechny prostory ve hře
        včetně těch aktuálně nedosažitelných či neaktivních.
        """
        raise Exception(f'Ještě není plně implementováno')


    def place(self, name:str) -> IPlace:
        """Vrátí prostor se zadaným názvem.
        Pokud ve hře takový není, vrátí None.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IActionManager(Protocol):
    """Reprezentuje správce akcí, který řídí celkové chování
    v závislosti na tom, je-li hra právě aktivní a rozhoduje,
    která akce dostane na starost zpracování aktuálního příkazu.
    Správce akcí bývá definován jako modul definující třídy akcí.
    """

    def execute_command(self, command:str) -> str:
        """Zpracuje zadaný příkaz a vrátí odpověď hry.
        Zadaný příkaz zanalyzuje a v závislosti na aktuální aktivitě hry
        rozhodne, která akce dostane na starost jeho zpracování.
        Vrátí odpověď hry na zadaný příkaz.
       """
        raise Exception(f'Ještě není plně implementováno')


    def is_alive(self) -> bool:
        """Vrátí informaci o tom, je-li hra živá = aktuálně spuštěná.
        Spuštěnou hru není možno pustit znovu.
        Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
        """
        raise Exception(f'Ještě není plně implementováno')


    def conditions(self) -> dict[str, object]:
        """Vrátí slovník s aktuálním nastavením příznaků.
        """
        raise Exception(f'Ještě není plně implementováno')


    def tests(self) -> dict[str, object]:
        """Vrátí slovník jehož hodnotami jsou testovací funkce
        ověřující platnost vstupních podmínek pomocných akcí.
        """
        raise Exception(f'Ještě není plně implementováno')


    def _initialize(self):
        """V rámci startu hry inicializuje všechny potřebné objekty.
        """
        raise Exception(f'Ještě není plně implementováno')



############################################################################

@runtime_checkable
class IAction(INamed, Protocol):
    """Společná rodičovská třída všech akcí.
    """

    def __init__(self, name:str, description:str,
                       execute:Callable[[list[str]], str]):
        """Vytvoří instanci, která si zapamatuje
        název dané akce a její popis.
        """
        raise Exception(f'Ještě není plně implementováno')


    @property
    def description(self) -> str:
        """Vrátí popis příkazu s vysvětlením jeho funkce,
        významu jednotlivých parametrů a možností (resp. účelu) použití
        daného příkazu. Tento popis tak může sloužit jako nápověda
        k použití daného příkazu.
        """
        raise Exception(f'Ještě není plně implementováno')


    execute:Callable[[list[str]], str] = None
    """Metoda realizující reakci hry na zadání daného příkazu.
    Předávané pole je vždy neprázdné, protože jeho nultý prvek
    je zadaný název vyvolaného příkazu. Počet argumentů je závislý
    na konkrétním akci, ale pro každou akci je konstantní.
    """



############################################################################

@runtime_checkable
class IGame(Protocol):
    """Instance má na starosti řízení hry a komunikaci s uživatelem.
    Je schopna akceptovat zadávané příkazy a poskytovat informace
    o průběžném stavu hry a jejích součástí.
    Hra musí být definována jako jedináček (singleton),
    a bývá proto definována jako modul.
    """

    def is_alive(self) -> bool:
        """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
        Spuštěnou hru není možno pustit znovu.
        Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
        """
        raise Exception(f'Ještě není plně implementováno')


    def execute_command(self, command:str) -> str:
        """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
        """
        raise Exception(f'Ještě není plně implementováno')


    def stop(self) -> None:
        """Ukončí hru a uvolní alokované prostředky.
        Zadáním prázdného příkazu lze následně spustit hru znovu.
        """
        raise Exception(f'Ještě není plně implementováno')


    def basic_actions(self) -> BasicActions:
        """Vrátí přepravku s názvy povinných akcí.
        """
        raise Exception(f'Ještě není plně implementováno')


    def all_actions(self) -> tuple[IAction]:
        """Vrátí n-tici všech akcí použitelných ve hře.
        """
        raise Exception(f'Ještě není plně implementováno')


    def conditions(self) -> dict[str, object]:
        """Vrátí slovník s aktuálním nastavením příznaků.
        """
        raise Exception(f'Ještě není plně implementováno')


    def tests(self) -> dict[str, object]:
        """Vrátí slovník jehož hodnotami jsou testovací funkce
        ověřující platnost vstupních podmínek pomocných akcí.
        """
        raise Exception(f'Ještě není plně implementováno')


    def bag(self) -> IBag:
        """Vrátí odkaz na batoh, do nějž bude hráč ukládat sebrané objekty.
        """
        raise Exception(f'Ještě není plně implementováno')


    def world(self) -> IWorld:
        """Vrátí odkaz na svět hry.
        """
        raise Exception(f'Ještě není plně implementováno')



###########################################################################q

@runtime_checkable
class IAuthor(Protocol):
    """Protokol `IAuthor` deklaruje požadované vlastnosti objektů,
    které na požádání dodají ID a jméno autora/autorky programu.
    Protože tento protokol má být importován odevzdaným modulem/balíčkem,
    nejsou funkce deklarovány jako instanční metody s parametrem self,
    ale jako datové atributy daného modulu anebo initoru balíčku.
    """

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

    # Čas začátku kroužku, který navštěvujete, zadaný ve formátu
    # d_HHMM, kde d je pořadí dne v týdnu - např. hodnota '1_0730'
    # označuje začátek v pondělí v 07:30
    GROUP_TIME = '3_0000'



###########################################################################q

@runtime_checkable
class IPortal(IAuthor, Protocol):

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
# MODIFIED      Test aplikace s nadstavbovými úpravami
# EXTENDED      Test upravené aplikace s dalším scénářem

def self_test():
    """Otestuje, zda stav projektu odpovídá zadané hladině rozpracovanosti.
    """
    from game23s.tests import Level
    LEVEL = Level.HAPPY         # Nastavení hladiny rozpracovanosti aplikace
    
    from importlib import import_module
    me = import_module(__package__)   # Importuje modul svého balíčku
    from game23s.tests import test
    test(me, LEVEL)         # Testuje implementaci na nastavené hladině



# Test spustíte nastavením požadované hladiny a zadáním příkazů:
# import game23s.název_vašeho_balíčku as at; at.self_test()



###########################################################################q
dbg.stop_mod(2, __name__)
