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
from ..api.scen_types   import TypeOfStep, tsSUCCESS, SubtypeOfStep as STS
from .common.texts      import HASH_N, AFTER_N, N_AFTER_N
from .common.errors     import error
from .common.utils      import containers_differs
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
    n2s = portal.NAME_2_SCENARIO()            # Získání slovníku scénářů

    global VISITOR;     VISITOR = visitor_class(portal, level)
    global LEVEL;       LEVEL   = level
    global HAPPY;       HAPPY   = n2s[HAPPY_]
    global GAME;        GAME    = portal.GAME()

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
        msg = 'OK' if _test_by(s) else 'ŠPATNĚ'
        result += f'{s.name}: {msg}\n'
        prVb(Verbosity.STEPS,
             f'{2*(75*"A"+NL)}Konec testu dle scénáře: {s.name}\n')
    result += HASH_N
    prVb(Verbosity.SUMMARY, result)



############################################################################
_from_scenario:list[str] = None
_from_game    :list[str]  = None


def _test_by(scenario:Scenario) -> bool:
    """
    Otestuje zadanou hru podle zadaného scénáře
    za pomoci zadaného návštěvníka.
    
    :param scenario:
    :return:
    """
    global SCENARIO;    SCENARIO = scenario
    global STEP;        STEP     = None
    
    if LEVEL >= Level.RUNNING:
        if containers_differs(test_scenario.ALL_ACTIONS, GAME.all_actions()):
            msg = f'\nSeznamy definovaných akcí nesouhlasí\n' \
                  f'   Scénáře: {containers_differs.from_scenario}\n' \
                  f'   Hra:     {containers_differs.from_game}'
            raise Exception(msg)
    VISITOR.before_game_start(scenario)
    source = (scenario.steps if LEVEL > Level.WORLD
                           else (scenario.steps[0], ))
    for STEP in source:
        prVb(Verbosity.STEPS,
             f'{STEP.index}. {(command:=STEP.command)}\n{30*"-"}')
        _verify_before_step()
        try:
            VISITOR.before_entering_command(STEP)
            answer = GAME.execute_command(command)
            prVb(Verbosity.STEPS,     f'{answer}')
            prVb(Verbosity.STEP_ATTR, f'{30*"-"}\n{state_of(GAME)}')
            prVb(Verbosity.STEPS,     f'{30*"="}\n')
        except Exception as ex:
            print(f'Při vykonávání příkazu '
                  f'{STEP.index}. {(command:=STEP.command)}\n'
                  f'byla vyhozena výjimka {ex}')
            raise ex
        _verify_after_step(answer)

    VISITOR.after_game_end()
    if LEVEL <= Level.WORLD:   GAME.stop()
    if GAME.is_alive():
        _ERR('Po ukončení scénáře není hra ukončena', (), ())
    return True


def _verify_before_step():
    """
    Prověří stav hry před provedením následujícího pomocného kroku,
    jmenovitě platnost podmínek a nastavení příznaků.
    """
    subtype   = STEP.typeOfStep.subtype
    arguments = STEP.command.split()
    match subtype:
        case STS.NONSTANDARD  |  STS.SUCCESS:
            for flag in STEP.needs:
                expected = STEP.needs[flag]
                obtained = GAME.conditions()[flag]
                if expected != obtained:
                    _ERR(f'Neodpovídá hodnota příznaku {flag}',
                         expected, obtained)
            for test in STEP.tests:
                if not (tst := GAME.tests()[test](arguments)):
                    _ERR(f'Neodpovídá hodnota testu {test}()', True, tst)
        case STS.MISTAKE_NS:
            for key in STEP.needs:
                wrong    = STEP.needs[key]
                obtained = GAME.conditions()[key]
                if wrong == obtained:
                    _ERR(f'Hodnota příznaku {key} odpovídá',
                         f'Nemá být {wrong}', obtained)
            for test in STEP.tests:
                if (tst := GAME.tests()[test](arguments)):
                    _ERR(f'Test {test}() neměl projít', False, tst)
    # Prověřeno


def _verify_after_step(answer:str):
    """
    Prověří stav hry po provedení posledního kroku
    a jeho shodu se stavem požadovaným ve scénáři.
    """
    if STEP.typeOfStep == scen_types.tsSTART:
        _verify_set()
        VISITOR.after_game_start(SCENARIO)
    VISITOR.before_step_test(STEP, answer)
    if (not answer or
            STEP.message.lower() != answer[:len(STEP.message)].lower()
    ):
        _ERR('odpověď hry', STEP.message, answer)
    if STEP.typeOfStep == scen_types.tsNOT_START:
        return      # U tohoto typu kroku není co dál prověřovat ==========>
    current_place = GAME.world().current_place()
    if STEP.place != current_place.name:
        _ERR('aktuální prostor', STEP.place, current_place)
    cd = containers_differs
    if containers_differs(STEP.neighbors, current_place.neighbors):
        _ERR('aktuální sousedé', cd.from_scenario, cd.from_game)
    if containers_differs(STEP.items, current_place.items):
        _ERR('objekty v aktuálním prostoru',
             cd.from_scenario, cd.from_game)
    if containers_differs(STEP.bag, GAME.bag().items):
        _ERR('objekty v batohu', cd.from_scenario, cd.from_game)
    if STEP.typeOfStep.subtype == STS.NONSTANDARD:
        _verify_set()  # Řádná pomocná akce
    else:
        _verify_nothing_set()
    VISITOR.after_step_test(STEP, answer)


# @dbg.prSEda()
def _verify_set():
    """
    Prověří, že příznaky mají hodnoty požadované startovním krokem.
    """
    expected = STEP.sets
    obtained = GAME.conditions()
    for key in expected:
        if ((key not in obtained)
        or  (expected[key] != obtained[key])
        ):
            _ERR('Nastavené příznaky neodpovídají požadavkům',
                 expected, obtained)


def _verify_nothing_set():
    """
    PROZATÍM SE NEPROVĚŘUJE.
    Prověří, že v aktuálně testovaném kroku nebyl změněn žádný
    z příznaků požadovaný pro aktivovatelnost pomocných akcí.
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
# Globální proměnné nastavované na počátku testu
VISITOR:Visitor     = None
LEVEL:Level         = None
HAPPY:Scenario      = None
GAME :IGame         = None
SCENARIO:Scenario   = None
STEP:ScenarioStep   = None

_ERR = lambda reason, expected, obtained: \
              error(reason, SCENARIO, STEP, GAME, expected, obtained)


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
