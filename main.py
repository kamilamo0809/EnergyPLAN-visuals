from sensitivity_analysis import heatmap, CAPEX_sens, OPEX_sens
from plot_costs import calc_costs, plot_costs, plot_total_costs
from plot_timeseries import plot_april, plot_year, plot_imp_exp
from market_economic import plot_monthly_cf
from hydrogen import plot_h2_storage_individual
from data_prep import get_timeseries

scenarios = {'Only RES':        'Renewable',
             '1GW Nuclear':     'Nuclear_flex',
             '3GW Nuclear':     '3GW',
             'High Nuclear':    'Nuclear'}
def main():

    #for name, sheet_name in scenarios.items():
    #    get_timeseries('Excel/Original.xlsx', sheet_name, ['Nuclear Electr.', "Wave Electr.", "CHP 3 Heat", "Discharge Electr.", "Charge Electr.", 'H2 Storage'], f'Data/{name}_timeseries.csv', True)

    ''' ------------------------------------------------ PLOTS -------------------------------------------------'''
    # TODO: Comment out the functions you do not want to run

                                        # COSTS
    plot_costs(2.5, 1.13, 6.18, OPEX_nuclear = 30.20, outputfile = '--')                        # Relative costs (differences between scenarios)
    #plot_total_costs()                  # Total costs

                                        # SENSITIVITY ANALYSIS
    #heatmap(5, 2.1, 4.2, 4.2, 10.2)                           # Heatmap with a variation of offshore wind and nuclear CAPEX
    #CAPEX_sens(6.18, 2.1, 3.3, 'CAPEX_intersection_original')                        # Sensitivity to offshore wind CAPEX
    #CAPEX_sens(4.72, 2.1, 3.3, 'CAPEX_intersection_adj_nuclear')                        # Sensitivity to offshore wind CAPEX

    #OPEX_sens(1.9, plotname = 'OPEX_sens1.9')                         # Sensitivity to nuclear OPEX
    #OPEX_sens(2.5, plotname = 'OPEX_sens2.5')                         # Sensitivity to nuclear OPEX

                                        # TIMESERIES
    #plot_april()                        # Supply and demand for the month of april
    #plot_year()                         # Yearly supply and demand
    #plot_imp_exp()
                                        # CAPACITY FACTOR
    #plot_monthly_cf()                   # for each month for offshore and nuclear power

                                        # HYDROGEN STORAGE
    #plot_h2_storage_individual('./Excel/original.xlsx')        # Duration curves for H2 storage



if __name__ == "__main__":
    main()
