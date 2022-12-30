
import requests
import json
import argparse
import yagmail
import pandas as pd
import datetime as dt

# Global API key
API_KEY = "802af00e5d74070c90c5a3c49c1e5b59"
OUT_PATH = '/home/scripts/fleetmon/master_port_tracker.csv'
FLEET = '/home/scripts/fleetmon/fleet.txt'


def sendAlert(content):  # Sends an email with given content

    user = yagmail.SMTP(user='nknews.thermalradar@gmail.com',
                        password='pknzhwayprlenjyi')
    user.send(to='ethan.jewell@nknews.org',
                 subject='[SHIP ALERT] - New vessel detected in Nampho',
                 contents=content)


def getFleet():
    URL = f"https://apiv2.fleetmon.com/myfleet/?apikey={API_KEY}"

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(URL, headers=headers)
    response_text = response.text

    return response_text


def getVessel(vessel_id):
    URL = f"https://apiv2.fleetmon.com/myfleet/{vessel_id}"

    headers = {
        "Accept": "application/json",
        "Api-Key": API_KEY
    }

    response = requests.get(URL, headers=headers)
    response_json = response.json()

    return response_json


def makeList(raw):
    raw = raw.replace('[', '')
    raw = raw.replace(']', '')
    raw = raw.replace('\'', '')
    raw = raw.split(',')
    raw = [ves.strip(' ') for ves in raw]

    # If this is the first time we're creating an entry for a given day, .split() will generate 'nan', which should be removed.
    if raw.count('nan') > 0:
        raw.remove('nan')

    print(f'List after makeList: {set(raw)}')
    return set(raw)


def formatForSheet(raw):
    raw = str(raw)
    raw = raw.replace('{', '')
    raw = raw.replace('}', '')
    raw = raw.replace('\'', '')
    print(f'List after formatForSheet: {str(raw)}')
    return str(raw)


def updateNamphoRecords(vessel_list):

    todays_date = str(dt.date.today())
    all_nampho_vessel_names_set = set(vessel_list)

    master_port_tracker = pd.read_csv(
        OUT_PATH)

    if not master_port_tracker['Date'].eq(f'{todays_date}').any():
        all_nampho_vessel_names_set = formatForSheet(
            all_nampho_vessel_names_set)

        new_row = pd.DataFrame(
            {'Date': [str(dt.date.today())], 'Nampho': str(all_nampho_vessel_names_set)})
        master_port_tracker = pd.concat([master_port_tracker, new_row])
        print(str(all_nampho_vessel_names_set))

    else:
        sheet_vessels = str(master_port_tracker[master_port_tracker['Date']
                                                == todays_date]['Nampho'].values)
        sheet_vessels = makeList(sheet_vessels)
        sheet_vessels.update(all_nampho_vessel_names_set)
        sheet_vessels = formatForSheet(sheet_vessels)

        master_port_tracker.loc[master_port_tracker['Date']
                                == todays_date, 'Nampho'] = sheet_vessels

        print(master_port_tracker)

    master_port_tracker.to_csv(
        OUT_PATH, index=False)


def scanNampho():

    URL = "https://apiv2.fleetmon.com/regional_ais/"

    headers = {
        "Api-Key": API_KEY,
        "Accept": "application/json"
    }

    response = requests.get(URL, headers=headers)
    nampho_dict = response.json()

    print(nampho_dict)

    nampho_set = nampho_dict['vessels']
    nampho_set = [ves['name'] for ves in nampho_set]
    nampho_set = set(nampho_set)

    updateNamphoRecords(nampho_set)

    with open(FLEET) as f:
        fleet_text = f.read()

    vessel_dict = json.loads(fleet_text)

    all_vessels = vessel_dict["vessels"]
    nampho_vessels = nampho_dict["vessels"]

    all_vessel_names = [ves['name'] for ves in all_vessels]
    all_nampho_vessel_names = [ves['name'] for ves in nampho_vessels]

    all_vessel_imo_numbers = [ves['imo_number'] for ves in all_vessels]
    all_nampho_vessel_imo_numbers = [
        ves['imo_number'] for ves in nampho_vessels]

    all_vessel_mmsi_numbers = [ves['mmsi_number'] for ves in all_vessels]
    all_nampho_vessel_mmsi_numbers = [
        ves['mmsi_number'] for ves in nampho_vessels]

    # create sets of the names, IMO numbers, and MMSI numbers for all vessels and Nampho vessels
    all_vessel_names_set = set(all_vessel_names)
    all_nampho_vessel_names_set = set(all_nampho_vessel_names)
    all_vessel_imo_numbers_set = set(all_vessel_imo_numbers)
    all_nampho_vessel_imo_numbers_set = set(all_nampho_vessel_imo_numbers)
    all_vessel_mmsi_numbers_set = set(all_vessel_mmsi_numbers)
    all_nampho_vessel_mmsi_numbers_set = set(all_nampho_vessel_mmsi_numbers)

    # find any Nampho vessels that are not in the all vessels list by using the difference operator on the sets
    not_in_all_vessels_by_name = all_nampho_vessel_names_set - all_vessel_names_set
    not_in_all_vessels_by_imo_number = all_nampho_vessel_imo_numbers_set - \
        all_vessel_imo_numbers_set
    not_in_all_vessels_by_mmsi_number = all_nampho_vessel_mmsi_numbers_set - \
        all_vessel_mmsi_numbers_set

    # print the resulting sets to see the Nampho vessels that are not in the all vessels list
    if not_in_all_vessels_by_name or not_in_all_vessels_by_imo_number or not_in_all_vessels_by_mmsi_number:
        sendAlert(
            f'New ships likely detected. Names: {not_in_all_vessels_by_name}. IMO numbers: {not_in_all_vessels_by_imo_number}. MMSI numbers: {not_in_all_vessels_by_mmsi_number}')


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    parser.add_argument("--getFleet", action="store_true",
                        help="Returns NK News\" FleetMon fleet")
    parser.add_argument("--getVessel", type=int,
                        help="Returns NK News\" FleetMon fleet")
    parser.add_argument("--scanNampho", action="store_true",
                        help="Returns NK News\" FleetMon fleet")

    args = parser.parse_args()

    function_args = {
        args.getFleet: [],
        args.getVessel: [args.getVessel],
        args.scanNampho: []
    }

    # Update the function_mapping dictionary to include the delFleet function
    function_mapping = {
        args.getFleet: getFleet,
        args.getVessel: getVessel,
        args.scanNampho: scanNampho
    }

    # Iterate over the dictionary and call the functions with the appropriate arguments
    for arg_value, function in function_mapping.items():
        if arg_value:
            result = function(*function_args[arg_value])
            print(result)


if __name__ == "__main__":
    main()
