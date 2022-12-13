import pandas as pd
import datetime as dt


def makeList(raw):
    raw = raw.replace('[', '')
    raw = raw.replace(']', '')
    raw = raw.replace('\'', '')
    raw = raw.replace(' ', '')
    raw = raw.split(',')
    return set(raw)


def formatForSheet(raw):
    raw = str(raw)
    raw = raw.replace('{', '')
    raw = raw.replace('}', '')
    raw = raw.replace('\'', '')
    return str(raw)


todays_date = str(dt.date.today())
all_nampho_vessel_names_set = set(['B'])

master_port_tracker = pd.read_csv(
    '/Users/ethanjewell/Desktop/Python Env/Scripting/FleetMon/fleetmon/fleetmon/master_port_tracker.csv')

if not master_port_tracker['Date'].eq(f'{todays_date}').any():
    new_row = pd.DataFrame(
        {'Date': [str(dt.date.today())], 'Nampho': str(all_nampho_vessel_names_set)})
    master_port_tracker = pd.concat([master_port_tracker, new_row])

else:
    sheet_vessels = str(master_port_tracker[master_port_tracker['Date']
                                            == todays_date]['Nampho'].values)

    sheet_vessels = makeList(sheet_vessels)

    print(f'Old vessels: {sheet_vessels}')
    print(f'All nampho vessels: {all_nampho_vessel_names_set}')

    sheet_vessels.update(all_nampho_vessel_names_set)

    print(f'Updated set: {sheet_vessels}')

    sheet_vessels = formatForSheet(sheet_vessels)

    print(f'Attempt at making new set to string: {sheet_vessels}')
    master_port_tracker.loc[master_port_tracker['Date']
                            == todays_date, 'Nampho'] = sheet_vessels

    print(master_port_tracker)

master_port_tracker.to_csv(
    '/Users/ethanjewell/Desktop/Python Env/Scripting/FleetMon/fleetmon/fleetmon/master_port_tracker.csv', index=False)
