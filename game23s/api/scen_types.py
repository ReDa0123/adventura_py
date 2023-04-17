#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/api/scen_types.py
"""
Třídy definující typy scénářů a jejich kroků¤
+ jejich instance = konkrétní typy.

Definované třídy:
    TypeOfScenario
    SubtypeOfStep(Enum) - 9 podtypů kroku scénáře
    TypeOfStep

Instance výše definovaných typů:
    6 typů scénářů, názvy mají předponu st - st???
    40 typů kroku scénáře, názvy mají předponu ts - ts???
    ALL_TYPES        - Seznam všech definovaných typů kroků
    BASIC_TYPES      - Seznam povinných typů kroků
    HAPPY_TYPES      - Seznam typů kroků povinných ve scénáři HAPPY
    MISTAKE_TYPES    - Seznam typů kroků povinných ve scénáři MISTAKE
    MISTAKE_NS_TYPES - Seznam typů kroků povinných ve scénáři MISTAKE_NS

"""
import dbg
dbg.start_mod(2, __name__)
############################################################################

from enum import Enum


############################################################################

class TypeOfScenario:
    """Instance představují možné typy scénářů hry.
    """
    count = 0
    def __init__(self,
                 description:str,   # Stručný popis
                 purpose:str,       # Stručný popis jeho účelu
                 name:str=''        # Název scénářů daného typu
        ):
        self._ordinal     = TypeOfScenario.count;   TypeOfScenario.count+=1
        self._description = description
        self._purpose     = purpose
        self._name        = name

    @staticmethod
    def get(index:int) -> 'TypeOfScenario':
        """Vrátí typ scénáře se zadaným indexem."""
        match(index):
            case 0: return stHAPPY
            case 1: return stMISTAKES
            case 2: return stMISTAKES_NS
            case 3: return stBASIC
            case 4: return stGENERAL
            case 5: return stDEMO
            case _: raise Exception(f'Typ scénáře se zadaným indexem '
                                     f'neexistuje: {index=}')

    ordinal     = property(lambda self: self._ordinal,
                           doc="Pořadí (index) scénáře mezi ostatními")
    description = property(lambda self: self._description,
                           doc="Název popisující typ daného scénáře")
    purpose     = property(lambda self: self._purpose,
                           doc="Co se pomocí tohoto scénáře testuje")
    name        = property(lambda self: self._name,
                           doc="Název scénářů daného typu")

    def __repr__(self): return self._name



############################################################################

HAPPY_NAME      = "HAPPY"
BASIC_NAME      = "BASIC"
MISTAKE_NAME    = "MISTAKES"
MISTAKE_NS_NAME = "MISTAKES_NS"
FOURTH_NAME     = "FOURTH"
SCEN_NAMES      = [HAPPY_NAME, BASIC_NAME, MISTAKE_NAME, MISTAKE_NS_NAME,
                   FOURTH_NAME, ]

stHAPPY       = TypeOfScenario(
                "základní úspěšný scénář",
                "úspěšné zvládnutí hry",
                HAPPY_NAME)
stBASIC       = TypeOfScenario(
                "základní testovací scénář",
                "reakce na korektně vyvolané povinné akce",
                BASIC_NAME)
stMISTAKES    = TypeOfScenario(
                "základní chybový scénář",
                "reakce na chyby při aktivaci základních akcí",
                MISTAKE_NAME)
stMISTAKES_NS = TypeOfScenario(
                "doplňkový chybový scénář",
                "reakce na chyby při aktivaci pomocných akcí",
                MISTAKE_NS_NAME)
stGENERAL     = TypeOfScenario(
                "obecný testovatelný scénář",
                "alternativní možný testovatelný průběh hry")
stDEMO        = TypeOfScenario(
                "netestovatelný demonstrační scénář",
                "možný průběh hry pro simulace")
# TODO Přidat typ scénáře stFOURTH
# stFOURTH      = TypeOfScenario(
#                 "scénář pro test přidané akce při obhajobě",
#                 "prověření funkčnosti přidané akce")


############################################################################

class SubtypeOfStep(Enum):
    """Podtyp typu kroku - subtype"""
    CORRECT     = 0 # Správně zadaný příkaz povinně zařazený do HAPPY
    STOP        = 1 # Správně zadaný povinný příkaz STOP
    MISTAKE     = 2 # Povinně testovaný chybně zadaný příkaz
    NONSTANDARD = 3 # Správně zadaný příkaz aktivující pomocnou akci
    MISTAKE_NS  = 4 # Povinný test příkazů aktivujících pomocné akce
    DIALOG      = 5 # Součást rozhovoru
    DEMO        = 6 # Demonstrační krok bez doprovodných informací,
                    # který proto nelze použít k testu funkce hry
    MODIFIED    = 7 # Typ používaný v modifikačních zadáních v obhajobách
    UNDEFINED   = 8 # Typ kroků vytvořených pro pomocné operace,
                    # a nesmí se proto vyskytnout v žádném scénáři
    SUCCESS     = 9 # Úspěšné ukončení hry
    HELP        =10 # Správně zadaný povinný příkaz HELP



############################################################################

class TypeOfStep:
    """Mateřská třída typů kroků scénáře.
    """
    def __init__(self, subtype:SubtypeOfStep, arg_count:int,
                 group:'TypeOfStep', name:str, doc:str, extended=False):
        """
        Definuje nový typ kroku
        
        :param subtype:     Podtyp vytvářeného kroku
        :param arg_count:   Požadovaný počet argumentů
        :param group:       Skupinu typů příkazů spouštějících shodnou akci
               Typ této akce je takovým "rodičem" dané skupiny typů,
               který pak tuto skupinu reprezentuje vůči okolí.
               Skupina není kontejner, její členové se pouze hlásí ke
               společnému rodiči, a ten se hlásí k None - podle to se pozná
        :param name:        Název vytvářeného typu
        :param doc:         Dokumentačních komentář vytvářeného typu
        :param extended:    Jedná-li se o typ vytvářený pro konkrétní
                            aplikaci a její pomocné akce
        """
        self._subtype   = SubtypeOfStep(subtype)
        self._arg_count = arg_count
        self._group     = self if group==None else group
        self.__name__   = name
        self.__doc__    = doc
        if extended:
            # Při definici pomocných typů byly již základní kontejnery
            # naplněny a čištění a naplňování kontejnerů těchto typů kroků
            # má na starosti tester scénářů prověřovaných aplikací
            return
        else:
            self._append()

    subtype   = property(lambda self: self._subtype,
                doc='Podtyp kroku')
    arg_count = property(lambda self: self._arg_count,
                doc='Počet argumentů v krocích daného typu')
    group     = property(lambda self: self._group,
                doc='Skupina typů spouštějících shodnou akci')
    name      = property(lambda self: self.__name__,
                doc='Název daného typu kroku a příslušné proměnné')

    def __repr__(self): return self.__name__

    def __str__(self):  return self.__name__

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TypeOfStep):  return False
        return self.__name__ == o.__name__

    def __hash__(self) -> int:
        return __name__.__hash__()

    def _append(self):
        """Přidá odkaz na daný typ do příslušných kontejnerů.
        """
        global ALL_TYPES, BASIC_TYPES, HAPPY_TYPES
        # Základní typy akcí, kontejnery jsou seznamy
        ALL_TYPES.append(self)
        st = self._subtype
        if st == SubtypeOfStep.CORRECT:
            BASIC_TYPES.append(self)
            HAPPY_TYPES.append(self)
        elif st == SubtypeOfStep.STOP:
            BASIC_TYPES  .append(self)
            MISTAKE_TYPES.append(self)
        elif st == SubtypeOfStep.MISTAKE:
            MISTAKE_TYPES.append(self)
        elif st == SubtypeOfStep.NONSTANDARD:
            NS_TYPES.append(self)
            if (self.__name__ == 'NS_0') or (self.__name__ == 'NS_1'):
                HAPPY_TYPES.append(self)
        elif st == SubtypeOfStep.MISTAKE_NS:
            MISTAKE_NS_TYPES.append(self)
        elif st in {SubtypeOfStep.DIALOG,   SubtypeOfStep.DEMO,
                    SubtypeOfStep.MODIFIED, SubtypeOfStep.UNDEFINED}:
            "Nedělá se nic"
        elif st == SubtypeOfStep.SUCCESS:
            HAPPY_TYPES.append(self)
        elif st == SubtypeOfStep.HELP:
            BASIC_TYPES.append(self)
        else:
            raise Exception(f'Neznámý podtyp kroku: {self} -> {st=}')



############################################################################

ALL_TYPES        = []  # Seznam všech definovaných typů kroků
BASIC_TYPES      = []  # Seznam povinných typů kroků
NS_TYPES         = []  # Základní typy nadstandardních (ns) akcí
HAPPY_TYPES      = []  # Seznam typů kroků povinných ve scénáři HAPPY
MISTAKE_TYPES    = []  # Seznam typů kroků povinných ve scénáři MISTAKE
MISTAKE_NS_TYPES = []  # Seznam typů kroků povinných ve scénáři MISTAKE_NS


def print_step_types():
    """Vytiskne povinné typy kroků roztříděné podle cílových scénářů.
    """
    _print_tuple(HAPPY_TYPES, 'HAPPY')
    _print_tuple(MISTAKE_TYPES, 'MISTAKE')
    _print_tuple(MISTAKE_NS_TYPES, 'MISTAKE_NS')


def _print_tuple(types:tuple, description:str):
    """Vytiskne popisek následovaný prvky zadané n-tice
    každý na samostatný řádek.
    """
    print(f'Typy kroků povinně přítomné ve scénáři {description}')
    for t in types:
        print(f'   {str(t):16s} - {t.__doc__}')



############################################################################

#Typ kroku neurčeného pro zařazení do nějakého scénáře,
#ale pouze pro doplnění chybového hlášení a pomocné akce
tsNOT_SET         =TypeOfStep(8, -1, None, 'tsNOT_SET',
                  "Typ kroku pro chybová hlášení a pomocné akce")

#Typy řádných kroků, které se musí objevit v základním úspěšném scénáři
tsSTART           =TypeOfStep(0, -1, None, 'tsSTART',
                  "Startovací krok s prázdným názvem")
tsGOTO            =TypeOfStep(0, 1, None, 'tsGOTO',
                  "Úspěšný přesun do sousedního prostoru")
tsTAKE            =TypeOfStep(0, 1, None, 'tsTAKE',
                  "Úspěšné zvednutí objektu v prostoru")
tsPUT_DOWN        =TypeOfStep(0, 1, None, 'tsPUT_DOWN',
                  "Úspěšné položení objektu z batohu")
tsSUCCESS         =TypeOfStep(9, 0, None, 'tsSUCCESS',
                  "Úspěšné ukončení hry", True)

#Následující typy kroků musí být otestovány v základním chybovém scénáři
tsEND             =TypeOfStep(1, 0, None, 'tsEND',
                  "Příkaz okamžitě ukončující hru")
tsHELP            =TypeOfStep(10,0, None, 'tsHELP',
                  "Nápověda")

#Problémy s předčasně zadaným korektním ukončením
tsNOT_SUCCESS     = TypeOfStep(4, 0, tsSUCCESS, 'tsNOT_SUCCESS',
                  "Neúspěšný pokus o úspěšné ukončení hry")

#Problémy se správným zadáním příkazu
tsNOT_START       = TypeOfStep(2, -1, None, 'tsNOT_START',
                  "Startovací příkaz není prázdný string")
tsEMPTY           = TypeOfStep(2, -1, tsSTART, 'tsEMPTY',
                  "NE-startovací zadání prázdného stringu")
tsUNKNOWN         = TypeOfStep(2, -1, None, 'tsUNKNOWN',
                  "Zadání neznámé akce")

#Vyvolání některé ze základních akcí bez povinného parametru
tsGOTO_WA         = \
tsMOVE_WA         = TypeOfStep(2, 0, tsGOTO, 'tsMOVE_WA',
                  "Nebylo zadáno, kam se přesunout")
tsTAKE_WA         = TypeOfStep(2, 0, tsTAKE, 'tsTAKE_WA',
                  "Nebylo zadáno, co se má zvednout")
tsPUT_DOWN_WA     = TypeOfStep(2, 0, tsPUT_DOWN, 'tsPUT_DOWN_WA',
                  "Nebylo zadáno, co se má položit")

#Problémy se změnou místnosti
tsBAD_NEIGHBOR    = TypeOfStep(2, 1, tsGOTO, 'tsBAD_NEIGHBOR',
                  "Cílový prostor není sousedem aktuálního")

#Problémy se zvednutím či položením předmětu
tsBAD_ITEM        = TypeOfStep(2, 1, tsTAKE, 'tsBAD_ITEM',
                  "Zadaný předmět v prostoru není")
tsUNMOVABLE       = TypeOfStep(2, 1, tsTAKE, 'tsUNMOVABLE',
                  "Zadaný předmět nelze zvednout")
tsBAG_FULL        = TypeOfStep(2, 1, tsTAKE, 'tsBAG_FULL',
                  "Zadaný předmět se nevejde do batohu")
tsNOT_IN_BAG      = TypeOfStep(2, 1, tsPUT_DOWN, 'tsNOT_IN_BAG',
                  "Zadaný předmět v batohu není")

#Typy kroků korektně aktivujících pomocné akce
tsNS_0            = TypeOfStep(3, 0, None, 'tsNS_0',
                  "Úspěšná bezparametrická pomocná akce")
tsNS_1            = TypeOfStep(3, 1, None, 'tsNS_1',
                  "Úspěšná jednoparametrická pomocná akce")
tsNS_2            = TypeOfStep(3, 2, None, 'tsNS_2',
                  "Úspěšná dvouparametrická pomocná akce")
tsNS_3            = TypeOfStep(3, 3, None, 'tsNS_3',
                  "Úspěšná tříparametrická pomocná akce")

#Kroky testující reakci na chybně zadané pomocné akce
tsNS0_WrongCond   = TypeOfStep(4, 0, tsNS_0, 'tsNS0_WrongCond',
                  "Neproveditelná bezparametrická pomocná akce")
tsNS1_WrongCond   = TypeOfStep(4, 1, tsNS_1, 'tsNS1_WrongCond',
                  "Neproveditelná jednoparametrická pomocná akce")
tsNS2_WrongCond   = TypeOfStep(4, 2, tsNS_2, 'tsNS2_WrongCond',
                  "Neproveditelná dvouparametrická pomocná akce")
tsNS3_WrongCond   = TypeOfStep(4, 2, tsNS_3, 'tsNS3_WrongCond',
                  "Neproveditelná tříparametrická pomocná akce")
tsNS1_0Args       = TypeOfStep(4, 0, tsNS_1, 'tsNS1_0Args',
        "Jednoparametrická pomocná akce s nezadaným argumentem")
tsNS2_1Args       = TypeOfStep(4, 1, tsNS_2, 'tsNS2_1Args',
        "Dvouparametrická pomocná akce s malým počtem zadaných argumentů")
tsNS3_012Args     = TypeOfStep(4, 2, tsNS_3, 'tsNS3_012Args',
        "Tříparametrická pomocná akce s malým počtem zadaných argumentů")
# Test špatných argumentů byl zaměněn za test nesplněných podmínek
# Požadavky na argumenty se budou zadávat do podmínek
# tsNS1_WRONG_ARG   = TypeOfStep(4, 1, tsNS_1, 'tsNS1_WRONG_ARG',
#         "Jednoparametrická pomocná akce se špatným argumentem")
# tsNS2_WRONG_1stARG= TypeOfStep(4, 2, tsNS_2, 'tsNS2_WRONG_1stARG',
#         "Dvouparametrická pomocná akce s nevhodným prvním argumentem")
# tsNS2_WRONG_2ndARG= TypeOfStep(4, 2, tsNS_2, 'tsNS2_WRONG_2ndARG',
#         "Dvouparametrická pomocná akce s nevhodným druhým argumentem")
# tsNS3_WRONG_1stARG= TypeOfStep(4, 3, tsNS_3, 'tsNS3_WRONG_1stARG',
#         "Tříparametrická pomocná akce s nevhodným prvním argumentem")
# tsNS3_WRONG_2ndARG= TypeOfStep(4, 3, tsNS_3, 'tsNS3_WRONG_2ndARG',
#         "Tříparametrická pomocná akce s nevhodným druhým argumentem")
# tsNS3_WRONG_3rdARG= TypeOfStep(4, 3, tsNS_3, 'tsNS3_WRONG_3rdARG',
#         "Tříparametrická pomocná akce s nevhodným třetím argumentem")

#Typy kroku nepoužitelných pro testování reakce hry na zadaný příkaz
tsDIALOG          =TypeOfStep(5, -1, None, 'tsDIALOG',
        "Krok je součástí rozhovoru nebo nějaké obdobné činnosti")
tsDEMO            =TypeOfStep(6, -1, None, 'tsDEMO',
        "Netestovatelný krok určený pouze pro předvedení funkce hry")

#Typy kroku používané v modifikačních zadáních při obhajobách
tsMOD_A           =TypeOfStep(7, -1, None, 'tsMOD_A',
        "Modifikační krok používaný při obhajobách")
tsMOD_B           =TypeOfStep(7, -1, None, 'tsMOD_B',
        "Modifikační krok používaný při obhajobách")
tsMOD_C           =TypeOfStep(7, -1, None, 'tsMOD_C',
        "Modifikační krok používaný při obhajobách")



############################################################################

# N-tice n-tic obsahujících podmínky, které je třeba prověřit
# u pomocných akcí s příslušným počtem parametrů
_required_ns_err = (
        (tsNS0_WrongCond, ),
        (tsNS1_WrongCond, tsNS1_0Args),  # tsNS1_WRONG_ARG),
        (tsNS2_WrongCond, tsNS2_1Args),  # tsNS2_WRONG_1stARG,
                                         # tsNS2_WRONG_2ndARG),
        (tsNS3_WrongCond, tsNS3_012Args),# tsNS3_WRONG_1stARG,
                      #tsNS3_WRONG_2ndARG, tsNS3_WRONG_3rdARG)
)



############################################################################
# HAPPY_TYPES.remove(tsNS_3)

#Množiny typů kroků povinně použitých v různých typech scénářů
ALL_TYPES        = frozenset(ALL_TYPES)     # Všechny typy
BASIC_TYPES      = frozenset(BASIC_TYPES)   # Povinné akce
NS_TYPES         = frozenset(NS_TYPES)      # Základní typy ns akcí
HAPPY_TYPES      = frozenset(HAPPY_TYPES)   # Povinné ve šťastném scénáři
MISTAKE_TYPES    = frozenset(MISTAKE_TYPES) # Povinné v chybovém scénáři
MISTAKE_NS_TYPES = frozenset(MISTAKE_NS_TYPES)#Povinné v chybovém NS scénáři



############################################################################
dbg.stop_mod(2, __name__)
