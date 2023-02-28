import json
from datetime import date

SHOP_PATH = "shop.txt"

def fetch() -> list[ str ]:
    with open( SHOP_PATH, "r" ) as f:
        lines = f.read().split( "\n" )
        if lines[ -1 ] == "":
            lines = lines[:-1]

        return lines

def reset() -> None:
    with open( SHOP_PATH, "w" ) as f:
        f.write("")

def rewrite( lst: list[ str ] ) -> None:
    
    with open( SHOP_PATH, "w" ) as f:
        for ln in lst:
            f.write( f"{ln}\n" )

def remove_nth( n: int ) -> None:
    lst = fetch()

    if n >= len( lst ):
        return

    lst.pop( n )
    rewrite( lst )

def push( item: str ) -> None:
    with open( SHOP_PATH, "a" ) as f:
        f.write( f"{item}\n" )
