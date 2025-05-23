from plot_costs import calc_costs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from interface import get_scensrios, get_dh_scenarios

def heatmap(resolution = 30, off_low = 2.18, off_upp = 3.2, nuc_low = 4.29, nuc_upp = 10.24):
    '''
    This function plots the least cost scenario of a range of offshore wind and nuclear CAPEX combinations in a heatmap

    :param resolution: resolution of the heatmap
    :param off_low: lower bound for offshore wind CAPEX
    :param off_upp: upper bound for offshore wind CAPEX
    :param nuc_low: lower bound for nuclear CAPEX
    :param nuc_upp: upper bound for nuclear CAPEX

    :return: None
    '''

    scenarios = get_dh_scenarios()

    # Set range and resolution of sensitivity analysis
    offshore_capex_values = np.linspace(off_low, off_upp, resolution)
    nuclear_capex_values = np.linspace(nuc_low, nuc_upp, resolution)

    # Make offshore go the other way in the map
    offshore_capex_values = offshore_capex_values[::-1]

    # Get scenario names
    names = list(scenarios.keys())

    # Make empty arrays
    best_cost = np.full((len(nuclear_capex_values), len(offshore_capex_values)), np.inf)
    best_scenario = np.empty_like(best_cost, dtype=object)
    best_scenario_number = np.full((len(nuclear_capex_values), len(offshore_capex_values)), np.inf)

    # Iterate through every CAPEX combination
    for i, c_off in enumerate(offshore_capex_values):
        for j, c_nuc in enumerate(nuclear_capex_values):
            uranium_uses, inv_res_values, OM_values, nuc_inv, remaining_inv = calc_costs(c_off, 1.13, c_nuc)
            for idx, n in enumerate(names):
                # Calculate total scenario cost
                total = uranium_uses[n] + inv_res_values[n] + OM_values[n] + nuc_inv[n] + remaining_inv[n]

                # Add values to array if it is the least cost scenario
                if total < best_cost[i, j]:
                    best_cost[i, j] = total             # Save cost
                    best_scenario[i, j] = n             # Save scenario name
                    best_scenario_number[i, j] = idx    # Save scenario index


    # Make pandas DataFrame for seaborn heatmap
    df = pd.DataFrame(best_scenario_number,
                      columns=[f"{v:.1f}" for v in nuclear_capex_values],
                      index=[f"{v:.1f}" for v in offshore_capex_values])

    # Set color palette
    colorblind = sns.color_palette('Blues')
    colors = ['#8FD7D7',  '#FF8CA1', '#BDD373','#FFB255']
    yellows = sns.color_palette('YlOrRd', 8)
    yellows = yellows[4::-1]
    sns.set_palette(yellows)


    # Make figure and plot heatmap
    plt.figure(figsize = (8, 4))  # width=8 inches, height=6 inches
    cmap = plt.get_cmap("Blues", len(names))  # same colormap used in the heatmap
    ax = sns.heatmap(df, cmap = cmap, annot = False, fmt = "")

    # Make colorbar to the right of the chart
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks(np.arange(len(names)))  # Set tick positions
    colorbar.set_ticklabels(names)

    # Set lables and save figure to heatmap.eps
    ax.set_xlabel("Nuclear CAPEX [MEUR/MW]")
    ax.set_ylabel("Offshore Wind CAPEX [MEUR/MW]")
    plt.tight_layout()
    plt.show()


def CAPEX_sens(nuc_capex = 6.18, x1 = 1.9, x2 = 3.5, plotname = '--'):
    '''
    This function plots how total costs change for scenarios when offshore wind CAPEX changes

    :param x1: lower bound for offshore wind CAPEX
    :param x2: upper bound for offshore wind CAPEX

    :return: None
    '''

    # Make array
    x = np.array([x1, x2])

    # Calculate cost with CAPEX assumtions
    lower_sum = calc_costs(x1, 1.13, nuc_capex)
    upper_sum = calc_costs(x2, 1.13, nuc_capex)

    sum_RES_lower, sum_1gw_lower, sum_3gw_lower, sum_high_lower = 0, 0, 0, 0
    sum_RES_upper, sum_1gw_upper, sum_3gw_upper, sum_high_upper = 0, 0, 0, 0

    # Calculate upper and lower sum for each scenario
    for item in lower_sum:
        sum_RES_lower += item['Only RES']
        sum_1gw_lower += item['1GW Nuclear w/ DH']
        sum_3gw_lower += item['3GW Nuclear w/ DH']
        sum_high_lower += item['High Nuclear w/ DH']

    for item in upper_sum:
        sum_RES_upper += item['Only RES']
        sum_1gw_upper += item['1GW Nuclear w/ DH']
        sum_3gw_upper += item['3GW Nuclear w/ DH']
        sum_high_upper += item['High Nuclear w/ DH']

    # Choose scenarios to plot
    scenarios = {
        'Only Renewables': np.array([sum_RES_lower, sum_RES_upper]),
        '1 GW Nuclear w/ DH': np.array([sum_1gw_lower, sum_1gw_upper]),
        '3 GW Nuclear w/ DH': np.array([sum_3gw_lower, sum_3gw_upper]),
        'High Nuclear w/ DH': np.array([sum_high_lower, sum_high_upper]),
    }

    scenario_names = list(scenarios.keys())
    scenario_lines = [scenarios[name] for name in scenario_names]

    # Function to compute intersection between two lines
    def compute_intersection(x_vals, y1, y2):
        m1, b1 = np.polyfit(x_vals, y1, 1)
        m2, b2 = np.polyfit(x_vals, y2, 1)
        x_int = (b2 - b1) / (m1 - m2)
        y_int = m1 * x_int + b1
        return x_int, y_int

    intersections = []
    # Create intersections between adjacent scenarios
    for x_line in scenario_lines:
        for y_line in scenario_lines:
            intersections.append(compute_intersection(x, x_line, y_line))

    # Plot

    # Set Seaborn style and color palette
    sns.set_theme(style = "whitegrid")
    #colors = sns.color_palette("mako", n_colors = 4)
    #colors = sns.color_palette("hls", n_colors = 6)
    colors = ['#8FD7D7',  '#FF8CA1', '#BDD373','#FFB255']
    #colors = ['#00B0BE',  '#F45F74',  '#98C127', '#FFB255']

    sns.set_palette(colors)

    plt.figure(figsize=(5, 4))

    for label, y_vals in scenarios.items():
        plt.plot(x, y_vals/1000, label=label, linewidth=4)

    y_low = min(sum_RES_lower, sum_1gw_lower, sum_3gw_lower, sum_high_lower)
    y_high = max(sum_RES_upper, sum_1gw_upper, sum_3gw_upper, sum_high_upper)

    # Mark intersections
    for i, q in enumerate(intersections):
        xi, yi = q[0], q[1] / 1000
        if x1 <= xi <= x2:
            # Sjekk y-verdier for alle scenarier i punktet xi
            y_vals_at_xi = [np.polyval(np.polyfit(x, line, 1), xi) for line in scenario_lines]
            y_vals_at_xi = [o / 1000 for o in y_vals_at_xi]
            min_y = min(y_vals_at_xi)

            if np.isclose(yi, min_y, atol = 1e-3):  # litt mer romslig toleranse
                plt.scatter(xi, yi, color = 'black', s = 100, zorder = 5)
                xi2 = xi
                if yi <= (y_low/ 1000 + 0.400):
                    yi2 = y_low / 1000 + 0.300
                    xi2 = xi + 0.3
                else:
                    yi2 = yi

                if xi >= (x2 - 0.3):
                    xi2 = x2 - 0.3

                plt.annotate(f"(CAPEX = {xi:.2f})", xy = (xi, yi - 0.05), xytext = (xi2, yi2 - 0.3),
                             arrowprops = dict(arrowstyle = '->', lw = 1, color = 'black'), fontsize = 10)

     # Labels and formatting
    plt.xlabel("Offshore wind CAPEX [MEUR/MW-e]", fontsize=12)
    plt.ylabel("Total annual costs [bEUR]", fontsize=12)
    #plt.title("Scenario Cost Comparison vs Offshore Wind CAPEX", fontsize=14)

    plt.ylim(23.400, (y_high + 100)/ 1000)

    plt.tight_layout()
    plt.show()


def OPEX_sens(offshore_capex = 2.5, x1 = 23, x2 = 35, plotname = '--'):
    '''
    This function plots how total costs for scenarios change for scenarios when the total nuclear OPEX changes

    :param x1: lower bound for nuclear OPEX
    :param x2: upper bound for nuclear OPEX
    :return:
    '''

    # Make array
    y = np.array([x1, x2])

    # Calculate costs
    lower_sum = calc_costs(offshore_capex, 1.13, 6.18, y[0])
    upper_sum = calc_costs(offshore_capex, 1.13, 6.18, y[1])

    sum_RES_lower, sum_1gw_lower, sum_3gw_lower, sum_high_lower = 0, 0, 0, 0
    sum_RES_upper, sum_1gw_upper, sum_3gw_upper, sum_high_upper = 0, 0, 0, 0

    # Calculate upper and lower sum for each scenario
    for item in lower_sum:
        sum_RES_lower += item['Only RES']
        sum_1gw_lower += item['1GW Nuclear w/ DH']
        sum_3gw_lower += item['3GW Nuclear w/ DH']
        sum_high_lower += item['High Nuclear w/ DH']

    for item in upper_sum:
        sum_RES_upper += item['Only RES']
        sum_1gw_upper += item['1GW Nuclear w/ DH']
        sum_3gw_upper += item['3GW Nuclear w/ DH']
        sum_high_upper += item['High Nuclear w/ DH']

    # Choose scenarios to plot
    scenarios = {
        'Only Renewables': np.array([sum_RES_lower, sum_RES_upper]),
        '1 GW Nuclear w/ DH': np.array([sum_1gw_lower, sum_1gw_upper]),
        '3 GW Nuclear w/ DH': np.array([sum_3gw_lower, sum_3gw_upper]),
        'High Nuclear w/ DH': np.array([sum_high_lower, sum_high_upper]),
    }

    scenario_names = list(scenarios.keys())
    scenario_lines = [scenarios[name] for name in scenario_names]

    # Function to compute intersection between two lines
    def compute_intersection(x_vals, y1, y2):
        m1, b1 = np.polyfit(x_vals, y1, 1)
        m2, b2 = np.polyfit(x_vals, y2, 1)
        x_int = (b2 - b1) / (m1 - m2)
        y_int = m1 * x_int + b1
        return x_int, y_int

    intersections = []
    # Create intersections between adjacent scenarios
    for x_line in scenario_lines:
        for y_line in scenario_lines:
            intersections.append(compute_intersection(y, x_line, y_line))

    # Plot

    # Set Seaborn style and color palette
    sns.set_theme(style = "whitegrid")
    #colors = sns.color_palette("mako", n_colors = 4)
    #colors = sns.color_palette("hls", n_colors = 6)
    colors = ['#8FD7D7',  '#FF8CA1', '#BDD373','#FFB255']
    #colors = ['#00B0BE',  '#F45F74',  '#98C127', '#FFB255']

    sns.set_palette(colors)

    plt.figure(figsize=(5, 4))

    for label, y_vals in scenarios.items():
        plt.plot(y, y_vals/1000, label=label, linewidth=4)

    y_low = min(sum_RES_lower, sum_1gw_lower, sum_3gw_lower, sum_high_lower)
    y_high = max(sum_RES_upper, sum_1gw_upper, sum_3gw_upper, sum_high_upper)

    # Mark intersections
    for i, q in enumerate(intersections):
        xi, yi = q[0], q[1] / 1000
        if x1 <= xi <= x2:
            # Sjekk y-verdier for alle scenarier i punktet xi
            y_vals_at_xi = [np.polyval(np.polyfit(y, line, 1), xi) for line in scenario_lines]
            y_vals_at_xi = [o / 1000 for o in y_vals_at_xi]
            min_y = min(y_vals_at_xi)

            if np.isclose(yi, min_y, atol = 1e-3):  # litt mer romslig toleranse
                plt.scatter(xi, yi, color = 'black', s = 100, zorder = 5)
                xi2 = xi
                if yi <= (y_low/ 1000 + 0.400):
                    yi2 = y_low / 1000 + 0.500
                    xi2 = xi + 1
                else:
                    yi2 = yi

                if xi >= (x2 - 0.3):
                    xi2 = x2 - 0.3

                plt.annotate(f"(OPEX = {xi:.2f})", xy = (xi, yi - 0.05), xytext = (xi2, yi2 - 0.3),
                             arrowprops = dict(arrowstyle = '->', lw = 1, color = 'black'), fontsize = 10)

     # Labels and formatting
    plt.xlabel("Nuclear OPEX [MEUR/MWh]", fontsize=12)
    plt.ylabel("Total annual costs [bEUR]", fontsize=12)
    #plt.title("Scenario Cost Comparison vs Offshore Wind CAPEX", fontsize=14)

    plt.ylim(23.200, (y_high + 100)/ 1000)

    plt.tight_layout()
    plt.show()


