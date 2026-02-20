try:
    import sys
except ModuleNotFoundError:
    print("Module sys is not installed")

try:
    import os
except ModuleNotFoundError:
    print("Module os is not installed")

try:
    import requests as r
except ModuleNotFoundError:
    print("Module requests is not installed")

try:
    import json
except ModuleNotFoundError:
    print("Module json is not installed")

try:
    import yaml
except ModuleNotFoundError:
    print("Module yaml is not installed")

endpointUrl = "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/"

def read_config():
    configPath = os.path.expanduser('~/.config/giosifier/config.yaml')
    try:
        with open(configPath, 'r') as configFile:
            config = yaml.safe_load(configFile)
    except FileNotFoundError:
        sys.exit(f"Config file not found in {configPath}")

    pm10Config = {"name": "Pył PM10", "id": config["pm10"]["sensor_id"], "alert": config["pm10"]["alert"]}
    no2Config = {"name": "Pył PM10", "id": config["no2"]["sensor_id"], "alert": config["no2"]["alert"]}
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

def main():
    config = read_config()

    apiHeader = {"Authorization": config[2]["auth"]}
    try:
        pm10Response = json.loads(r.get(endpointUrl+config[0]["id"]).text)
        no2Response = json.loads(r.get(endpointUrl+config[1]["id"]).text)
    except ConnectionError:
        sys.exit("Connection error when trying to connect to API")

    pm10Status = parse_response(pm10Response, config[0])
    no2Status = parse_response(no2Response, config[1])

    if pm10Status["triggered"]:
        r.post(config[2]["url"], headers=apiHeader, data=pm10Status["message"])

    if no2Status["triggered"]: 
        r.post(config[2]["url"], headers=apiHeader, data=no2Status["message"])

main()
