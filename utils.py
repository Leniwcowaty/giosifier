import sys
try:
    import os
    import requests as r
    import json
    import yaml
except ImportError as e:
    sys.exit(f"Module {e.name} not found. Please install correct module.")

endpointUrl = "https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/"

def read_config():
    configPathLocal = os.path.expanduser('~/.config/giosifier/config.yaml')
    configPathGlobal = ('/etc/giosifier/config.yaml')
    try:
        with open(configPathLocal, 'r') as configFile:
            config = yaml.safe_load(configFile)
    except FileNotFoundError:
        try:
            with open(configPathGlobal, 'r') as configFile:
                config = yaml.safe_load(configFile)
        except FileNotFoundError as e:
            sys.exit(f"Config file not found: {e}")

    stationInfo = json.loads(r.get(endpointUrl+str(config["station"]["id"])).text)["Lista stanowisk pomiarowych dla podanej stacji"]
    sensors = {item["Wskaźnik - kod"]: item["Identyfikator stanowiska"] for item in stationInfo}

    try:
        pm10Config = {"name": "Pył PM10", "id": str(sensors["PM10"]), "alert": config["pm10"]["alert"]}
        no2Config = {"name": "Dwutlenek azotu (NO2)", "id": str(sensors["NO2"]), "alert": config["no2"]["alert"]}
    except KeyError as e:
        sys.exit(f"This station does not have {e} sensor")
    
    try:
        nftyConfig = {"url": config["ntfy"]["url"], "auth": config["ntfy"]["auth"]}
    except KeyError:
        nftyConfig = {"url": config["ntfy"]["url"], "auth": None}

    configList = [pm10Config, no2Config, nftyConfig]

    return configList
    
def parse_response(json, obj):
    level = json["Lista danych pomiarowych"][0]["Wartość"]
    station = json["Lista danych pomiarowych"][0]["Kod stanowiska"]
    measurement = json["Lista danych pomiarowych"][0]["Data"]
    if level > obj["alert"]:
        body = "Stacja \"" + station + "\": Poziom " + obj["name"] + " za wysoki! Wartość: " + str(level) + " (data pomiaru: " + measurement + ")\n"
        result = {"message": body, "triggered": True}
    else:
        result = {"message": None, "triggered": False}
    return result