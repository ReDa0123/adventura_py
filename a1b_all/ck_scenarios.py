#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_EDU/p1_Demos23s/game23s/a1b_all/ck_scenarios.py
"""
Modul obsahuje základní čtveřici scénářů pro hru inspirovanou pohádkou
o Červené Karkulce. Podle těchto scénářů je možno hrát či testovat hru.
Aby bylo možno jednotlivé scénáře od sebe odlišit, je každý pojmenován
a má přiřazen typ, podle které lze blíže určit, k čemu je možno jej použít.
Scénáře jsou definovány jako posloupnosti kroků.
"""
import dbg; dbg.start_mod(1, __name__)
###########################################################################q

from game23s.api.scenario   import ScenarioStep, Scenario
from game23s.api.scen_types import *  # Především typu kroků



###########################################################################q
ScenarioStep.next_index = 0   # Index prvního kroku za startem

SUBJECT = (
    'Toto je příběh o Červené Karkulce, babičce a vlkovi.\n'
    'Svými příkazy řídíte Karkulku, aby donesla bábovku a víno\n'
    'babičce v chaloupce za temným lesem.\n'
    'Karkulka musí nejprve v domečku vložit do košíku víno a bábovku,\n'
    'a potom přejít přes les a temný les do chaloupky.\n'
    'Když přijde do chaloupky, měla by položit dárky, vzbudit babičku,\n'
    'pozdravit ji a popřát jí k narozeninám.\n'
    'Jste-li dobrodružné typy, můžete to místo s babičkou provést\n'
    's vlkem, který spí v temném lese.\n'
    )

# Základní úspěšný scénář demonstrující průběh hry, při němž hráč
# nezadává žádné chybné příkazy a dosáhne zadaného cíle.
HAPPY = Scenario(stHAPPY, (
    START_STEP :=
    ScenarioStep(tsSTART, '',                       # Zadaný příkaz
        WELCOME := 'Vítejte!\n' + SUBJECT
      + '\nNebudete-li si vědět rady, zadejte znak ?, jenž zobrazí nápovědu.',
        'Domeček',                                  # Aktuální prostor
        ('Les',),                                   # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        # Počáteční stavy stavových proměnných
        sets = {'grandma.sleeping': True,
                'grandma.greeted':  False,
                'wolf.sleeping': True,
                'wolf.greeted':  False,
                'wakeable': ('babička', 'vlk'), # Objekty, které lze budit
                },
        tests = ['argument_present',   # Argument je v aktuálním prostoru
                 'argument_wakeable',  # Argument je buditelný
                 'argument_sleeping',  # Argument spí
                 'wakeable_present',   # V akt. prost. je buditelný objekt
                 'waken_present',      # V akt. prost. je probuzený objekt
                 'greeted_present', ], # V ak. p. je již pozdravený objekt
        ),
    ScenarioStep(tsTAKE, 'Vezmi víno',              # Zadaný příkaz
        'Karkulka dala do košíku objekt Víno',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Stůl', 'Panenka', ),           # H-objekty v prostoru
        ('Víno', ),                                 # H-Objekty v batohu
        ),
    ScenarioStep(tsTAKE, 'Vezmi bábovka',           # Zadaný příkaz
        'Karkulka dala do košíku objekt Bábovka',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Stůl', 'Panenka', ),                      # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsGOTO, 'Jdi LES',                 # Zadaný příkaz
        'Karkulka se přesunula do prostoru:\n'
        'Les s jahodami, malinami a pramenem vody',
        'Les',                                      # Aktuální prostor
        ('Domeček', 'Temný_les', ),                 # Aktuální sousedé
        ('Maliny', 'Jahody', 'Studánka', ),         # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsGOTO, 'Jdi temný_les',           # Zadaný příkaz
        'Karkulka se přesunula do prostoru:\n'
        'Temný_les s jeskyní a číhajícím vlkem',
        'Temný_les',                                # Aktuální prostor
        ('Les', 'Jeskyně', 'Chaloupka', ),          # Aktuální sousedé
        ('Vlk',  ),                                 # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsGOTO, 'Jdi chaloupka',           # Zadaný příkaz
        'Karkulka se přesunula do prostoru:\n'
        'Chaloupka, kde bydlí babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les',),                             # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', ),            # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož bábovka',       # Zadaný příkaz
        'Karkulka vyndala z košíku objekt Bábovka',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les',),                             # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', ), # H-objekty v prostoru
        ('Víno', ),                                 # H-Objekty v batohu
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož VÍNO',          # Zadaný příkaz
        'Karkulka vyndala z košíku objekt Víno',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsNS_1, 'Probuď babička',          # Zadaný příkaz
        'Karkulka probudila osobu Babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        needs = {},
        tests = ['argument_present',
                 'argument_wakeable',
                 'argument_sleeping', ],
        sets  = {'grandma.sleeping': False, },
        ),
    ScenarioStep(tsNS_0, 'Pozdrav',                 # Zadaný příkaz
        'Karkulka pozdravila osobu Babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        needs = {'grandma.greeted':  False, },
        tests = ['waken_present', ],
        sets  = {'grandma.greeted':  True, },
        ),
    ScenarioStep(tsSUCCESS, 'Popřej',                  # Zadaný příkaz
        'Karkulka popřála objektu babička vše nejlepší k narozeninám\n'
        'Úspěšně jste ukončili hru.\n'
        'Děkujeme, že jste si zahráli.',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        tests = ['greeted_present', ],
        ),
    )   # N-tice
)   # Konstruktor



############################################################################

ScenarioStep.next_index = +1  # Index prvního kroku za startem

BASIC = Scenario(stBASIC, (
    START_STEP,
    ScenarioStep(tsGOTO, 'Jdi LES',                 # Zadaný příkaz
        'Karkulka se přesunula do prostoru:\n'
        'Les s jahodami, malinami a pramenem vody',
        'Les',                                      # Aktuální prostor
        ('Domeček', 'Temný_les', ),                 # Aktuální sousedé
        ('Maliny', 'Jahody', 'Studánka', ),         # H-objekty v prostoru
        ( ),                                        # H-Objekty v batohu
        ),
    ScenarioStep(tsTAKE, 'Vezmi maliny',            # Zadaný příkaz
        'Karkulka dala do košíku objekt Maliny',
        'Les',                                      # Aktuální prostor
        ('Domeček', 'Temný_les', ),                 # Aktuální sousedé
        ('Jahody', 'Studánka', ),                   # H-objekty v prostoru
        ('Maliny', ),                               # H-Objekty v batohu
        ),
    ScenarioStep(tsPUT_DOWN, 'Polož maliny',        # Zadaný příkaz
        'Karkulka vyndala z košíku objekt Maliny',
        'Les',                                      # Aktuální prostor
        ('Domeček', 'Temný_les', ),                 # Aktuální sousedé
        ('Maliny', 'Jahody', 'Studánka', ),         # H-objekty v prostoru
        ( ),                                        # H-Objekty v batohu
        ),
    ScenarioStep(tsHELP, '?',                       # Zadaný příkaz
        SUBJECT,
        'Les',                                      # Aktuální prostor
        ('Domeček', 'Temný_les', ),                 # Aktuální sousedé
        ('Maliny', 'Jahody', 'Studánka', ),         # H-objekty v prostoru
        ( ),                                        # H-Objekty v batohu
        ),
    ScenarioStep(tsEND, 'KONEC',                    # Zadaný příkaz
        'Ukončili jste hru.\nDěkujeme, že jste si zahráli.',
        'Les',                                      # Aktuální prostor
        ('Domeček', 'Temný_les', ),                 # Aktuální sousedé
        ('Maliny', 'Jahody', 'Studánka', ),         # H-objekty v prostoru
        ( ),                                        # H-Objekty v batohu
        ),
    )   # N-tice
)   # Konstruktor



############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení základních akcí
# a současně vyzkouší vyvolání nápovědy a nestandardní ukončení.

ScenarioStep.next_index = -1  # Index kroku před korektním startem

WRONG_START = ScenarioStep(tsNOT_START, 'start', # Zadaný příkaz
        'Prvním příkazem není startovací příkaz.\n' 
        'Hru, která neběží, lze spustit pouze startovacím příkazem.\n',
        '',                                         # Aktuální prostor
        (),                                         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        )

ScenarioStep.next_index = +1  # Index prvního kroku za startem

MISTAKE = Scenario(stMISTAKES, (
    WRONG_START,
    START_STEP,
    ScenarioStep(tsEMPTY, '',                       # Zadaný příkaz
        'Prázdný příkaz lze použít pouze pro start hry',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsUNKNOWN, 'maso',                 # Zadaný příkaz
        'Tento příkaz neznám: maso',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsMOVE_WA, "jdi",                  # Zadaný příkaz
        'Nevím, kam mám jít.\n'
        'Je třeba zadat název cílového prostoru.',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsTAKE_WA, "vezmi",                # Zadaný příkaz
        'Nevím, co mám zvednout.\n'
        'Je třeba zadat název zvedaného objektu.',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsPUT_DOWN_WA, "polož",            # Zadaný příkaz
        'Nevím, co mám položit.\n'
        'Je třeba zadat název pokládaného objektu.',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsBAD_NEIGHBOR, "jdi do_háje", # Zadaný příkaz
        'Do zadaného prostoru se odsud jít nedá: do_háje',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsBAD_ITEM, "vezmi whisky",        # Zadaný příkaz
        'Zadaný objekt v prostoru není: whisky',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsUNMOVABLE, "vezmi stůl",         # Zadaný příkaz
        'Zadaný objekt není možno zvednout: stůl',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsTAKE, 'Vezmi víno',              # Zadaný příkaz
        'Karkulka dala do košíku objekt Víno',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Bábovka', 'Stůl', 'Panenka', ),           # H-objekty v prostoru
        ('Víno', ),                                 # H-Objekty v batohu
        ),
    ScenarioStep(tsTAKE, 'Vezmi bábovka',           # Zadaný příkaz
        'Karkulka dala do košíku objekt Bábovka',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Stůl', 'Panenka', ),                      # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsBAG_FULL, 'Vezmi panenka',       # Zadaný příkaz
        'Zadaný objekt se už do košíku nevejde: panenka',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Stůl', 'Panenka', ),                      # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsNOT_IN_BAG, 'polož panenka',     # Zadaný příkaz
        'Zadaný objekt v košíku není: panenka',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Stůl', 'Panenka', ),                      # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsHELP, '?',                       # Zadaný příkaz
        SUBJECT,
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Stůl', 'Panenka', ),                      # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsEND, 'KONEC',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'Domeček',                                  # Aktuální prostor
        ('Les', ),                                  # Aktuální sousedé
        ('Stůl', 'Panenka', ),                      # H-objekty v prostoru
        ('Bábovka', 'Víno', ),                      # H-Objekty v batohu
        ),
    )   # N-tice
)   # Konstruktor



############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení povinně definovaných akcí.
ScenarioStep.next_index = 5    # Index prvního nestandardního kroku
MISTAKE_NS = Scenario(stMISTAKES_NS, (
    HAPPY.steps[0],
    ScenarioStep(tsNS0_WrongCond, 'Pozdrav',        # Zadaný příkaz
        'V aktuálním prostoru není koho zdravit',
        'Domeček',                                  # Aktuální prostor
        ('Les',),                                   # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka',),    # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        tests = ['wakeable_present', ],
        ),
    ScenarioStep(tsNOT_SUCCESS, 'Popřej',        # Zadaný příkaz
        'V aktuálním prostoru není komu popřát.',
        'Domeček',                                  # Aktuální prostor
        ('Les',),                                   # Aktuální sousedé
        ('Bábovka', 'Víno', 'Stůl', 'Panenka',),    # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        tests = ['greeted_present', ],
        ),
    HAPPY.steps[1],   # Vezmi víno
    HAPPY.steps[2],   # Vezmi Bábovka
    HAPPY.steps[3],   # Jdi les
    HAPPY.steps[4],   # Jdi Temný_les
    HAPPY.steps[5],   # Jdi Chaloupka
    HAPPY.steps[6],   # Polož Bábovka
    HAPPY.steps[7],   # Polož Víno
    ScenarioStep(tsNS0_WrongCond, 'Pozdrav',        # Zadaný příkaz
        'Nemá smysl zdravit, osoba babička ještě není probuzená.',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        tests = ['waken_present'],
        ),
    ScenarioStep(tsNS1_0Args, 'Probuď',             # Zadaný příkaz
        'Nevím, koho mám probudit',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsNS1_WrongCond, 'Probuď Vlk',     # Zadaný příkaz
        'Nelze budit nepřítomný objekt Vlk',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        tests = ['argument_present', ],
        ),
    ScenarioStep(tsNS1_WrongCond, 'Probuď Stůl',    # Zadaný příkaz
        (NS1_WRONG_ARGb := 'Nelze budit objekt ') + 'Stůl',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        tests = ['argument_wakeable'],
        ),
    ScenarioStep(tsNS_1, 'Probuď babička',          # Zadaný příkaz
        'Karkulka probudila osobu Babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        needs = {'grandma.sleeping': True, },
        tests = ['argument_present',
                 'argument_wakeable'],
        sets  = {'grandma.sleeping': False, },
        ),
    ScenarioStep(tsNS1_WrongCond, 'Probuď babička', # Zadaný příkaz
        'Nelze budit osobu, která je již probuzená: Babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        tests = ['argument_sleeping', ]
        ),
    ScenarioStep(tsNOT_SUCCESS, 'popřej',           # Zadaný příkaz
        'Osoba babička ještě nebyla pozdravena',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        tests = ['greeted_present', ]
        ),
    ScenarioStep(tsNS_0, 'Pozdrav',                 # Zadaný příkaz
        'Karkulka pozdravila osobu Babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        needs = {'grandma.sleeping': False,
                 'grandma.greeted':  False},
        sets  = {'grandma.greeted':  True },
        ),
    ScenarioStep(tsNS0_WrongCond, 'Pozdrav',        # Zadaný příkaz
        'Nemá smysl zdravit osobu babička, protože již byla pozdravena',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        needs = {'grandma.greeted':  False},
        ),
    ScenarioStep(tsEND, 'konec',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        ),
    )   # N-tice
)   # Konstruktor



###########################################################################q

# Slovník převádějící názvy scénářů na scénáře
NAME_2_SCENARIO = {
    HAPPY       .name: HAPPY,     # Základní úspěšný (= šťastný) scénář
    BASIC       .name: BASIC,     # Scénář obsahující jen povinné akce
    MISTAKE     .name: MISTAKE,   # Scénář chybně zadaných povinných akcí
    MISTAKE_NS  .name: MISTAKE_NS,# Scénář chybně zadaných dodatečných akcí
}



###########################################################################q
dbg.stop_mod(1, __name__)
