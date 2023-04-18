#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_ILS/game23s/api/__init__.py
"""
Balíček definující společné API všech her.¤
Obsahuje moduly definující společně používané objekty
a vedle nich i moduly definující protokoly .

Moduly:
    __init__    - Initor balíčku deklaruje povinné atributy initorů balíčků
                  odevzdaných semestrálních prací
    game_types  - Protokoly deklarující povinné atributy objektů hry
    scen_types  - Typy scénářů a jejich kroků
    scenarios   - Třídy kroků scénáře a scénářů
    gui         - Grafické uživatelské rozhraní pro hry dodržující api

"""
import dbg; dbg.start_pkg(1, __name__, __doc__)
############################################################################

def version(): return '23s.03.9274_2023-03-13'

from collections import namedtuple

BasicActions = namedtuple('BasicActions',
    'MOVE_NAME PUT_DOWN_NAME TAKE_NAME HELP_NAME END_NAME SUCCESS_NAME')
BasicActions.__doc__ = """Přepravka s názvy povinných akcí."""

# @dbg.prSEd()
def BA_eq(self, other) -> bool:
    """Porovná atributy argumentů bez ohledu na velikost písmen."""
    if not isinstance(other, BasicActions):  return False
    return((self.MOVE_NAME    .lower() == other.MOVE_NAME    .lower())  and
           (self.PUT_DOWN_NAME.lower() == other.PUT_DOWN_NAME.lower())  and
           (self.TAKE_NAME    .lower() == other.TAKE_NAME    .lower())  and
           (self.HELP_NAME    .lower() == other.HELP_NAME    .lower())  and
           (self.END_NAME     .lower() == other.END_NAME     .lower())  and
           (self.SUCCESS_NAME .lower() == other.SUCCESS_NAME .lower())  )
# BasicActions.__eq__ = __eq__;
# del __eq__



############################################################################

# Modul interfaces musí být importován až po definici modulu BasicActions,
# Protože v modulu Interfaces je modul BasicActions používán
from .interfaces import IGame

def state_of(game:IGame) -> str:
    """Vrátí string s popisem aktuálního stavu, tj. s názvem
    aktuálního prostoru, jeho sousedů a h-objektů a obsahu batohu.
    """
    cp = game.world().current_place()
    result = (f'Aktuální prostor:    {cp}\n'
              f'Sousedé prostoru:    {list(cp.neighbors)}\n'
              f'Předměty v prostoru: {cp.items}\n'
              f'Předměty v batohu:   {game.world().BAG.items}\n'
              f'Nastavené příznaky:  {game.conditions()}')
    return result



############################################################################
dbg.stop_pkg(1, __name__)
