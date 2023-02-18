import json
from datetime import date

PATH = "schedule.json"

ERROR_MSG = "!when [set] <day_name> <time> / !when [get] <day_name>"
HELP_MSG = "To find out when we playing type: '!when'"

def get_timetable() -> dict[ str, str ]:
    with open( PATH, "r" ) as f:
        return json.load( f )

def store_timetable( timetable: dict[ str, str ] ) -> None:
    with open( PATH, "w" ) as f:
        json_str = json.dumps( timetable )
        f.write( json_str )

def set_playtime( day: str, when: str ) -> None:
    table = get_timetable( )
    table[ day ] = when
    store_timetable( table )

def get_playtime( day: str ) -> str:
    table = get_timetable( )
    return table[ day ]
