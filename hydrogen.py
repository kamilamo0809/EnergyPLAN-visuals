from data_prep import get_timeseries
import matplotlib.pyplot as plt
import seaborn as sns

def plot_h2_storage_individual(file):
    # Set Seaborn style and color palette
    sns.set_theme(style = "whitegrid")
    colors = sns.color_palette("mako", n_colors = 4)
    sns.set_palette(colors)

    scenarios = {'Only RES': 'Renewable', '1GW Nuclear': 'Nuclear_flex', '3GW Nuclear': '3GW', 'High Nuclear': 'Nuclear'}

    # X-axis values and constants
    x_values = list(range(8784))
    precentage = [0.486 * 100 for _ in x_values]

    # Helper function for plotting
    def plot_storage(scenario1, scenario2, title, filename, limit_label, storage_key = 'H2 Storage'):
        data1 = get_timeseries(file, scenario1, ["Nuclear Electr.", storage_key], ".")
        data2 = get_timeseries(file, scenario2, ["Nuclear Electr.", storage_key], ".")
        max1 = max(data1[storage_key] / 1000)

        fig, ax1 = plt.subplots(figsize = (6, 6))
        ax2 = ax1.twinx()

        prop = 658.7 / max1

        ax1.fill_between(x_values, sorted(data1[storage_key] / 1000, reverse = True), color = palet[1],
                         label = "Unlimited Storage Capacity")
        ax1.fill_between(x_values, sorted(data2[storage_key] / 1000, reverse = True), color = palet[3],
                         label = limit_label)
        ax2.plot(x_values, precentage, color = mako[4], linewidth = 1,
                 label = "48.6% of unconstraind storage capacity")

        ax1.set_xlabel("Hour", fontsize = 14)
        ax1.set_ylim(-658.7 * 0.05, 658.7 * 1.05)
        ax2.set_ylim(-0.05 * prop * 100, 1.05 * prop * 100)

        ax2.tick_params(axis = 'y', labelsize = 13, colors = mako[4])
        ax2.spines['right'].set_color(mako[4])
        ax2.yaxis.label.set_color(mako[4])

        fig.tight_layout()
        plt.show()


    plot_storage(scenario1 = 'Nuclear_flex_dh_640', scenario2 = 'Nuclear_flex_dh_180', title = '1 GW Nuclear',
        filename = 'storage_1GW', limit_label = 'Storage Capacity Limited to 180.2 GWh')

    plot_storage(scenario1 = 'Nuc3_800', scenario2 = 'Nuc3_144', title = '3 GW Nuclear', filename = 'storage_3GW',
        limit_label = 'Storage Capacity Limited to 180.2 GWh')

    plot_storage(scenario1 = 'Nuc_800', scenario2 = 'Nuc_0', title = 'High Nuclear',
        filename = 'storage_high_nuclear', limit_label = 'Storage Capacity Limited to 180.2 GWh')
