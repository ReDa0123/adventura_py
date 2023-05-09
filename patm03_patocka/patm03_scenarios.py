# Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Základní čtveřice scénářů pro postapokalyptickou hru.
Kroky jsou doplněny o podmínky k jejich úspěšnému provedení.
"""
import dbg

dbg.start_mod(1, __name__)
###########################################################################q

from game23s.api.scenario import ScenarioStep, Scenario
from game23s.api.scen_types import *  # Především typu kroků

###########################################################################q
ScenarioStep.next_index = 0  # Index prvního kroku za startem

place_details = {
    'křižovatka':
        'křižovatka - poměrně rozlehlé pustá křižovatky.\n Stojí zde '
        'opuštěné auto a uzavčené dveře do tunelu.\n Je odsud vidět i '
        'balkón, ale ten je moc vysoko.',
    'auto':
        'auto - vaše auto bez benzínu, hlídá ho tvůj parťák.',
    'smetiště':
        'smetiště - leží tu hodně harampádí.',
    'tunel':
        'tunel - kontrolní tunel do města.',
    'benzínka':
        'benzínka - opuštěná benzínka u města.',
    'kanál':
        'kanál - odpadní kanál předělaný na skrýš přeživších.',
    'most':
        'most - rozbitý most přes kanál.',
    'autoopravna':
        'autoopravna - autoopravna ve městě města.\n'
        'Leží tu raketomet a jsou tu zavřené dveře na balkon.',
    'balkon':
        'balkon - balkon na druhém patře autoopravy.\n'
        'Leží tu kanystr s benzinem.',
}

goto_first_part = 'Přesunul ses do prostoru:\n'


def get_take_message(name: str, weight: str | int) -> str:
    """Vrátí zprávu o převzetí předmětu do batohu."""
    return f'Dal sis do batohu (váha {str(weight)}kg) {name}'


def get_drop_message(name: str) -> str:
    """Vrátí zprávu o položení předmětu na zem."""
    return f'Položil si na zem z batohu {name}'


HELP = ("Ty a tvůj parťák jedete v autě pustinou v Americe zpustošené"
        " nukleární válkou.\n"
        "Najednou se ale auto zastaví, protože došel benzín.\n"
        "Domluvíte se, že tvůj parťák zůstane v autě a bude ho "
        "hlídat. \n"
        "Ty jsi byl vyslán do pustiny najít kanystr s benzínem.\n"
        "Uneseš maximálně 10 kg.\n"
        "Musíš nejdříve dojít na smetiště, prozkoumat ho a najít \n"
        "páčidlo a lano. Páčidlo použij na křižovatce, abys otevřel \n"
        "dveře do tunelu. Po vstupu do tunelu ho prozkoumej a vezmi \n"
        "nalezenou raketu. Polož všechny věci u benzínky a vrať se \n"
        "k autu pro žebřík. Vezmi ho a jdi do kanálu a použij žebřík, \n"
        "aby ses mohl dostat zpátky. V kanálu vem hák a vrať se na benzínku \n"
        "a seber zahozené věci. Zkombinuj hák a lano a vytvožený předmět \n"
        "použij na mostě. V autoopravně najdeš raketomet a ten zkombinuj \n"
        "s raketou a použij vytvořenou věc k otevření balkonu. \n"
        "Vezmi kanystr s benzínem a vrať se k autu a vyhraj! \n"
        "Příkazy: \njdi - přesun mezi prostory,\n"
        "vezmi - vezme předmět ze země,\n"
        "polož - položí předmět na zem z batohu,\n"
        "? - zobrazí nápovědu,\n"
        "konec - ukončí hru,\n"
        "prozkoumej - najde skryté věci v prostoru,\n"
        "použij - použije předmět z batohu,\n"
        "zkombinuj - zkombinuje předměty z batohu a vytvoří nový,\n"
        "naplň - vyhraje hru, pokud máš benzín u auta\n"
        )

# Základní úspěšný scénář demonstrující průběh hry, při němž hráč
# nezadává žádné chybné příkazy a dosáhne zadaného cíle.
HAPPY = Scenario(stHAPPY, (
    START_STEP :=
    ScenarioStep(tsSTART, '',  # Zadaný příkaz
                 "Vítej!\n" + HELP +
                 "Na začátku máš jen pěsti a otrhané oblečení.\n"
                 "Pokud si nevíš rady, napiš ?, což zobrazí nápovědu.\n",
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 sets={
                     "combinable": (frozenset({"hák", "lano"}),
                                    frozenset({"raketa", "raketomet"}),
                                    ),
                     "usable_in": {
                         "páčidlo": "křižovatka",
                         "žebřík": "kanál",
                         "lano_s_hákem": "most",
                         "nabitý_raketomet": "autoopravna",
                     },
                     "junkyard.searched": False,
                     "tunnel.searched": False,
                     "items.used": 0,
                     "items.created": 0,
                 },
                 tests=[
                     "hidden_items_present",  # Jsou skryté věci v prostoru
                     "first_argument_in_bag",  # 1. argument je v batohu
                     "second_argument_in_bag",  # 2. argument je v batohu
                     "argument_usable",  # Argument je použitelný
                     "argument_usable_in",  # Argument je použitelný v prostoru
                     "arguments_not_same",  # Argumenty nejsou stejné
                     "arguments_combinable",  # Argumenty jsou kombinovatelné
                     "in_car",  # Je v prostoru auto
                     "has_gas",  # Má benzín
                 ]
                 ),
    ScenarioStep(tsTAKE, 'Vezmi žebřík',  # Zadaný příkaz
                 get_take_message('žebřík', 10),
                 place='auto',
                 neighbors=("křižovatka",),
                 items=(),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsGOTO, 'Jdi křižovatka',  # Zadaný příkaz
                 goto_first_part + place_details['křižovatka'],
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto',),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsPUT_DOWN, 'Polož žebřík',  # Zadaný příkaz
                 get_drop_message('žebřík'),
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto', 'žebřík'),
                 bag=(),
                 ),
    ScenarioStep(tsGOTO, 'Jdi smetiště',  # Zadaný příkaz
                 goto_first_part + place_details['smetiště'],
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=(),
                 bag=(),
                 ),
    ScenarioStep(tsNS_0, 'prozkoumej',  # Zadaný příkaz
                 'Našel jsi na zemi páčidlo (váha 1kg), lano (váha 5kg)',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=(),
                 needs={"junkyard.searched": False},
                 tests=["hidden_items_present"],
                 sets={"junkyard.searched": True},
                 ),
    ScenarioStep(tsTAKE, 'Vezmi páčidlo',  # Zadaný příkaz
                 get_take_message('páčidlo', 1),
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('lano',),
                 bag=('páčidlo',),
                 ),
    ScenarioStep(tsTAKE, 'Vezmi lano',  # Zadaný příkaz
                 get_take_message('lano', 5),
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=(),
                 bag=('páčidlo', 'lano'),
                 ),
    ScenarioStep(tsGOTO, 'Jdi křižovatka',  # Zadaný příkaz
                 goto_first_part + place_details['křižovatka'],
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto', 'žebřík'),
                 bag=('páčidlo', 'lano'),
                 ),
    ScenarioStep(tsNS_1, 'Použij páčidlo',  # Zadaný příkaz
                 'Páčidlo se rozpadlo na kousky, ale otevřel si dveře do '
                 'tunelu.\n'
                 'ztratil si páčidlo',
                 place='křižovatka',
                 neighbors=('smetiště', 'auto', 'tunel'),
                 items=('rozbité_auto', 'žebřík'),
                 bag=('lano',),
                 tests=[
                     "first_argument_in_bag",
                     "argument_usable",
                     "argument_usable_in"
                 ],
                 sets={"items.used": 1, },
                 ),
    ScenarioStep(tsGOTO, 'Jdi tunel',  # Zadaný příkaz
                 goto_first_part + place_details['tunel'],
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=(),
                 bag=('lano',),
                 ),
    ScenarioStep(tsNS_0, 'prozkoumej',  # Zadaný příkaz
                 'Našel jsi na zemi raketa (váha 4kg)',
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=('raketa',),
                 bag=('lano',),
                 needs={"tunnel.searched": False},
                 tests=["hidden_items_present"],
                 sets={"tunnel.searched": True},
                 ),
    ScenarioStep(tsTAKE, 'Vezmi raketa',  # Zadaný příkaz
                 get_take_message('raketa', 4),
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=(),
                 bag=('lano', 'raketa'),
                 ),
    ScenarioStep(tsGOTO, 'Jdi benzínka',  # Zadaný příkaz
                 goto_first_part + place_details['benzínka'],
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž',),
                 bag=('lano', 'raketa'),
                 ),
    ScenarioStep(tsPUT_DOWN, 'Polož lano',  # Zadaný příkaz
                 get_drop_message('lano'),
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž', 'lano'),
                 bag=('raketa',),
                 ),
    ScenarioStep(tsPUT_DOWN, 'Polož raketa',  # Zadaný příkaz
                 get_drop_message('raketa'),
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž', 'lano', 'raketa'),
                 bag=(),
                 ),
    ScenarioStep(tsGOTO, 'Jdi tunel',  # Zadaný příkaz
                 goto_first_part + place_details['tunel'],
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=(),
                 bag=(),
                 ),
    ScenarioStep(tsGOTO, 'Jdi křižovatka',  # Zadaný příkaz
                 goto_first_part + place_details['křižovatka'],
                 place='křižovatka',
                 neighbors=('smetiště', 'auto', 'tunel'),
                 items=('rozbité_auto', 'žebřík'),
                 bag=(),
                 ),
    ScenarioStep(tsTAKE, 'vezmi žebřík',  # Zadaný příkaz
                 get_take_message('žebřík', 10),
                 place='křižovatka',
                 neighbors=('smetiště', 'auto', 'tunel'),
                 items=('rozbité_auto',),
                 bag=('žebřík',),
                 ),
    ScenarioStep(tsGOTO, 'jdi tunel',  # Zadaný příkaz
                 goto_first_part + place_details['tunel'],
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=(),
                 bag=('žebřík',),
                 ),
    ScenarioStep(tsGOTO, 'Jdi benzínka',  # Zadaný příkaz
                 goto_first_part + place_details['benzínka'],
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž', 'lano', 'raketa'),
                 bag=('žebřík',),
                 ),
    ScenarioStep(tsGOTO, 'Jdi kanál',  # Zadaný příkaz
                 goto_first_part + place_details['kanál'],
                 place='kanál',
                 neighbors=(),
                 items=('hák',),
                 bag=('žebřík',),
                 ),
    ScenarioStep(tsNS_1, 'POUŽIJ ŽEBŘÍK',  # Zadaný příkaz
                 'Použil si žebřík:\n'
                 'Nyní se můžeš dostat zpět z kanálu.\n'
                 'ztratil si žebřík',
                 place='kanál',
                 neighbors=('benzínka',),
                 items=('hák',),
                 bag=(),
                 tests=[
                     "first_argument_in_bag",
                     "argument_usable",
                     "argument_usable_in"
                 ],
                 sets={"items.used": 2, },
                 ),
    ScenarioStep(tsTAKE, 'vezmi hák',  # Zadaný příkaz
                 get_take_message('hák', 1),
                 place='kanál',
                 neighbors=('benzínka',),
                 items=(),
                 bag=('hák',),
                 ),
    ScenarioStep(tsGOTO, 'Jdi benzínka',  # Zadaný příkaz
                 goto_first_part + place_details['benzínka'],
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž', 'lano', 'raketa'),
                 bag=('hák',),
                 ),
    ScenarioStep(tsTAKE, 'vezmi lano',  # Zadaný příkaz
                 get_take_message('lano', 5),
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž', 'raketa'),
                 bag=('hák', 'lano'),
                 ),
    ScenarioStep(tsTAKE, 'vezmi raketa',  # Zadaný příkaz
                 get_take_message('raketa', 4),
                 place='benzínka',
                 neighbors=('tunel', 'most', 'kanál'),
                 items=('nádrž',),
                 bag=('hák', 'lano', 'raketa'),
                 ),
    ScenarioStep(tsGOTO, 'Jdi most',  # Zadaný příkaz
                 goto_first_part + place_details['most'],
                 place='most',
                 neighbors=('benzínka',),
                 items=(),
                 bag=('hák', 'lano', 'raketa'),
                 ),
    ScenarioStep(tsNS_2, 'zkombinuj hák lano',  # Zadaný příkaz
                 'Zkombinoval si hák a lano:\n'
                 'Vytvořil si nový předmět: lano_s_hákem (váha 6kg)',
                 place='most',
                 neighbors=('benzínka',),
                 items=(),
                 bag=('raketa', 'lano_s_hákem'),
                 tests=[
                     "first_argument_in_bag",
                     "second_argument_in_bag",
                     "arguments_not_same",
                     "arguments_combinable",
                 ],
                 sets={"items.created": 1, },
                 ),
    ScenarioStep(tsNS_1, 'POUŽIj LANO_S_HÁKEM',  # Zadaný příkaz
                 'Použil si lano_s_hákem:\n'
                 'Nyní se můžeš přehoupnout přes rozpadlý most.\n'
                 'ztratil si lano_s_hákem',
                 place='most',
                 neighbors=('benzínka', 'autoopravna'),
                 items=(),
                 bag=('raketa',),
                 tests=[
                     "first_argument_in_bag",
                     "argument_usable",
                     "argument_usable_in"
                 ],
                 sets={"items.used": 3, },
                 ),
    ScenarioStep(tsGOTO, 'Jdi autoopravna',  # Zadaný příkaz
                 goto_first_part + place_details['autoopravna'],
                 place='autoopravna',
                 neighbors=('most',),
                 items=('raketomet',),
                 bag=('raketa',),
                 ),
    ScenarioStep(tsTAKE, 'vezmi raketomet',  # Zadaný příkaz
                 get_take_message('raketomet', 6),
                 place='autoopravna',
                 neighbors=('most',),
                 items=(),
                 bag=('raketa', 'raketomet'),
                 ),
    ScenarioStep(tsNS_2, 'zkombinuj raketa raketomet',  # Zadaný příkaz
                 'Zkombinoval si raketa a raketomet:\n'
                 'Vytvořil si nový předmět: nabitý_raketomet (váha 10kg)',
                 place='autoopravna',
                 neighbors=('most',),
                 items=(),
                 bag=('nabitý_raketomet',),
                 tests=[
                     "first_argument_in_bag",
                     "second_argument_in_bag",
                     "arguments_not_same",
                     "arguments_combinable",
                 ],
                 sets={"items.created": 2, },
                 ),
    ScenarioStep(tsNS_1, 'POUŽIj NABITÝ_RAKETOMET',  # Zadaný příkaz
                 'Použil si nabitý_raketomet:\n'
                 'Rozbil si dveře na balkon.\n'
                 'ztratil si nabitý_raketomet',
                 place='autoopravna',
                 neighbors=('most', 'balkon'),
                 items=(),
                 bag=(),
                 tests=[
                     "first_argument_in_bag",
                     "argument_usable",
                     "argument_usable_in"
                 ],
                 sets={"items.used": 4, },
                 ),
    ScenarioStep(tsGOTO, 'Jdi balkon',  # Zadaný příkaz
                 goto_first_part + place_details['balkon'],
                 place='balkon',
                 neighbors=('autoopravna', 'křižovatka'),
                 items=('kanystr',),
                 bag=(),
                 ),
    ScenarioStep(tsTAKE, 'vezmi kanystr',  # Zadaný příkaz
                 get_take_message('kanystr', 10),
                 place='balkon',
                 neighbors=('autoopravna', 'křižovatka'),
                 items=(),
                 bag=('kanystr',),
                 ),
    ScenarioStep(tsGOTO, 'Jdi křižovatka',  # Zadaný příkaz
                 goto_first_part + place_details['křižovatka'],
                 place='křižovatka',
                 neighbors=('smetiště', 'auto', 'tunel'),
                 items=('rozbité_auto',),
                 bag=('kanystr',),
                 ),
    ScenarioStep(tsGOTO, 'Jdi auto',  # Zadaný příkaz
                 goto_first_part + place_details['auto'],
                 place='auto',
                 neighbors=('křižovatka',),
                 items=(),
                 bag=('kanystr',),
                 ),
    ScenarioStep(tsSUCCESS, 'naplň',  # Zadaný příkaz
                 'Naplnil si auto benzínem a s parťákem odjíždíte.\n'
                 'Gratuluji, vyhrál jsi hru!',
                 place='auto',
                 neighbors=('křižovatka',),
                 items=(),
                 bag=('kanystr',),
                 tests=["in_car", "has_gas"]
                 ),
)  # N-tice
                 )  # Konstruktor

############################################################################

ScenarioStep.next_index = +1  # Index prvního kroku za startem

BASIC = Scenario(stBASIC, (
    START_STEP,
    HAPPY.steps[1],  # Vezmi žebrík
    HAPPY.steps[2],  # Jdi křižovatka
    HAPPY.steps[3],  # Polož žebrík
    ScenarioStep(tsHELP, '?',  # Zadaný příkaz
                 HELP,
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto', 'žebřík'),
                 bag=(),
                 ),
    ScenarioStep(tsEND, 'konec',  # Zadaný příkaz
                 'Ukončil si hru.',
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto', 'žebřík'),
                 bag=(),
                 ),
)  # N-tice
                 )  # Konstruktor

############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení základních akcí
# a současně vyzkouší vyvolání nápovědy a nestandardní ukončení.

ScenarioStep.next_index = -1  # Index kroku před korektním startem

WRONG_START = \
    ScenarioStep(tsNOT_START, 'start',  # Zadaný příkaz
                 'Prvním příkazem není startovací příkaz.\n'
                 'Pro start zadejte prázdný příkaz.\n',
                 '',  # Aktuální prostor
                 (),  # Aktuální sousedé
                 (),  # H-objekty v prostoru
                 (),  # H-Objekty v batohu
                 )

ScenarioStep.next_index = +1  # Index prvního kroku za startem

MISTAKE = Scenario(stMISTAKES, (
    WRONG_START,
    START_STEP,
    ScenarioStep(tsEMPTY, '',  # Zadaný příkaz
                 'Prázdný příkaz lze použít pouze pro start hry',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    ScenarioStep(tsUNKNOWN, 'neexistuje',  # Zadaný příkaz
                 'Tento příkaz neznám: neexistuje',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    ScenarioStep(tsMOVE_WA, "jdi",  # Zadaný příkaz
                 'Nevím, kam mám jít.\n'
                 'Je třeba zadat název cílového prostoru.',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    ScenarioStep(tsTAKE_WA, "vezmi",  # Zadaný příkaz
                 'Nevím, co mám zvednout.\n'
                 'Je třeba zadat název zvedaného objektu.',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    ScenarioStep(tsPUT_DOWN_WA, "polož",  # Zadaný příkaz
                 'Nevím, co mám položit.\n'
                 'Je třeba zadat název pokládaného objektu.',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    ScenarioStep(tsBAD_NEIGHBOR, "jdi někam",  # Zadaný příkaz
                 'Do zadaného prostoru se odsud jít nedá: někam',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    ScenarioStep(tsBAD_ITEM, "vezmi pes",  # Zadaný příkaz
                 'Zadaný objekt v prostoru není: pes',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 ),
    HAPPY.steps[1],  # Vezmi žebrík
    HAPPY.steps[2],  # Jdi křižovatka
    ScenarioStep(tsUNMOVABLE, "vezmi rozbité_auto",  # Zadaný příkaz
                 'Zadaný objekt není možno zvednout: rozbité_auto',
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto',),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsGOTO, 'Jdi smetiště',  # Zadaný příkaz
                 goto_first_part + place_details['smetiště'],
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=(),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsNS_0, 'prozkoumej',  # Zadaný příkaz
                 'Našel jsi na zemi páčidlo (váha 1kg), lano (váha 5kg)',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 needs={"junkyard.searched": False},
                 tests=["hidden_items_present"],
                 sets={"junkyard.searched": True},
                 ),
    ScenarioStep(tsBAG_FULL, 'Vezmi lano',  # Zadaný příkaz
                 'Zadaný objekt se už do batohu nevejde: lano',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsNOT_IN_BAG, 'polož lano',  # Zadaný příkaz
                 'Zadaný objekt v batohu není: lano',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsHELP, '?',  # Zadaný příkaz
                 HELP,
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsEND, 'KONEC',  # Zadaný příkaz
                 'Ukončil si hru.',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 ),
)  # N-tice
                   )  # Konstruktor

############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení povinně definovaných akcí.
ScenarioStep.next_index = 5  # Index prvního nestandardního kroku
MISTAKE_NS = Scenario(stMISTAKES_NS, (
    START_STEP,
    ScenarioStep(tsNS0_WrongCond, 'prozkoumej',  # Zadaný příkaz
                 'V daném prostoru nejsou žádné skryté předměty',
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 tests=["hidden_items_present"],
                 ),
    ScenarioStep(tsNOT_SUCCESS, 'naplň',  # Zadaný příkaz
                 "Ještě nemáš benzín.",
                 place='auto',
                 neighbors=("křižovatka",),
                 items=("žebřík",),
                 bag=(),
                 tests=["has_gas"],
                 ),
    HAPPY.steps[1],  # Vezmi žebřík
    HAPPY.steps[2],  # Jdi křižovatka
    ScenarioStep(tsNOT_SUCCESS, 'naplň',  # Zadaný příkaz
                 "Nejsi u auta.",
                 place='křižovatka',
                 neighbors=('smetiště', 'auto'),
                 items=('rozbité_auto',),
                 bag=("žebřík",),
                 tests=["in_car"],
                 ),
    ScenarioStep(tsGOTO, "jdi smetiště",  # Zadaný příkaz
                 goto_first_part + place_details['smetiště'],
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=(),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsNS_0, 'prozkoumej',  # Zadaný příkaz
                 'Našel jsi na zemi páčidlo (váha 1kg), lano (váha 5kg)',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 needs={"junkyard.searched": False},
                 tests=["hidden_items_present"],
                 sets={"junkyard.searched": True},
                 ),
    ScenarioStep(tsNS0_WrongCond, 'prozkoumej',  # Zadaný příkaz
                 'Daný prostor si již prozkoumal',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 needs={"junkyard.searched": False},
                 ),
    ScenarioStep(tsNS1_0Args, 'použij',  # Zadaný příkaz
                 'Nevím, co chceš použít',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 ),
    ScenarioStep(tsNS1_WrongCond, 'použij lano',  # Zadaný příkaz
                 'Daný předmět nemáš v batohu: lano',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 tests=["first_argument_in_bag"],
                 ),
    ScenarioStep(tsNS1_WrongCond, 'použij žebřík',  # Zadaný příkaz
                 "Daný předmět zde nemůžeš použít: žebřík",
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano'),
                 bag=("žebřík",),
                 tests=["argument_usable_in"],
                 ),
    ScenarioStep(tsPUT_DOWN, 'Polož žebřík',  # Zadaný příkaz
                 get_drop_message('žebřík'),
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('páčidlo', 'lano', 'žebřík'),
                 bag=(),
                 ),
    ScenarioStep(tsTAKE, 'Vezmi páčidlo',  # Zadaný příkaz
                 get_take_message('páčidlo', 1),
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('lano', 'žebřík'),
                 bag=('páčidlo',),
                 ),
    ScenarioStep(tsTAKE, 'Vezmi lano',  # Zadaný příkaz
                 get_take_message('lano', 5),
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 ),
    ScenarioStep(tsNS1_WrongCond, 'použij lano',
                 'Daný předmět se nedá použít: lano',
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 tests=["argument_usable"],
                 ),
    ScenarioStep(tsNS2_1Args, 'zkombinuj lano',  # Zadaný příkaz
                 "Zadej dva předměty, které chceš zkombinovat",
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 ),
    ScenarioStep(tsNS2_WrongCond, 'zkombinuj pes lano',  # Zadaný příkaz
                 "Předmět nemáš v batohu: pes",
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 tests=["first_argument_in_bag"],
                 ),
    ScenarioStep(tsNS2_WrongCond, 'zkombinuj lano kočka',  # Zadaný příkaz
                 "Předmět nemáš v batohu: kočka",
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 tests=["second_argument_in_bag"],
                 ),
    ScenarioStep(tsNS2_WrongCond, 'zkombinuj lano lano',  # Zadaný příkaz
                 "Zadej dva různé předměty",
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 tests=["arguments_not_same"]
                 ),
    ScenarioStep(tsNS2_WrongCond, 'zkombinuj lano páčidlo',  # Zadaný příkaz
                 "Dané předměty se nedají zkombinovat: lano, páčidlo",
                 place='smetiště',
                 neighbors=('křižovatka',),
                 items=('žebřík',),
                 bag=('páčidlo', 'lano'),
                 tests=["arguments_combinable"]
                 ),
    ScenarioStep(tsGOTO, "jdi křižovatka",  # Zadaný příkaz
                 goto_first_part + place_details['křižovatka'],
                 place='křižovatka',
                 neighbors=("smetiště", "auto"),
                 items=('rozbité_auto',),
                 bag=('páčidlo', 'lano'),
                 ),
    ScenarioStep(tsNS_1, 'Použij páčidlo',  # Zadaný příkaz
                 'Páčidlo se rozpadlo na kousky, ale otevřel si dveře do '
                 'tunelu.\n'
                 'ztratil si páčidlo',
                 place='křižovatka',
                 neighbors=('smetiště', 'auto', 'tunel'),
                 items=('rozbité_auto',),
                 bag=('lano',),
                 tests=[
                     "first_argument_in_bag",
                     "argument_usable",
                     "argument_usable_in"
                 ],
                 sets={"items.used": 1, },
                 ),
    ScenarioStep(tsGOTO, "jdi tunel",  # Zadaný příkaz
                 goto_first_part + place_details['tunel'],
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=(),
                 bag=('lano',),
                 ),
    ScenarioStep(tsNS_0, 'prozkoumej',  # Zadaný příkaz
                 'Našel jsi na zemi raketa (váha 4kg)',
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=('raketa',),
                 bag=('lano',),
                 needs={"tunnel.searched": False},
                 tests=["hidden_items_present"],
                 sets={"tunnel.searched": True},
                 ),
    ScenarioStep(tsNS0_WrongCond, 'prozkoumej',  # Zadaný příkaz
                 'Daný prostor si již prozkoumal',
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=('raketa',),
                 bag=('lano',),
                 needs={"tunnel.searched": False},
                 ),
    ScenarioStep(tsEND, 'konec',  # Zadaný příkaz
                 'Ukončil si hru.',
                 place='tunel',
                 neighbors=('křižovatka', 'benzínka'),
                 items=('raketa',),
                 bag=('lano',),
                 ),
)  # N-tice
                      )  # Konstruktor

###########################################################################q

# Slovník převádějící názvy scénářů na scénáře
NAME_2_SCENARIO = {
    HAPPY.name: HAPPY,  # Základní úspěšný (= šťastný) scénář
    BASIC.name: BASIC,  # Scénář obsahující jen povinné akce
    MISTAKE.name: MISTAKE,  # Scénář chybně zadaných povinných akcí
    MISTAKE_NS.name: MISTAKE_NS,  # Scénář chybně zadaných dodatečných akcí
}

###########################################################################q
dbg.stop_mod(1, __name__)
