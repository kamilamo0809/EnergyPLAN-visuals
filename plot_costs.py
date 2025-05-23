import matplotlib.pyplot as plt
from data_prep import get_annual_data
import numpy as np
import seaborn as sns
from interface import settings, get_file_path, get_scensrios

def calc_costs(CAPEX_offshore = 1.9, CAPEX_onshore = 1.03, CAPEX_nuclear = 6.18, OPEX_nuclear = 30.20):
    '''
    This function calculates costs within 5 different categories for each scenario

    :param CAPEX_offshore: Offshore wind CAPEX assumption
    :param CAPEX_onshore: Onshore wind CAPEX assumption
    :param CAPEX_nuclear: Nuclear CAPEX assumption
    :param OPEX_nuclear: Nuclear OPEX assumption

    :return: 5 dictionaries (for each category) with scenario costs
    '''
    print(f'Calculating costs\t CAPEX offshore = {CAPEX_offshore}, CAPEX nuclear = {CAPEX_nuclear}')

    (file_path, scenarios, output_file, nuc_size, offshore_size, onshore_size, pv_size, change_cf, offshore_CF_original,
     onshore_CF_original, PV_CF_original, offshore_CF, onshore_CF, PV_CF, ir, lifetime_nuc, lifetime_off, lifetime_on,
     uranium_cost, OM_nuc, OM_offshore_2035) = settings()

    # read data to annual lists
    data = {name: get_annual_data(file_path, sheet) for name, sheet in scenarios.items()}
    CAPEX_PV = 0.6
    lifetime_pv = 40
    # Change CF if true
    if change_cf:
        offshore_size = {k: v * offshore_CF_original / offshore_CF for k, v in offshore_size.items()}
        onshore_size = {k: v * onshore_CF_original / onshore_CF for k, v in onshore_size.items()}
        pv_size = {k: v * PV_CF_original / PV_CF for k, v in pv_size.items()}

    print('Offshore capacities:\n', offshore_size, '\nOnshore capacities:\n', onshore_size, '\nPV capacities:\n', pv_size)
    # Set OPEX values
    fixed_OM_nuc = (OM_nuc * 8760 * 0.9) / (CAPEX_nuclear * 1e6)
    fixed_OM_off = 0.0167 # Technology catalouge: 1.44 ved normal CAPEX forecast
    fixed_OM_on = 0.0251
    OPEX_nuclear = OPEX_nuclear - 14.26 - 9.33


    # Make empty dicts for saving costs
    uranium_uses, inv_res_values, OM_values, nuc_inv, remaining_inv = {}, {}, {}, {}, {}

    # Process each scenario
    for name, scenario in data.items():
        # Get annual nuclear electricity production (TWh) (if there is some)
        if 'Nuclear Electr.' in scenario['ENERGY']:
            nuclear_electr = scenario['ENERGY']['Nuclear Electr.'].iloc[0]
        else:
            nuclear_electr = 0  # Set to zero if empty

        # Calculate uranium costs
        uranium_use = nuclear_electr * uranium_cost

        # Calculate O&M costs
        OM = (sum(scenario['INV'].get('Fixed', [0])) + sum(scenario['INV2'].get('Fixed.1', [0]))
              - scenario['INV'].get('Fixed', [0])[18] + CAPEX_nuclear * nuc_size[name] * fixed_OM_nuc
              - scenario['INV'].get('Fixed', [0])[11] + CAPEX_offshore* offshore_size[name] * fixed_OM_off
              - scenario['INV'].get('Fixed', [0])[10] + CAPEX_onshore * onshore_size[name] * fixed_OM_on
              + scenario['COSTS'].get('TOTAL:  ')[22]) - scenario['COSTS'].get('VARIABLE:')[10] + nuclear_electr * (OPEX_nuclear - 15)

        # Calculate investment in renewable energy (wind, solar, hydro, river etc.)
        inv_res = (sum(scenario['INV'].get('Annual Inv.', [0])[12:16])
                   + round(offshore_size[name] * CAPEX_offshore * ir / (1 - (1 + ir)**(-lifetime_off)), 0)
                   + round(onshore_size[name] * CAPEX_onshore * ir / (1 - (1 + ir)**(-lifetime_on)), 0)
                   + round(pv_size[name] * CAPEX_PV * ir / (1 - (1 + ir)**(-lifetime_pv)), 0))

        # Calculate investment in nuclear power
        inv_nuc = nuc_size[name] * CAPEX_nuclear * ir / (1 - (1 + ir)**(-lifetime_nuc))

        # Calculate remaining investments
        rem_inv = (scenario['COSTS'].get('TOTAL:  ')[28] - sum(scenario['INV'].get('Annual Inv.', [0])[9:16]) - scenario['INV'].get('Annual Inv.', [0])[18] - sum(scenario['INV'].get('Fixed', [0])) - sum(scenario['INV2'].get('Fixed.1', [0])) - scenario['COSTS'].get('TOTAL:  ')[22] + scenario['COSTS'].get('VARIABLE:')[10]) #sum(scenario['INV'].get('Annual Inv.', [0])) + sum(

        # Save in dictionaries before moving on to the next scenario
        uranium_uses[name] = uranium_use
        inv_res_values[name] = inv_res
        OM_values[name] = OM
        nuc_inv[name] = inv_nuc
        remaining_inv[name] = rem_inv

    return uranium_uses, inv_res_values, OM_values, nuc_inv, remaining_inv

def plot_costs(CAPEX_offshore = 1.9, CAPEX_onshore = 1.03, CAPEX_nuclear = 6.18, OPEX_nuclear = 30.44, outputfile = '--'):

    file_path = get_file_path()
    scenarios = get_scensrios()
    data = {name: get_annual_data(file_path, sheet) for name, sheet in scenarios.items()}

    uranium_uses, inv_res_values, OM_values, nuc_inv, remaining_inv = calc_costs(CAPEX_offshore, CAPEX_onshore, CAPEX_nuclear, OPEX_nuclear)
    tot_cost = {}
    for n in list(data.keys()):
        tot_cost[n] = uranium_uses[n] + inv_res_values[n] + OM_values[n] + nuc_inv[n] + remaining_inv[n]
        print(n, tot_cost[n])

    print('\n')

    prosent = {}
    for i in list(data.keys()):
        for j in list(data.keys()):
            prosent[i,j] = tot_cost[i] / tot_cost[j] * 100

    # Find the cheapest scenario

    min_cost = min(tot_cost.values())
    cheapest_scenario = next((k for k, v in tot_cost.items() if v == min_cost), None)
    pro_diff = {}
    cost_diff = {}
    for i in list(data.keys()):
        pro_diff[i] = prosent[i, cheapest_scenario] - 100
        cost_diff[i] = tot_cost[i] - tot_cost[cheapest_scenario]

    print(pro_diff)
    print(cost_diff)

    # Juster verdier slik at de er relative til minste verdi
    for values in [inv_res_values, OM_values, remaining_inv]:
        min_val = min(values.values())
        for key in values:
            values[key] -= min_val

    # Lag en liste av nullverdier
    bottom = np.zeros(len(scenarios))

    # Sett barbredde
    width = 0.3

    # Definer datasett for plotting
    weight_counts = {'Uranium': np.array(list(uranium_uses.values())),
        'Operation and maintenance': np.array(list(OM_values.values())),
        'Investment in renewable electricity': np.array(list(inv_res_values.values())),
        'Investment in nuclear power': np.array(list(nuc_inv.values())),
        'Remaining investments': np.array(list(remaining_inv.values()))}

    # Finn den laveste søylesummen
    total_costs = np.sum(np.array(list(weight_counts.values())), axis=0)

    min_bar_value = min(total_costs)

    # Set color palette
    colorblind = sns.color_palette('Blues')
    custom_palette = [colorblind[i] for i in [1, 2, 3, 4, 5]]
    sns.set_palette(custom_palette)


    # Plott diagram
    fig, ax = plt.subplots(figsize = (10, 5))
    x = np.zeros(len(scenarios))  # X-posisjoner for søyler
    num_scenarios = len(scenarios)
    # First bar alone
    x[0] = 0.2
    # Remaining bars in pairs
    x_positions = np.arange(1, (num_scenarios + 1) // 2)  # Positions for pairs
    x[1::2] = x_positions - (width / 2 + 0.02)  # Left bar in pair
    x[2::2] = x_positions + (width / 2 + 0.02) # Right bar in pair

    # Loop gjennom kategoriene og plott
    for i, (label, values) in enumerate(weight_counts.items()):
        ax.bar(x, values, width, label = label, bottom = bottom, color = colorblind[i+1])
        bottom += values

    fig.subplots_adjust(bottom=0.1)  # Adjust the value as needed

    # --- Add Labels ---
    # Individual scenario labels
    scenario_labels = scenarios.copy()

    # Common labels for grouped bars
    group_labels = [list(scenarios.keys())[i] for i in [0, 1, 3, 5]]
    group_positions = [x[0], (x[1]+x[2])/2, (x[3]+x[4])/2, (x[5]+x[6])/2]

    # Set grouped labels at midpoint
    for label, pos in zip(group_labels, group_positions):
        if label:  # Avoid empty labels
            ax.text(pos, -min(total_costs) * 0.2, label, ha='center', va='top', fontsize=12)


    # Legg til en horisontal linje for laveste søyleverdi
    ax.axhline(min_bar_value, color='black', linestyle='--', linewidth=2, label='Lowest total cost')

    bbbl = ['', 'without DH \nutilization', 'with DH \nutilization', 'without DH \nutilization', 'with DH \nutilization', 'without DH \nutilization', 'with DH \nutilization']

    # Forbedret utseende
    ax.set_xticks(x)
    ax.set_xticklabels(bbbl, rotation = 0, ha='center', fontsize=7)
    ax.xaxis.set_tick_params(pad=10)  # Moves labels further away from axis
    plt.grid(True, linestyle = '--', axis = 'y')
    plt.ylim(0, 3500)
    ax.set_ylabel("Annual costs [M EUR]")
    plt.legend(loc = 'center left', bbox_to_anchor = (1.02, 0.5),  # Push legend outside the axes
        borderaxespad = 0., frameon = False,
    labelspacing=4)

    plt.tight_layout()
    plt.show()

    yellows = sns.color_palette('YlOrRd', 16)
    yellows = yellows[7::-1]
    # Plot
    pro_diff = dict(sorted(pro_diff.items(), key = lambda item: item[1]))
    cost_diff = dict(sorted(cost_diff.items(), key = lambda item: item[1]))
    fig, ax = plt.subplots(figsize = (8, 3))
    values = [round(x, 3) for x in pro_diff.values()]
    values2 = [round(x, 3) for x in cost_diff.values()]

    bars = ax.barh(list(pro_diff.keys()), values2, color = yellows)

    # Legg på prosent til høyre for hver søyle
    for bar, pct in zip(bars, values):
        width = bar.get_width()
        ax.text(width + 10, bar.get_y() + bar.get_height() / 2, f'+{pct}%', ha = 'left', va = 'center', fontsize = 10)

    # Stil

    # Fjern rammen (spines)
    for spine in ['bottom', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    # Flytt x-aksen til toppen
    ax.xaxis.set_ticks_position('top')  # Sett tickene øverst
    ax.xaxis.set_label_position('top')  # Sett label øverst
    #ax.set_xticks()
    plt.tight_layout()
    plt.xlim(0, max(values2) * 1.1)
    ax.spines['top'].set_color('black')
    plt.xticks(color = 'black')

    plt.show()


def plot_total_costs(CAPEX_offshore = 1.9, CAPEX_onshore = 1.03, CAPEX_nuclear = 6.18, OPEX_nuclear = 30.44):

    file_path = get_file_path()
    scenarios = get_scensrios()
    data = {name: get_annual_data(file_path, sheet) for name, sheet in scenarios.items()}

    uranium_uses, inv_res_values, OM_values, nuc_inv, remaining_inv = calc_costs(CAPEX_offshore, CAPEX_onshore, CAPEX_nuclear, OPEX_nuclear)
    tot_cost = {}
    for n in list(data.keys()):
        tot_cost[n] = uranium_uses[n] + inv_res_values[n] + OM_values[n] + nuc_inv[n] + remaining_inv[n]
        print(n, tot_cost[n])

    prosent = {}
    for i in list(data.keys()):
        for j in list(data.keys()):
            prosent[i,j] = tot_cost[i] / tot_cost[j] * 100

    print(prosent)

    # Lag en liste av nullverdier
    bottom = np.zeros(len(scenarios))

    # Sett barbredde
    width = 0.3

    # Definer datasett for plotting
    weight_counts = {'Uranium': np.array(list(uranium_uses.values())),
        'Operation and maintenance': np.array(list(OM_values.values())),
        'Investment in renewable electricity': np.array(list(inv_res_values.values())),
        'Investment in nuclear power': np.array(list(nuc_inv.values())),
        'Remaining investments': np.array(list(remaining_inv.values()))}

    # Set color palette
    colorblind = sns.color_palette('Blues')
    custom_palette = [colorblind[i] for i in [1, 2, 3, 4, 5]]
    sns.set_palette(custom_palette)

    # Finn den laveste søylesummen
    total_costs = np.sum(np.array(list(weight_counts.values())), axis=0)

    min_bar_value = min(total_costs)

    # Plott diagram
    fig, ax = plt.subplots(figsize = (10, 5))
    x = np.zeros(len(scenarios))  # X-posisjoner for søyler
    num_scenarios = len(scenarios)
    # First bar alone
    x[0] = 0.2
    # Remaining bars in pairs
    x_positions = np.arange(1, (num_scenarios + 1) // 2)  # Positions for pairs
    x[1::2] = x_positions - (width / 2 + 0.02)  # Left bar in pair
    x[2::2] = x_positions + (width / 2 + 0.02) # Right bar in pair

    # Loop gjennom kategoriene og plott
    for i, (label, values) in enumerate(weight_counts.items()):
        ax.bar(x, values, width, label = label, bottom = bottom, color = colorblind[i+1])
        bottom += values

    fig.subplots_adjust(bottom=0.1)  # Adjust the value as needed

    # --- Add Labels ---
    # Individual scenario labels
    scenario_labels = scenarios.copy()

    # Common labels for grouped bars
    group_labels = [list(scenarios.keys())[i] for i in [0, 1, 3, 5]]
    group_positions = [x[0], (x[1]+x[2])/2, (x[3]+x[4])/2, (x[5]+x[6])/2]

    # Set grouped labels at midpoint
    for label, pos in zip(group_labels, group_positions):
        if label:  # Avoid empty labels
            ax.text(pos, -min(total_costs) * 0.2, label, ha='center', va='top', fontsize=16)


    # Legg til en horisontal linje for laveste søyleverdi
    ax.axhline(min_bar_value, color='black', linestyle='--', linewidth=2, label='Lowest total cost')

    bbbl = ['', 'without DH \nutilization', 'with DH \nutilization', 'without DH \nutilization', 'with DH \nutilization', 'without DH \nutilization', 'with DH \nutilization']

    # Forbedret utseende
    ax.set_xticks(x)
    ax.set_xticklabels(bbbl, rotation = 0, ha='center', fontsize = 7)
    ax.xaxis.set_tick_params(pad=10)  # Moves labels further away from axis
    plt.grid(True, linestyle = '--', axis = 'y')
    plt.ylim(0, 30000)
    ax.set_ylabel("Annual costs [M EUR]")
    plt.legend(loc = 'center left', bbox_to_anchor = (1.02, 0.5),  # Push legend outside the axes
        borderaxespad = 0., frameon = False, labelspacing=4)
    plt.tight_layout()
    plt.show()

    sns.color_palette(palette='colorblind', n_colors=5, desat=None, as_cmap=False)

