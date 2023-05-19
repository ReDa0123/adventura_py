#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#P:/p1_INP/game23s/tests/visitor/vma_notentered.py
"""
Modul definuje třídu `Visitor_NotEntered`, jejíž instance testují
správné zapracování modifikace požadující následující úpravu
původního programu:

Na konec každé zprávy vypisované jako odpověď hry na zadání příkazu
přidat řádek s textem:

§Dosud nezadáno: [name1, name2, name3, ..., namen]

kde v hranatých závorkách bude uveden abecedně seřazený seznam
čárkami oddělených a na malá písmena převedených názvů akcí,
které hráč během aktuální hry ještě nezadal.
Názvy name1, name2 atd. ve výše  uvedeném textu
zastupují na malá písmena převedené názvy akcí testované hry.
"""
import dbg; dbg.start_mod(2, __name__)
###########################################################################q

from game23s.api.interfaces        import IPortal, IGame, INamed
from game23s.api.scenario          import Scenario, ScenarioStep
from game23s.tests                 import Level, test_scenario
from game23s.tests.common.errors   import error
from game23s.tests.common.texts    import *
from game23s.tests.common.utils    import containers_differs
from game23s.tests.visitor         import Visitor



###########################################################################q

class Visitor_NotEntered(Visitor):
    """
    Třída návštěvníků kontrolujících modifikaci původní hry
    pomáhá kontrolovat správnost řešení popsaného v dokumentaci modulu.
    """

    def __init__(self, portal:IPortal, level:Level):
        super().__init__(portal, level)
        self.not_entered = []


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
        Cílem metody je připravit potřebné informace o testované hře.
        
        :param scenario: Scénář, podle nějž se hra testuje
        """
        # @dbg.prSEda()
        def verify_no_ck(*modules):
            """Prověří, že názvy zadaných modulů nezačínají 'ck_'.
            """
            CK = 'ck_'
            for module in modules:
                if module.__name__.lower().startswith(CK):
                    reason = 'Názvy modulů nebyly zbaveny předpony `ck_`'
                    print(f'\n{N_EXCLAM_N}CHYBA:\n{reason}{N_EXCLAM_N}')
                    raise Exception(f'{reason}')

        super().after_game_start(scenario)
        # Porovná úvodní hlášení hry se situací odvozenou ze scénářů
        if len(self.portal.AUTHOR_ID) > 4:  # Ne pro demonstrační programy
            verify_no_ck(self.game, self.game.world())
        sne = [action.name.lower() for action in self.game.all_actions()]
        sne.sort()
        self.not_entered = sne


    def before_entering_command(self, step:ScenarioStep) -> None:
        """
        Akce, která se má provést před zadáním příkazu hře.
        Používá se zřídka. Při její definici je třeba vzít v úvahu, že se
        u startovacího kroku provede ještě před odstartováním hry,
        tj. před metodami `before_game_start` a `after_game_start`.

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


    # @dbg.prSEd()
    def after_step_test(self, step:ScenarioStep, answer:str) -> None:
        """
        Akce, která se má provést po testu aktuálního kroku.
        
        :param step:   Aktuálně prověřovaný krok scénáře
        :param answer: Odpověď hry na zadání příkazu
        """
        command = step.command.strip()
        if command:
            words   = command.split()
            action  = words[0].lower()
            if action in self.not_entered:
                self.not_entered.remove(action)
        requested = f'§Dosud nezadáno: {self.not_entered}'
        
        def err(reason:str) -> None:
            error(reason, self.scenario, step, self.game,
                  f'{step.message}\n{requested}', answer)

        parts = answer.split('§')
        if len(parts) < 2:
            err('Chybí požadovaný závěrečný řádek')
        if len(parts) > 2:
            err('Nečekaný znak § v obdržené odpovědi hry')
        obtained = answer.splitlines()
        ####################################################################
        if not (requested == obtained[-1]):
            err('Závěrečný řádek nemá požadovaný tvar')


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
dbg.stop_mod(2, __name__)
