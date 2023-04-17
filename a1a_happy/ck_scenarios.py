#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_EDU/p1_Demos23s/game23s/a1a_happy/ck_scenarios.py
"""
Ideový návrh šťastného scénáře pro hru inspirovanou
pohádkou o Červené Karkulce.
"""
import dbg; dbg.start_mod(1, __name__)
###########################################################################q

from game23s.api.scenario   import ScenarioStep, Scenario
from game23s.api.scen_types import *  # Především typu kroků



###########################################################################q
# Základní úspěšný scénář demonstrující průběh hry, při němž hráč
# nezadává žádné chybné příkazy a dosáhne zadaného cíle.
HAPPY = Scenario(stHAPPY, (
    ScenarioStep(tsSTART, '',                       # Zadaný příkaz
        'Vítejte!\n'
        'Toto je příběh o Červené Karkulce, babičce a vlkovi.\n'
        'Svými příkazy řídíte Karkulku, aby donesla bábovku a víno\n'
        'babičce v chaloupce za temným lesem.\n'
        'Když přijde do chaloupky, měla by položit dárky, vzbudit babičku,\n'
        'pozdravit a popřát jí k narozeninám.\n'
        'Jste-li dobrodružné typy, můžete to místo s babičkou provést\n'
        's vlkem, který spí v temném lese.\n'
        '\nNebudete-li si vědět rady, zadejte znak ?, jenž zobrazí nápovědu.',
        'Domeček',                                  # Aktuální prostor
        ('Les',),                                   # Aktuální sousedé
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
        ),
    ScenarioStep(tsNS_0, 'Pozdrav',                 # Zadaný příkaz
        'Karkulka pozdravila osobu Babička',
        'Chaloupka',                                # Aktuální prostor
        ('Temný_les', ),                            # Aktuální sousedé
        ('Postel', 'Stůl', 'Babička', 'Bábovka', 'Víno', ),
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsSUCCESS, 'Popřej',                  # Zadaný příkaz
        'Karkulka popřála objektu babička vše nejlepší k narozeninám\n'
        'Úspěšně jste ukončili hru.\n'
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
    # BASIC       .name: BASIC,     # Scénář obsahující jen povinné akce
    # MISTAKE     .name: MISTAKE,   # Scénář chybně zadaných povinných akcí
    # MISTAKE_NS  .name: MISTAKE_NS,# Scénář chybně zadaných dodatečných akcí
}



###########################################################################q
dbg.stop_mod(1, __name__)
