

''' -------------------------------------------- USER INTERFACE --------------------------------------------'''
# Here you can choose some of the settings that are important to the analysis in the thesis


''' ----------------------------------------------- SETTINGS -----------------------------------------------'''


# File path
file_path = "Excel/original.xlsx"

# Excel sheet names
scenarios = {'Only RES': 'Renewable',
             '1GW Nuclear': 'Nuclear_flex',
             '1GW Nuclear w/ DH': 'Nuclear_flex_dh',
             '3GW Nuclear':'3GW',
             '3GW Nuclear w/ DH':'3GW_dh',
             'High Nuclear': 'Nuclear',
             'High Nuclear w/ DH': 'Nuclear_dh'}


# Set name of output file
output_file = "output"

# manually set the nuclear, offshore and onshore wind sizes because they are not in the excel results sheet
nuc_size = {'Only RES': 0, '1GW Nuclear': 1000, '1GW Nuclear w/ DH': 1000, '3GW Nuclear': 3000, '3GW Nuclear w/ DH': 3000,
            'High Nuclear': 7521, 'High Nuclear w/ DH': 7581}

offshore_size = {'Only RES': 14075, '1GW Nuclear': 12560, '1GW Nuclear w/ DH': 12735, '3GW Nuclear': 9300,
                 '3GW Nuclear w/ DH': 9300, 'High Nuclear': 2306, 'High Nuclear w/ DH': 2306}

onshore_size = {'Only RES': 5000, '1GW Nuclear': 5000, '1GW Nuclear w/ DH': 5000, '3GW Nuclear': 5000,
                '3GW Nuclear w/ DH': 5000, 'High Nuclear': 4689, 'High Nuclear w/ DH': 4689}

pv_size = {'Only RES': 10000, '1GW Nuclear': 10000, '1GW Nuclear w/ DH': 10000, '3GW Nuclear': 10000,
                '3GW Nuclear w/ DH': 10000, 'High Nuclear': 2000, 'High Nuclear w/ DH': 2000}
# Original capacity factors
offshore_CF_original = 0.51
onshore_CF_original = 0.37
PV_CF_original = 0.14

# True if you want to see how much capacity and costs change when capacity factor change
change_cf = False

# Set new CF values (optional)
offshore_CF = 0.40
onshore_CF = 0.26
PV_CF = 0.11

# Constants
ir = 0.03
lifetime_nuc = 60               # years
lifetime_off = 30               # years
lifetime_on = 30                # years
uranium_cost = 9.33             # MEUR / TWh = EUR / MWh
OM_nuc = 14.26                  # MEUR / MWh
OM_offshore_2035 = 36000        # EUR/ MW / year

''' --------------------------------------------------------------------------------------------------------'''

def settings():
    return (file_path, scenarios, output_file, nuc_size, offshore_size, onshore_size, pv_size,
            change_cf, offshore_CF_original, onshore_CF_original, PV_CF_original,
            offshore_CF, onshore_CF, PV_CF,
            ir, lifetime_nuc, lifetime_off, lifetime_on, uranium_cost, OM_nuc, OM_offshore_2035)

def get_file_path():
    return file_path

def get_scensrios():
    return scenarios

def get_nuc_size():
    return nuc_size

def get_offwind_size():
    return offshore_size

def get_onwind_size():
    return onshore_size

def get_dh_scenarios():
    scenarios = {'Only RES': 'Renewable',
                 '1GW Nuclear w/ DH': 'Nuclear_flex_dh',
                 '3GW Nuclear w/ DH': '3GW_dh',
                 'High Nuclear w/ DH': 'Nuclear_dh'}
    return scenarios