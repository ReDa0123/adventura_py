#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Modul s často používanými texty.
"""
import dbg
dbg.start_mod(2, __name__)
############################################################################

MAX_LENGTH = 80

LENGTH = 70

BEFORE_ = LENGTH * 'V'
AFTER_  = LENGTH * 'A'
HASH_   = LENGTH * '#'
AMP_    = LENGTH * '@'
DOUBLE_ = LENGTH * '='
SINGLE_ = LENGTH * '-'
EXCLAM_ = LENGTH * '!'

N_BEFORE    = '\n' + BEFORE_
BEFORE_N    =        BEFORE_ + '\n'
N_BEFORE_N  = '\n' + BEFORE_ + '\n'

N_AFTER    = '\n' + AFTER_
AFTER_N    =        AFTER_ + '\n'
N_AFTER_N  = '\n' + AFTER_ + '\n'

N_HASH     = '\n' + HASH_
HASH_N     =        HASH_ + '\n'
N_HASH_N   = '\n' + HASH_ + '\n'

N_AMP      = '\n' + HASH_
AMP_N      =        HASH_ + '\n'
N_AMP_N    = '\n' + HASH_ + '\n'

N_DOUBLE   = '\n' + DOUBLE_
DOUBLE_N   =        DOUBLE_ + '\n'
N_DOUBLE_N = '\n' + DOUBLE_ + '\n'

N_SINGLE   = '\n' + SINGLE_
SINGLE_N   =        SINGLE_ + '\n'
N_SINGLE_N = '\n' + SINGLE_ + '\n'

N_EXCLAM   = '\n' + EXCLAM_
EXCLAM_N   =        EXCLAM_ + '\n'
N_EXCLAM_N = '\n' + EXCLAM_ + '\n'



############################################################################

def check_message_length(description:str, text:str) -> None:
    """Prověří délku řádků zadaného textu.
    Žádný řádek nesmí mít více než {@link #MAX_LINE_LENGTH} znaků.
    Tento test využívají testery scénářů spolu s testery běhu hry.
    """
    lines = text.splitlines()
    for line in lines:
        if len(line) > MAX_LENGTH:
            msg = (f'Délka řádku textu {description}\n'
                   f'je delší než povolených {MAX_LENGTH} znaků.')
            print(f'{N_BEFORE_N}{msg}{N_AFTER_N}')
            raise Exception(msg)



############################################################################
dbg.stop_mod(2, __name__)
