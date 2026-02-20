# GIOSifier - poor air quality notifier for Polish people
---
## TL;DR
This simple Python application utilizes GIOŚ (Główny Inspektorat Ochrony Środowiska) API to collect info about PM10 and NO2 levels in measuring station near you, then if these levels are too high sends a notification utilizing Ntfy app (either to public Ntfy instance, or private self-hosted one).

## Installation
There are two ways to install GIOSifier:

### Manual installation
If you want to read the code and execute actual .py file
1. Clone the repository
2. Install python3 and needed modules (either through pip or from your distro's repositories):
    * sys
    * os
    * yaml
    * json
    * requests
3. [Configure the app](#configuration)
4. Run with `python3 main.py`

### "Single binary" installation
If you want to just execute the binary without the need to install dependencies or python
1. Download [latest release](https://github.com/Leniwcowaty/giosifier/releases)
2. Place it somewhere on your system (preferably where you've added it to the $PATH)
3. Run the `giosifier` binary

*The binary is built with pyinstaller on Python 3.13*

## Configuration
The program is configured with a simple `config.yaml` file. It looks for the config file in following locations (in this order):
1. `~/.config/giosifier/config.yaml`
2. `/etc/giosifier/config.yaml`

The config file must be manually placed in one of these locations, and ensured whatever user you run this program as has at **READ** rights to it.

### Filling in the config file
You can download example config file from the repository [HERE](https://raw.githubusercontent.com/Leniwcowaty/giosifier/refs/heads/main/config_template.yaml).

To configure GIOSifier you will need two (optionally up to five) informations:
1. Station ID of measuring station in your area
2. Ntfy request URL
3. (optional) Authentication method string for custom Ntfy server
4. (optional) Custom alert level for PM10
5. (optional) Custom alert level for NO2

The config template file is well documented and tells you where to put what.

### Obtaining station ID
To obtain the ID of the station you want to monitor go to GIOŚ website with current measurements [HERE](https://powietrze.gios.gov.pl/pjp/current), and select station closest to you. Click on it and click on "Więcej informacji" ("More info"). You will be redirected to the page for this station. In its URL it will have the station ID. Eg. for Warsaw, Solidarności the URL is: https://powietrze.gios.gov.pl/pjp/current/station_details/info/20488, then the Station ID you need to place in the config is "20488" as a string.

On the general info page of the station you will also have the list of sensors this station has. Ensure it has PM10 and NO2 sensors, if not the program will exit with error (TBD implementing more sensors and modular system).

The default values for alerts are taken from https://powietrze.gios.gov.pl/pjp/content/annual_assessment_air_acceptable_level.

## Running the application on a schedule
You can either just create a cron to run this application every hour (since the sensors typically refresh hourly), or be a fancypants and create a systemd service or something. Up to you.

---

# Closing notes
This is my hobby project, expect breakages and stuff not working correctly. It works fine for me on my RISC-V devboard. I will probably develop this in free time. Feel free to submit issues and pull requests if you want to contribute. 