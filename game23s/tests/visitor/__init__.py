#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/tests/visitor/__init__.py
"""
Balíček návštěvníků, přičemž v initoru balíčku je definována
třída `Visitor`, která je jejich společným rodičem.
"""
import dbg; dbg.start_pkg(2, __name__, __doc__)
###########################################################################q

from ...api.scenario    import ScenarioStep, Scenario
from ...api.interfaces  import IPortal, IGame
from  ..                import Level, test_scenario
from  ..common.utils    import containers_differs
from  ..common.errors   import error



############################################################################

class Visitor:
    """
    Společný rodič tříd návštěvníků testů.
    Definuje sadu funkcí požadovaných od návštěvníka testů
    schopných ovlivnit způsob testování hry podle jimi známých dispozic.

    Slouží především k tomu, aby bylo možno doplnit základní testy
    o doplňkové kontroly prověřující, zda byly správně zapracovány
    všechny úpravy vyžadované při obhajobách aplikace.

    Třída definuje všechny metody návštěvníka jako prázdné s tím,
    že pro každé zadání požadované modifikace pro obhajobu
    bude definován odpovídající potomek kontrolující správnost řešení.
    """

    def __init__(self, portal:IPortal, level:Level):
        self.portal = portal
        self.level  = level
        try:
            self.game:IGame = portal.GAME()
        except:
            raise Exception(f'\nPortál nedodal hru k testování.')


    @staticmethod
    def are_imperfect_scenarios_allowed(self) -> None:
        """Vrátí informaci o tom, je-li v prověřovaném zadání povoleno
        testování hry i v případě, kdy správce scénářů neprojde verifikací.
        """
        return False


    def before_game_start(self, scenario:Scenario) -> None:
        """
        Akce, která se má provést před spuštěním hry.
        Cílem metody je prověřit scénáře a případné další pomocné kódy.

        :param scenario: Scénář, podle nějž se hra testuje
        """
        self.scenario = scenario


    # @dbg.prSEda()
    def after_game_start(self, scenario:Scenario) -> None:
        """
        Akce, která se má provést po provedení startovacího kroku hry
        (tj. ve chvíli, kde je hra již inicializována), ale před jeho testem,
        tj. před ověřením, že stav hry odpovídá scénáři.
        TODO Prověří, že hra deklaruje právě ty akce, které jsou deklarované
        TODO ve scénářích a uloží seznam jejich abecedně seřazených názvů.
        Cílem metody je připravit potřebné informace o testované hře.
        
        :param scenario: Scénář, podle nějž se hra testuje
        """


    def before_entering_command(self, step:ScenarioStep) -> None:
        """
        Akce, která se má provést před zadáním příkazu hře.
        Používá se zřídka. Při její definici je třeba vzít v úvahu, že se
        u startovacího kroku provede ještě před odstartováním hry,
        tj. před metodou `after_game_start`.

        :param step: Aktuálně prověřovaný krok scénáře
        :return: Aktuálně prověřovaný krok scénáře
        """


    def before_step_test(self, step:ScenarioStep, answer:str) -> None:
        """
        Akce, která se má provést po provedení kroku hry, ale před jeho
        testem, tj. před ověřením, že stav hry odpovídá scénáři.
        
        :param step:    Aktuálně prověřovaný krok scénáře
        :param answer:  Odpověď hry na zadání příkazu
        """


    def after_step_test(self, step:ScenarioStep, answer:str) -> None:
        """
        Akce, která se má provést po testu aktuálního kroku.
        :param step:   Aktuálně prověřovaný krok scénáře
        :param answer: Odpověď hry na zadání příkazu
        """


    def after_game_end(self, verbose_message:str='',
              exception:Exception=None, summary:'GameSummary'=None) -> None:
        """
        Akce, která se má provést po testu posledního kroku.
        
        :param verbose_message: Kompletní zpráva o průběhu testu
        :param exception:       Případná vyhazovaná výjimka
        :param summary:         Přepravka s informacemi o předpokládaném
                                průběhu hry podle scénářů
        """


    def __repr__(self) -> str:
        """
        Systémový podpis instance -- vrátí název třídy
        a autora testované aplikace.
        """
        return f'{self.__class__.__module__}.{self.__class__.__name__}(' \
               f'{self.portal.__name__})'



###########################################################################q
dbg.stop_pkg(2, __name__)
