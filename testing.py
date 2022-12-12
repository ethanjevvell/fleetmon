import pandas as pd
import datetime as dt

todays_date = str(dt.date.today())
all_nampho_vessel_names_set = set(['b'])

master_port_tracker = pd.read_csv(
    '/Users/ethanjewell/Desktop/Python Env/Scripting/FleetMon/fleetmon/fleetmon/master_port_tracker.csv')

if not master_port_tracker['Date'].eq(f'{todays_date}').any():
    new_row = pd.DataFrame(
        {'Date': [str(dt.date.today())], 'Nampho': all_nampho_vessel_names_set})
    master_port_tracker = pd.concat([master_port_tracker, new_row])

else:
    sheet_vessels = str(master_port_tracker[master_port_tracker['Date']
                                            == todays_date]['Nampho'].values)

    sheet_vessels = sheet_vessels.replace('[', '')
    sheet_vessels = sheet_vessels.replace(']', '')
    sheet_vessels = sheet_vessels.replace('\'', '')
    sheet_vessels = sheet_vessels.replace(' ', '')
    sheet_vessels = sheet_vessels.split(',')

    sheet_vessels = set(sheet_vessels)

    sheet_vessels.update(all_nampho_vessel_names_set)

    master_port_tracker.loc[master_port_tracker['Date']
                            == todays_date, 'Nampho'] = sheet_vessels

master_port_tracker.to_csv(
    '/Users/ethanjewell/Desktop/Python Env/Scripting/FleetMon/fleetmon/fleetmon/master_port_tracker.csv', index=False)
