import requests

HELP_MSG = "!nameday <country> <day> <month>\n If parameters are not provided, gives today's name Slovakia"

def get_nameday(country_code: str, day: int=None, month: int=None) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"country": country_code}
    if day is not None:
        params["day"] = day
    if month is not None:
        params["month"] = month

    tp = "today" if day is None else "getdate"
    response = requests.get(f"https://nameday.abalin.net/api/V1/{tp}", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["nameday"][country_code]
    else:
        return "Something went wrong on the network :(("
