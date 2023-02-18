import random

HELP_MSG = "!pick *[ items ]"
EMPTY_ERR = "Empty sequence provided!"

def pick( pool: list[ str ] ) -> str:
    return random.choice( pool )
