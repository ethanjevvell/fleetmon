import pandas as pd
import datetime as dt


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


todays_date = str(dt.date.today())
all_nampho_vessel_names_set = set(
    ['ETHANS BOAT'])

master_port_tracker = pd.read_csv(
    '/Users/ethanjewell/Desktop/Python Env/Scripting/FleetMon/fleetmon/fleetmon/master_port_tracker.csv')

if not master_port_tracker['Date'].eq(f'{todays_date}').any():
    all_nampho_vessel_names_set = formatForSheet(all_nampho_vessel_names_set)

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
    '/Users/ethanjewell/Desktop/Python Env/Scripting/FleetMon/fleetmon/fleetmon/master_port_tracker.csv', index=False)
