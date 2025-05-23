'''

'''

import pandas as pd

def get_timeseries(file_path, sheet, extra_columns, output_file = '.', save = False):
    '''
    This function processes and returns timeseries data from EnergyPLAN excel files with nice names, 
    and only necessary columns
    
    :param file_path: File path to excel file with EnergyPLAN results
    :param sheet: Name of the sheet in the excel file
    :param extra_columns: Add any extra columns with only 0 values if they are needed
    :param output_file: File to save result in if save = True
    :param save: Saves the results to csv if True. Else False
    
    :return: Timeseries dataframe
    '''
    
    # Read excel file
    xls = pd.ExcelFile(file_path)

    # read columns from rows 83 and 84 (index 82 and 83)
    df_columns = pd.read_excel(xls, sheet_name=sheet, skiprows=82, nrows=2, header=None)

    # Conbine the rows to make column names
    column_names = df_columns.astype(str).apply(lambda x: ' '.join(x.dropna()), axis=0).tolist()
    clean_column_names = [' '.join(name.split()).strip() for name in column_names if name.strip()]
    clean_column_names.insert(0, 'index')
    clean_column_names = ['Hour' if name == 'nan nan' else name for name in clean_column_names]

    # Read the timeseries from row 108 with the new column names
    df_hourly_values = pd.read_excel(xls, sheet_name=sheet, skiprows=107, header=None)
    df_hourly_values.columns = clean_column_names

    # Remove empty columns and 'index'
    df_hourly_values_filtered = df_hourly_values.loc[:, (df_hourly_values != 0).any(axis=0)]
    df_hourly_values_filtered = df_hourly_values_filtered.drop(columns=['index'], errors='ignore')

    # Add necessary columns if they do not exist
    for col in extra_columns:
        if col in df_hourly_values.columns:
            df_hourly_values_filtered[col] = df_hourly_values[col]

    # Save to CSV if save = True
    if save == True:
        df_hourly_values_filtered.to_csv(output_file, index=False)

    return df_hourly_values_filtered


def get_annual_data(file_path, sheet):
    '''
    This function reads excel sheets with data from EnergyPLAN, extract annual data og adds it to a dictionary of
    datatypes such as FUEL, CO2, INVESTMENT and COSTS
    
    :param file_path: File path to excel file with EnergyPLAN results
    :param sheet: Name of the sheet in the excel file
    
    :return: dictionary with annual data
    '''

    # Make a dictionary and add CO2, RESULTS and FUEL values
    data_dict = {'CO2': pd.read_excel(file_path, sheet_name = sheet, usecols = [1, 2], skiprows = 17, nrows = 2),
                 'RES': pd.read_excel(file_path, sheet_name = sheet, usecols = [1, 2], skiprows = 21, nrows = 3),
                 'FUEL': pd.read_excel(file_path, sheet_name = sheet, usecols = [1, 2], skiprows = 26, nrows = 12)}
    # Add INVESTMENT costs from the first column
    INV = pd.read_excel(file_path, sheet_name = sheet, usecols = [7, 8, 9, 10], skiprows = 7, nrows = 56)
    INV = INV.iloc[1:]
    data_dict['INV'] = INV

    # Add costs
    COSTS = pd.read_excel(file_path, sheet_name = sheet, usecols = [1, 2, 3, 4], skiprows = 40, nrows = 30)
    COSTS = COSTS.dropna(how = 'all')
    data_dict['COSTS'] = COSTS

    # Add INVESTMENT costs from the second column
    INV2 = pd.read_excel(file_path, sheet_name = sheet, usecols = [12, 13, 14, 15], skiprows = 7, nrows = 49)
    INV2.iloc[:, 0] = INV2.iloc[:, 0].ffill()
    INV2 = INV2.dropna()
    INV2 = INV2.iloc[1:]
    data_dict['INV2'] = INV2

    df_columns = pd.read_excel(file_path, sheet_name = sheet, skiprows = 82, nrows = 2, header = None)
    column_names = df_columns.astype(str).apply(lambda x: ' '.join(x.dropna()), axis = 0).tolist()
    clean_column_names = [' '.join(name.split()).strip() for name in column_names if name.strip()]
    clean_column_names.insert(0, 'index')
    clean_column_names = ['Hour' if name == 'nan nan' else name for name in clean_column_names]

    energy = pd.read_excel(file_path, sheet_name = sheet, skiprows = 86, header = None, nrows = 1)
    energy.columns = clean_column_names
    energy = energy.iloc[:, 2:]
    energy = energy.drop('Stabil. Load', axis = 1)
    energy_values = energy.astype(str).apply(lambda x: ' '.join(x.dropna()), axis = 0).tolist()
    energy_values = [' '.join(value.split()).strip() for value in energy_values if value.strip()]
    energy_values = [item.replace(',', '.') for item in energy_values]
    energy_values = [float(x) for x in energy_values]
    energy.iloc[0] = energy_values

    data_dict['ENERGY'] = energy

    return data_dict
