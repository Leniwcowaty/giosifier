import sys
import utils

try:
    import requests as r
    import json
except ImportError as e:
    sys.exit(f"Module {e.name} not found. Please install correct module.")

endpointUrl = "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/"

def main():
    config = utils.read_config()

    apiHeader = {"Authorization": config[2]["auth"]}
    try:
        pm10Response = json.loads(r.get(endpointUrl+config[0]["id"]).text)
        no2Response = json.loads(r.get(endpointUrl+config[1]["id"]).text)
    except ConnectionError:
        sys.exit("Connection error when trying to connect to API")

    pm10Status = utils.parse_response(pm10Response, config[0])
    no2Status = utils.parse_response(no2Response, config[1])

    if pm10Status["triggered"]:
        r.post(config[2]["url"], headers=apiHeader, data=pm10Status["message"])

    if no2Status["triggered"]: 
        r.post(config[2]["url"], headers=apiHeader, data=no2Status["message"])

main()
