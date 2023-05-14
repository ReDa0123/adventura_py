#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/api/scenario.py
"""
Třídy pro konstrukci scénářů:
    ScenarioStep
    Scenario

Definované proměnné:
    next_index      - Index následujícího kroku
    HAPPY_NAME      - Povinný název šťastného scénáře
    MISTAKE_NAME    - Povinný název chybového scénáře
    MISTAKE_NS_NAME - Povinný název chybového scénáře pomocných akcí
    START_NAME      - Doporučený název scénáře obsahujícího pouze povinné
                      akce, tj. scénáře přidávaného na počátku vývoje hry
    SCENARIO_NAMES  - N-tice výš zmíněných názvů scénářů

"""
import dbg
dbg.start_mod(2, __name__)
############################################################################

from collections import namedtuple
from .scen_types import (TypeOfScenario, TypeOfStep,
                         stHAPPY, stBASIC, stMISTAKES, stMISTAKES_NS)



############################################################################

# Definuje pomocnou třídu pojmenovanou ScenarioStep
_Step = namedtuple('ScenarioStep', 'index typeOfStep command message place '
                                   'neighbors items bag needs tests sets')

def ScenarioStep(typeOfStep:TypeOfStep, command:str, message:str, place:str,
         neighbors:tuple[str,...], items:tuple[str,...], bag:tuple[str,...],
         *, needs:dict[str,object]={}, tests:list[str]=[],
         sets:dict[str,object]={}):
    """Funkce vystupuje vůči okolnímu programu jako konstruktor,
    který vytváří instance třídy ScenarioStep, přičemž očekává argumenty:
    typeOfStep:TypeOfStep   - Typ kroku scénáře
    command:str             - Zadávaný příkaz
    message:str             - Odpověď hry
    place:str               - Název aktuálního prostoru
    neighbors:tuple[str]    - Aktuální sousedé aktuálního prostoru
    items:tuple[str]        - Aktuální předměty v aktuálním prostoru
    bag:tuple[str]          - Aktuální předměty v batohu
    needs:dict[str,object]  - Požadované stavy pro spuštění
    tests:list[str]         - Názvy testů složitějších podmínek
    sets:dict[str,object]   - Nastavované stavy
    """
    result = ScenarioStep.new(ScenarioStep.next_index, typeOfStep, command,
             message, place, neighbors, items, bag, needs, tests, sets)
    # Původní konstruktor pojmenovaných n-tic nevyhovuje, protože
    # po každém kroku je třeba inkrementovat index následujícího kroku
    ScenarioStep.next_index += 1
    return result

# Odkaz na konstruktor třídy ukládáme do atributu funkce
ScenarioStep.new = _Step
del _Step

# Atribut next_index zadává vypisovaný index následujícího kroku, jenž
# je vhodné inicializovat vždy při zadávání počátečního kroku scénáře
ScenarioStep.next_index = 0

def __repr__(self):     # Název v rámci modulu nekoliduje
    return (f'{self.index}. krok: {self.command}\n{30*"-"}\n'
            f'{self.message}\n{60*"-"}\n'
            f'Aktuální prostor:    {self.place}\n'
            f'Sousedé prostoru:    {self.neighbors}\n'
            f'Předměty v prostoru: {self.items}\n'
            f'Předměty v batohu:   {self.bag}\n'
        + ((f'Vyžaduje:            {self.needs}\n') if self.needs else '')
        + ((f'Složitější podmínky: {self.tests}\n') if self.tests else '')
        + ((f'Nastavuje:           {self.sets}\n')  if self.sets  else '')
        +   f'{60*"="}\n')

# Funkci přiřadíme jako atribut třídě pojmenované n-tice
ScenarioStep.new.__repr__ = __repr__
del __repr__   # Smažu dočasnou proměnnou



############################################################################

class Scenario:
    """
    Třída scénářů definujících požadované chování hry.
    """
    print_state = False     # Zda při testu průběžně zobrazovat stav

    def __init__(self, scenario_type:TypeOfScenario,
                 steps:tuple[ScenarioStep,...]|list[ScenarioStep,...],
                 name: str = ''):
        self._type = scenario_type
        self._steps = steps
        self._name = (scenario_type.name
                      if scenario_type.ordinal <= stMISTAKES_NS.ordinal
                      else name)
        if not self._name:  # Pokud název zůstal prázdný
            raise Exception('Nebyl zadán název doplňkového scénáře')


    def __repr__(self) -> str:
        """
        Jako systémový podpis daného scénáře vrátí jeho název.
        """
        return self._name

    # TODO Doplnit funkci __str__() nebo její náhražku -- např. prn()
    # def __str__(self) -> str:
    #     """
    #     Jako uživatelský podpis daného scénáře vrátí jeho název
    #     následovaný výpisem jeho kroků.
    #     """
    #     result  = f'Definice scénáře {self._name}\n{70*"V"}\n'
    #     steps   = [f'{step}' for step in self._steps]
    #     result += '\n'.join(steps) + f'{70*"A"}\n' \
    #               f'Konec definice scénáře: {self._name}\n\n'
    #     return result
    #

    @property
    def name(self) -> str:
        """
        Vrátí název daného scénáře.
        """
        return self._name


    @property
    def steps(self) -> tuple[ScenarioStep]:
        """
        Vrátí n-tici kroků daného scénáře.
        """
        return self._steps


    @property
    def type(self) -> TypeOfScenario:
        """
        Vrátí typ daného scénáře.
        """
        return self._type


    def simulate(self, with_state:bool=False) -> None:
        """
        Vytiskne jednoduchou simulaci běhu hry podle daného scénáře,
        přičemž hodnota argumentu `with_state` určuje,
        zda se v každém kroku zobrazí pouze příkaz a odpověď hry (`False`),
        anebo se navíc vytisknou informace o požadovaném stavu hry
        po provedeném kroku (`True`).
        """
        print(f'\nSimulace scénáře: {self._name}\n{70*"#"}')
        for step in self.steps:
            if with_state:
                print(step)
            else:
                print(f'{step.index}. {step.command}\n{30*"-"}\n'
                      f'{step.message}\n{60*"="}\n')
        input(f'{70*"#"}\n=== Konec simulace scénáře {self._name} ===\n\n'
              f'Stiskněte Enter')



############################################################################

# SCENARIO_NAMES  = tuple(s.name for s in
#                         (stHAPPY, stREQUIRED, stMISTAKES, stMISTAKES_NS))



############################################################################
dbg.stop_mod(2, __name__)
