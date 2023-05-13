#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/tests/test_game.py
"""
Modul s testy rozhraní, scénářů a běhu hry.
"""
import dbg
dbg.start_mod(2, __name__)
############################################################################

from ..api              import BasicActions, scen_types, state_of
from ..api.interfaces   import IPortal, IGame
from ..api.scenario     import ScenarioStep, Scenario
from ..api.scen_types   import TypeOfStep, tsSUCCESS
from .common.texts      import HASH_N, AFTER_N, N_AFTER_N
from .common.errors     import error
from .visitor           import Visitor
from .                  import Level, Verbosity, prVb, test_scenario



# ############################################################################
#
# # Nastavení, zda se budou vypisovat stavy hry po provedení jednotlivých akcí
# Scenario.print_state = True
#
#
#
############################################################################

# @dbg.prSEd()
def test_game_from(portal:IPortal, level:Level,
                   visitor_class:type=Visitor) -> str:
    """
    Test aplikace se zadaným portálem podle scénářů
    definovaných zadanou hladinou rozpracovanosti.

    :param portal:  Portál zprostředkující komunikaci s testovanou aplikací
    :param level:   Testovaná hladina rozpracovanosti aplikace
    :param visitor_class: Třída návštěvníka, který ví,
                    jak testovat útroby a chování hry
    :return: Metoda nic nevrací
    """
    global LEVEL
    LEVEL = level
    visitor = visitor_class(portal, level)  # Vytvoření návštěvníka
    n2s = portal.NAME_2_SCENARIO            # Získání slovníku scénářů
    if not isinstance(n2s, dict):   # Není-li obdržená instance slovník,
        n2s = n2s()                 # bude to funkce vracející slovník
    global GAME
    GAME = portal.GAME()
    
    # Vytvoříme n-tici scénářů, podle nichž se daná hladina testuje
    scen_list = []
    for scen_name in LEVEL_2_SCENARIOS[level]:
        scenario = n2s[scen_name]
        scen_list.append(scenario)
    scenarios = tuple(scen_list)
    prVb(Verbosity.DETAILS, f'\nSCENARIOS: {scenarios}\n')
    NL = '\n'
    result = f'{AFTER_N}{AFTER_N}'\
              'Testy hry podle jednotlivých scénářů skončily následovně:\n'
    for s in scenarios:
        prVb(Verbosity.DETAILS,
             f'\n{2*(75*"T"+NL)}Test hry dle scénáře: {s.name}')
        msg = 'OK' if _test_by(s, visitor) else 'ŠPATNĚ'
        result += f'{s.name}: {msg}\n'
        prVb(Verbosity.STEPS,
             f'{2*(75*"A"+NL)}Konec testu dle scénáře: {s.name}\n')
    result += HASH_N
    prVb(Verbosity.SUMMARY, result)



############################################################################
_from_scenario:list[str] = None
_from_game    :list[str]  = None

# @dbg.prSEda()
def _test_by(scenario:Scenario, visitor:Visitor) -> bool:
    """
    Otestuje zadanou hru podle zadaného scénáře
    za pomoci zadaného návštěvníka.
    
    :param scenario:
    :param visitor:
    :return:
    """

    _error = lambda reason, step, expected, obtained: \
             error(reason, scenario, step, GAME, expected, obtained)

    # TODO Porovnat sloučení s containers_differs v modulu utils
    # @dbg.prSEdr(msg='from tests.test_game._test_by')
    def containers_differs(scen_cont:tuple[str],
                           game_cont:tuple['INamed']) -> bool:
        """Porovná názvy v kontejneru scen_cont s názvy objektů
        v kontejneru game_cont bez ohledu na velikost písmen
        a vrátí informaci o tom, zda se liší (liší se = True).
        """
        if not ('__iter__' in dir(game_cont)):
            _error('objekt hry není kontejner', step, scen_cont, game_cont)
        global _from_scenario, _from_game
        _from_scenario = sorted([item     .lower() for item in scen_cont])
        _from_game     = sorted([item.name.lower() for item in game_cont])
        result = (_from_scenario != _from_game)
        return result

    # Zde začíná vlastní tělo funkce ======================================
    step:ScenarioStep
    if LEVEL >= Level.RUNNING:
        if containers_differs(test_scenario.ALL_ACTIONS, GAME.all_actions()):
            msg = f'\nSeznamy definovaných akcí nesouhlasí\n' \
                  f'   Scénáře: {_from_scenario}\n' \
                  f'   Hra:     {_from_game}'
            raise Exception(msg)
    visitor.before_game_start(scenario)
    source = (scenario.steps if LEVEL > Level.WORLD
                           else (scenario.steps[0], ))
    for step in source:
        prVb(Verbosity.STEPS,
             f'{step.index}. {(command:=step.command)}\n{30*"-"}')
        try:
            visitor.before_entering_command(step)
            if (step.typeOfStep.name.startswith('tsNS_')
               or  (step.typeOfStep == tsSUCCESS)
            ):
                _test_needs(step)
            answer = GAME.execute_command(command)
            prVb(Verbosity.STEPS,     f'{answer}')
            prVb(Verbosity.STEP_ATTR, f'{30*"-"}\n{state_of(GAME)}')
            prVb(Verbosity.STEPS,     f'{30*"="}\n')
        except Exception as ex:
            print(f'Při vykonávání příkazu '
                  f'{step.index}. {(command:=step.command)}\n'
                  f'byla vyhozena výjimka {ex}')
            raise ex

        if step.typeOfStep == scen_types.tsSTART:
            visitor.after_game_start(scenario)
        visitor.before_step_test(step, answer)
        if (not answer or
            step.message.lower() != answer[:len(step.message)].lower()
        ):
            _error('odpověď hry', step, step.message, answer)
        if step.typeOfStep == scen_types.tsNOT_START:
            continue
        current_place = GAME.world().current_place()
        if step.place != current_place.name:
            _error('aktuální prostor', step, step.place, current_place)
        if containers_differs(step.neighbors, current_place.neighbors):
            _error('aktuální sousedé', step, _from_scenario, _from_game)
        if containers_differs(step.items, current_place.items):
            _error('objekty v aktuálním prostoru', step, _from_scenario,
                                                         _from_game)
        if containers_differs(step.bag, GAME.bag().items):
            _error('objekty v batohu', step, _from_scenario, _from_game)
        if step.typeOfStep.name.startswith('tsNS´_'):
            _test_sets() # Řádná nestandardní akce
        else:
            _test_nothing_set()
        visitor.after_step_test(step, answer)
    visitor.after_game_end()
    if LEVEL <= Level.WORLD:   GAME.stop()
    if GAME.is_alive():
        _error('Po ukončení scénáře není hra ukončena', step, (), ())
    return True

    
def _test_needs(step:ScenarioStep):
    """
    Prověří, zda jsou nastaveny příznaky požadované pro zadaný
    testovaný krok aktivující nestandardní akci.
    
    :param step: Zadaný testovaný krok scénáře
    :return: Nic nebo vyhození výjimky
    """


def _test_sets(step:ScenarioStep):
    """
    Prověří, zda nestandardní akce prověřovaná v zadaném testovacím kroku
    nastavuje požadované příznaky.
    
    :param step: Zadaný testovaný krok scénáře
    :return: Nic nebo vyhození výjimky
    """


def _test_nothing_set():
    """
    Prověří, že v aktuálně testovaném kroku nebyl změněn žádný
    z příznaků požadovaný pro aktivovatelnost nestandardních akcí.
    
    :param step: Zadaný testovaný krok scénáře
    :return: Nic nebo vyhození výjimky
    """


def _verify_is_alive(step:ScenarioStep, the_last:bool):
    """Prověří, jestli testovaná hra správně hlásí svoji spuštěnost
    (před startem a po skončení ne, jinak ano).
    """
    game_is_alive = GAME.is_alive()
    if (step.typeOfStep == scen_types.tsNOT_START)  or  the_last:
        if game_is_alive:
            prefix = ("Po ukončení hry" if the_last
                else  "Před startem hry ")
            raise Exception(prefix + " hra hlásí, že je spuštěná,"
                                   + " přestože má být vypnutá")
    else:
        if not game_is_alive:
            raise Exception("Hra tvrdí, že je vypnutá přestože má běžet")



############################################################################
# Následující proměnné jsou zavedeny pro zpřehlednění n-tice názvů
# scénářů postupně používaných při testování na jednotlivých hladinách
HAPPY_   = scen_types.HAPPY_NAME
BASIC_   = scen_types.BASIC_NAME
MISTAKE_ = scen_types.MISTAKE_NAME
MIST_NS_ = scen_types.MISTAKE_NS_NAME
FOURTH_  = 'FOURTH' # Přidaný scénář pro modifikace s přidanou akcí
FIFTH_   = 'FIFTH'  # Druhý přidaný scénář pro modifikace s přidanou akcí


# Testovací posloupnosti scénářů pro jednotlivé hladiny testování
LEVEL_2_SCENARIOS = {
    Level.START     : (BASIC_, ),
    Level.WORLD     : (BASIC_, ),
    Level.BASIC     : (BASIC_, BASIC_, ),
    Level.MISTAKES  : (BASIC_, BASIC_, MISTAKE_, ),
    Level.RUNNING   : (HAPPY_, HAPPY_, ),
    Level.WHOLE     : (HAPPY_, HAPPY_, MISTAKE_, MIST_NS_, ),
    Level.MODIFIED  : (HAPPY_, HAPPY_, MISTAKE_, MIST_NS_, ),
    Level.EXTENDED  : (HAPPY_, HAPPY_, MISTAKE_, MIST_NS_, FOURTH_, ),
    # Level.EXTENDED2 : (HAPPY_, HAPPY_, MISTAKE_, MIST_NS_, FOURTH_, FIFTH_),
}


###########################################################################q
dbg.stop_mod(2, __name__)
