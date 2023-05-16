# Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul obsahující svět hry a příslušené třídy.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

CAR_NAME: str = 'auto'
CROSSROADS_NAME: str = 'křižovatka'
JUNKYARD_NAME: str = 'smetiště'
TUNNEL_NAME: str = 'tunel'
GAS_STATION_NAME: str = 'benzínka'
CANAL_NAME: str = 'kanál'
BRIDGE_NAME: str = 'most'
CAR_REPAIR_SHOP_NAME: str = 'autoopravna'
BALCONY_NAME: str = 'balkon'

MAX_CAPACITY: int = 10


class ANamed:
    """Instance představují objekty v prostorech či batohu.
    """

    def __init__(self, name: str, **args):
        """Inicializuje objekt zadaným názvem.
        """
        self._name = name
        super().__init__(**args)

    @property
    def name(self) -> str:
        """Vrátí název daného objektu.
        """
        return self._name

    def __str__(self) -> str:
        """Vrátí uživatelský textový podpis jako název dané instance.
        """
        return self.name


############################################################################

class Item(ANamed):
    """Instance představují h-objekty v prostorech či batohu.
    """

    def __init__(self,
                 name: str,
                 movable: bool,
                 usable_in: str | None,
                 weight: int,
                 **args):
        """Vytvoří h-objekt se zadaným názvem.
        """
        self._movable = movable
        self._usable_in = usable_in
        self._weight = weight
        super().__init__(name=name, **args)

    @property
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """
        return self._weight

    @property
    def movable(self) -> bool:
        """Vrátí informaci o tom, je-li objekt přenositelný.
        """
        return self._movable

    @property
    def usable_in(self) -> str | None:
        """Vrátí název prostoru, v němž je možno daný objekt použít,
        nebo None, není-li možno daný objekt nikde použít.
        """
        return self._usable_in

    def __repr__(self):
        """Vrátí textový podpis dané instance.
        """
        return f"{self.__class__.__name__}({self.name})"


############################################################################

class AItemContainer:
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names: tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """
        self.initial_item_names = initial_item_names
        super().__init__(**args)
        self._items = []
        self._item_names = []

    def initialize(self) -> None:
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        from . import actions
        for item_name in self.initial_item_names:
            item = Item(
                name=item_name,
                movable=item_name in items_weights,
                usable_in=(actions.get_usable_in_dict().get(item_name, None)),
                weight=items_weights.get(item_name, 0),
            )
            self._items.append(item)
            self._item_names.append(item_name.lower())

    @property
    def items(self) -> list[Item]:
        """Vrátí n-tici objektů v daném kontejneru.
        """
        return self._items[:]

    def item(self, name: str) -> Item | None:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """
        name_lower = name.lower()
        if name_lower in self._item_names:
            return self._items[self._item_names.index(name_lower)]
        return None

    def add_item(self, item: Item) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        self._items.append(item)
        self._item_names.append(item.name.lower())
        return True

    def remove_item(self, item_name: str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru.
        Vrátí odkaz na zadaný objekt nebo None.
        """
        item = self.item(item_name)
        if item:
            self._items.remove(item)
            self._item_names.remove(item.name.lower())
        return item


############################################################################

class Bag(AItemContainer):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    def __init__(self, initial_item_names: tuple[str] | tuple, **kwargs):
        """Definuje batoh jako kontejner h-objektů s omezenou kapacitou.
        """
        global BAG
        if BAG:
            raise Exception(f'Více než jeden batoh')
        self._capacity = 0
        super().__init__(initial_item_names, **kwargs)
        BAG = self

    def initialize(self) -> None:
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """
        self.clear()
        super().initialize()

    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """
        return self._capacity

    def add_item(self, item: Item) -> bool:
        """Přidá zadaný objekt do batohu a vrátí informaci o tom,
        jestli se to podařilo.
        """
        if item.weight + self._capacity <= MAX_CAPACITY:
            self._capacity += item.weight
            return super().add_item(item)
        return False

    def remove_item(self, item_name: str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z batohu.
        Vrátí odkaz na zadaný objekt nebo None.
        """
        item = super().remove_item(item_name)
        if item:
            self._capacity -= item.weight
        return item

    def clear(self) -> None:
        """Vyprázdní batoh a nastaví jeho kapacitu na nulu."""
        self._capacity = 0
        self._items = []
        self._item_names = []

    def __repr__(self):
        """Vrátí textový podpis dané instance.
        """
        return f"{self.__class__.__name__}({self.items})"


############################################################################

class Place(ANamed, AItemContainer):
    """Instance představují prostory, mezi nimiž hráč přechází.
    Prostory jsou definovány jako pojmenované kontejnery objektů.
    Prostory mohou obsahovat různé objekty,
    které mohou hráči pomoci v dosažení cíle hry.
    Každý prostor zná své aktuální bezprostřední sousedy
    a ví, jaké objekty se v něm v daném okamžiku nacházejí.
    Sousedé daného prostoru i v něm se nacházející objekty
    se mohou v průběhu hry měnit.
    """

    def __init__(self, name: str, description: str,
                 initial_neighbor_names: tuple[str, ...],
                 initial_item_names: tuple[str, ...] | tuple,
                 secret_item_names: tuple[str, ...] | None = None,
                 ):
        """Vytvoří nový prostor se zadaným názvem a popisem.
        Počáteční sousedy a objekty v prostoru jsou zadány
        jako n-tice jejich názvů.
        """
        super().__init__(name=name, initial_item_names=initial_item_names)
        self._description = description
        self._initial_neighbor_names = initial_neighbor_names
        self._neighbors = {}
        self._secret_item_names = secret_item_names

    def initialize(self) -> None:
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """
        for name in self._initial_neighbor_names:
            self._neighbors[name] = _all_places[name]

        super().initialize()

    @property
    def description(self) -> str:
        """Vrátí stručný popis daného prostoru.
        """
        return self._description

    @property
    def neighbors(self) -> tuple['Place'] | tuple:
        """Vrátí n-tici aktuálních sousedů daného prostoru,
        tj. prostorů, do nichž je možno se z tohoto prostoru přesunout
        příkazem typu `TypeOfStep.GOTO`.
        """
        return tuple(self._neighbors.values())

    @property
    def secret_items(self) -> tuple[str] | None:
        """Vrátí n-tici tajných objektů v prostoru.
        """
        if self._secret_item_names is None:
            return None
        return tuple(self._secret_item_names)

    def clear_secret_items(self) -> None:
        """Vyprázdní seznam tajných objektů v prostoru.
        """
        self._secret_item_names = tuple()

    def name_2_neighbor(self, name: str) -> 'Place':
        """Vrátí odkaz na souseda se zadaným názvem.
        Není-li takový, vrátí `None`.
        """
        return self._neighbors.get(name.lower())

    def add_neighbor(self, pl: 'Place') -> None:
        """Přidá zadaný prostor mezi sousedy.
        """
        self._neighbors[pl.name] = pl

    def __repr__(self):
        """Vrátí textový podpis dané instance.
        """
        class_name = self.__class__.__name__
        return f"{class_name}({self.name}, {self.items})"


############################################################################


def initialize() -> None:
    """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
        propojení jednotlivých prostorů a jejich výchozí obsah,
        nastaví výchozí aktuální prostor a inicializuje batoh.
        """
    from .patm03_scenarios import place_details
    global _current_place, _all_places
    auto = Place(
        name=CAR_NAME,
        description=place_details[CAR_NAME],
        initial_neighbor_names=(CROSSROADS_NAME,),
        initial_item_names=('žebřík',),
    )
    _all_places[CAR_NAME] = auto
    _all_places[CROSSROADS_NAME] = Place(
        name=CROSSROADS_NAME,
        description=place_details[CROSSROADS_NAME],
        initial_neighbor_names=(JUNKYARD_NAME, CAR_NAME),
        initial_item_names=('rozbité_auto',)
    )
    _all_places[JUNKYARD_NAME] = Place(
        name=JUNKYARD_NAME,
        description=place_details[JUNKYARD_NAME],
        initial_neighbor_names=(CROSSROADS_NAME,),
        initial_item_names=(),
        secret_item_names=secret_items[JUNKYARD_NAME],
    )
    _all_places[TUNNEL_NAME] = Place(
        name=TUNNEL_NAME,
        description=place_details[TUNNEL_NAME],
        initial_neighbor_names=(CROSSROADS_NAME, GAS_STATION_NAME),
        initial_item_names=(),
        secret_item_names=secret_items[TUNNEL_NAME],
    )
    _all_places[GAS_STATION_NAME] = Place(
        name=GAS_STATION_NAME,
        description=place_details[GAS_STATION_NAME],
        initial_neighbor_names=(TUNNEL_NAME, BRIDGE_NAME, CANAL_NAME),
        initial_item_names=('nádrž',),
    )
    _all_places[CANAL_NAME] = Place(
        name=CANAL_NAME,
        description=place_details[CANAL_NAME],
        initial_neighbor_names=(),
        initial_item_names=('hák',),
    )
    _all_places[BRIDGE_NAME] = Place(
        name=BRIDGE_NAME,
        description=place_details[BRIDGE_NAME],
        initial_neighbor_names=('benzínka',),
        initial_item_names=(),
    )
    _all_places[CAR_REPAIR_SHOP_NAME] = Place(
        name=CAR_REPAIR_SHOP_NAME,
        description=place_details[CAR_REPAIR_SHOP_NAME],
        initial_neighbor_names=(BRIDGE_NAME,),
        initial_item_names=('raketomet',),
    )
    _all_places[BALCONY_NAME] = Place(
        name=BALCONY_NAME,
        description=place_details[BALCONY_NAME],
        initial_neighbor_names=(CAR_REPAIR_SHOP_NAME, CROSSROADS_NAME),
        initial_item_names=('kanystr',),
    )

    for pl in _all_places.values():
        pl.initialize()

    _current_place = auto
    BAG.initialize()


def set_current_place(pl: Place) -> None:
    """Nastaví aktuální prostor.
        """
    global _current_place
    _current_place = pl


def current_place() -> Place:
    """Vrátí odkaz na aktuální prostor,
        tj. na prostor, v němž se hráč pravé nachází.
        """
    return _current_place


def places() -> tuple[Place]:
    """Vrátí n-tici odkazů na všechny prostory ve hře
        včetně těch aktuálně nedosažitelných či neaktivních.
        """
    return tuple(_all_places.values())


def place(name: str) -> Place | None:
    """Vrátí prostor se zadaným názvem.
        Pokud ve hře takový není, vrátí None.
        """
    if name not in _all_places:
        return None
    return _all_places[name]


###########################################################################q

BAG: Bag | None = None
BAG = Bag(())
_current_place: Place | None = None
_all_places: dict[str, Place] = {}

items_weights: dict[str, int] = {
    'žebřík': 10,
    'páčidlo': 1,
    'lano': 5,
    'raketa': 4,
    'hák': 1,
    'raketomet': 6,
    'nabitý_raketomet': 10,
    'kanystr': 10,
    'lano_s_hákem': 6,
}

secret_items: dict[str, tuple[str, ...]] = {
    JUNKYARD_NAME: ('páčidlo', 'lano'),
    TUNNEL_NAME: ('raketa',),
}

###########################################################################q
dbg.stop_mod(1, __name__)
