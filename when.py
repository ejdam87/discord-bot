import json
from datetime import date

PATH = "schedule.json"

def get_times( path: str ) -> dict[ str, str ]:
    with open( PATH, "r" ) as f:
        return json.load( f )


def get_time( weekday: int ) -> str:
    times = get_times( PATH )
    return times[ str( weekday ) ]

def get_time_today() -> int:
    return get_time( date.today().weekday() )
