import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_imp_exp():
    scenarios = {'Only RES': 'Renewable', '1GW Nuclear': 'Nuclear_flex', '3GW Nuclear': '3GW', 'High Nuclear': 'Nuclear'}
    data_dict = {name: pd.read_csv(f'Data/{name}_timeseries.csv') for name, sheet in scenarios.items()}
    colors = ['#8FD7D7',  '#FF8CA1', '#BDD373','#FFB255']
    q = 0
    plt.figure(figsize = (12, 4))

    for name, data in data_dict.items():
        data.index = pd.date_range(start = '2045-01-01', periods = 8784, freq = 'h')

        # ---------------- Extract relevant data from csv file ----------------

        # Import
        imp = data['Discharge Electr.']
        # Export
        exp = data['Charge Electr.']

        weekly_data = pd.DataFrame({
            'import': imp,
            'export': exp,
        }).resample('D').mean()

        netto = []
        for i, val in enumerate(weekly_data['export']):
            netto.append(weekly_data['import'][i]- weekly_data['export'][i])

        # ------------------------------ PLOT -------------------------------


        # Plot demand
        plt.plot(netto, color = colors[q], label = name, linewidth=(6-q))

        q += 1

    plt.grid(True, linestyle='--', alpha=0.5, axis = 'y')
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Electricity import (MW)', fontsize=12)
    plt.legend(loc='upper center', labelspacing=3, bbox_to_anchor=(0.5, -0.2), ncol=4)
    plt.xlim(0,366)
    plt.subplots_adjust(bottom = 0.05)  # reserve more space below the plot  # or 0.35 if more space is needed
    plt.tight_layout()

    plt.show()


def plot_april():
    blues = sns.color_palette("Blues", desat = None, as_cmap = False)
    oragnes = sns.color_palette("Oranges", desat = None, as_cmap = False)

    linjetykkelse = 1.8

    file_path = 'Excel/Original.xlsx'
    # Excel sheet names
    scenarios = {'Only RES': 'Renewable', '1GW Nuclear': '1GW', '3GW Nuclear': '3GW', 'High Nuclear': 'Nuclear'}

    data_dict = {name: pd.read_csv(f'Data/{name}_timeseries.csv') for name, sheet in scenarios.items()}

    for name, data in data_dict.items():
        # ---------------- Extract relevant data from csv file ----------------

        # Supply
        nuclear = data['Nuclear Electr.']
        wind_onshore_el = data['Wind Electr.']
        wind_offshore_el = data['Offshore Electr.']
        pv_el = data['PV Electr.']
        wave_el = data['Wave Electr.']
        biogas = data['Biogas']
        waste = data['Waste 2 Heat'] + data['Waste 3 Heat']
        CHP = data['CHP Electr.'] + data['CSHP Electr.'] #+ data['CHP2+3']
        PP = data['PP Electr.'] + data['PP2 Electr.']
        renewable_el = wind_onshore_el.values + wind_offshore_el.values + pv_el.values + wave_el.values
        disch = data['Discharge Electr.']

        # Demand
        Unflexible = data['Electr. Demand'] #+ data['Elec.dem  Cooling']
        Heating = (data['HP Electr.'])
        #transport = data['H2 demand']
        v2g = data['Flexible Electr.'] + data['V2G Charge']
        electrolysis = data['H2 Electr.'] + data['CO2Hydro Electr.'] + data['NH3Hydro Electr.']
        storage = data['Charge Electr.']
        # ------------------------------ PLOT -------------------------------

        plt.figure(figsize=(25, 8))

        # Plot supply
        plt.stackplot(wind_onshore_el.index, nuclear, CHP, renewable_el, waste, PP, disch,
                      colors=blues,#['dimgray','cornflowerblue', 'limegreen', 'midnightblue', 'chocolate'],
                      labels = ['Nuclear power','Renewable electricity', 'Waste incineration', 'Power plants', 'CHP plants', "Storage"])

        # Plot demand
        plt.plot(Unflexible, color = oragnes[1], label = 'Unflexible demand', linewidth=linjetykkelse)
        plt.plot(Unflexible + Heating, color = oragnes[2], label = 'Electricity for heating', linewidth=linjetykkelse)
        plt.plot(Unflexible + Heating  + electrolysis, color = oragnes[3], label = 'Electricity for electrolysis', linewidth=linjetykkelse)
        plt.plot(Unflexible + Heating  + v2g + electrolysis, color = oragnes[4], label = 'Electricity for transport', linewidth=linjetykkelse)
        plt.plot(Unflexible + Heating  + v2g + electrolysis + storage, color = oragnes[5], label = 'Storage', linewidth=linjetykkelse)

        plt.grid(True, linestyle='--', alpha=0.5, axis = 'y')
        plt.xlabel('Hour', fontsize=14)
        plt.ylabel('Power (MW)', fontsize=14)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
        plt.ylim(0,25000)
        plt.xlim(2160,2879)
        plt.tight_layout()
        plt.show()

def plot_year():
    blues = sns.color_palette("Blues", desat = None, as_cmap = False)
    oragnes = sns.color_palette("Oranges", desat = None, as_cmap = False)

    linjetykkelse = 1.8

    file_path = 'Excel/Final.xlsx'
    # Excel sheet names
    scenarios = {'Only RES': 'Renewable', '1GW Nuclear': '1GW', '3GW Nuclear': '3GW', 'High Nuclear': 'Nuclear'}

    data_dict = {name: pd.read_csv(f'Data/{name}_timeseries.csv') for name, sheet in scenarios.items()}

    for name, data in data_dict.items():

        data.index = pd.date_range(start = '2045-01-01', periods = 8784, freq = 'h')

        # ---------------- Extract relevant data from csv file ----------------

        # Supply
        nuclear = data['Nuclear Electr.']
        wind_onshore_el = data['Wind Electr.']
        wind_offshore_el = data['Offshore Electr.']
        pv_el = data['PV Electr.']
        wave_el = data['Wave Electr.']
        biogas = data['Biogas']
        waste = data['Waste 2 Heat'] + data['Waste 3 Heat']
        CHP = data['CHP Electr.'] + data['CSHP Electr.']
        PP = data['PP Electr.'] + data['PP2 Electr.']
        renewable_el = wind_onshore_el + wind_offshore_el + pv_el + wave_el
        disch = data['Discharge Electr.']

        # Demand
        Unflexible = data['Electr. Demand']
        Heating = data['HP Electr.']
        v2g = data['Flexible Electr.'] + data['V2G Charge']
        electrolysis = data['H2 Electr.'] + data['CO2Hydro Electr.'] + data['NH3Hydro Electr.']
        storage = data['Charge Electr.']

        # ----------------------- Resample to weekly mean -----------------------
        weekly_data = pd.DataFrame({
            'nuclear': nuclear,
            'CHP': CHP,
            'renewable_el': renewable_el,
            'waste': waste,
            'PP': PP,
            'disch': disch,
            'Unflexible': Unflexible,
            'Heating': Heating,
            'v2g': v2g,
            'electrolysis': electrolysis,
            'storage': storage
        }).resample('D').mean()

        # ------------------------------ PLOT -------------------------------

        plt.figure(figsize=(25, 8))

        # Plot supply
        plt.stackplot(weekly_data.index, weekly_data['nuclear'], weekly_data['CHP'], weekly_data['renewable_el'],
            weekly_data['waste'], weekly_data['PP'], weekly_data['disch'], colors = blues,
            labels = ['Nuclear power', 'CHP plants', 'Renewable electricity', 'Waste incineration', 'Power plants',
                      'Storage'])

        # Plot demand
        plt.plot(weekly_data['Unflexible'], color=oragnes[1], label='Unflexible demand', linewidth=linjetykkelse)
        plt.plot(weekly_data['Unflexible'] + weekly_data['Heating'], color=oragnes[2], label='Electricity for heating', linewidth=linjetykkelse)
        plt.plot(weekly_data['Unflexible'] + weekly_data['Heating'] + weekly_data['electrolysis'], color=oragnes[3], label='Electricity for electrolysis', linewidth=linjetykkelse)
        plt.plot(weekly_data['Unflexible'] + weekly_data['Heating'] + weekly_data['v2g'] + weekly_data['electrolysis'], color=oragnes[4], label='Electricity for transport', linewidth=linjetykkelse)
        plt.plot(weekly_data['Unflexible'] + weekly_data['Heating'] + weekly_data['v2g'] + weekly_data['electrolysis'] + weekly_data['storage'], color=oragnes[5], label='Storage', linewidth=linjetykkelse)

        plt.grid(True, linestyle='--', alpha=0.5, axis='y')
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Power (MW)', fontsize=14)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
        plt.ylim(0, 25000)
        plt.tight_layout()
        plt.show()