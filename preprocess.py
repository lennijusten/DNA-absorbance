import pandas as pd
import numpy as np
import os

# List of CSV files
files = ['Adenine.csv', 'Cytosine.csv', 'Guanine.csv', 'Thymine.csv']

# Initialize a dictionary to hold the dataframes
dfs = {}

# Define new_wavelength outside the loop
new_wavelength = np.arange(210, 321, 1)

# Constants
M_adenine = 135.13*10**3  # Molar mass of Adenine (units mg mol-1)
M_cytosine = 111.1*10**3  # Molar mass of Cytosine (units mg mol-1)
M_guanine = 151.13*10**3  # Molar mass of Guanine (units mg mol-1)
M_thymine = 126.11*10**3  # Molar mass of Thymine (units mg mol-1)

molar_mass = [M_adenine, M_cytosine, M_guanine, M_thymine]

for M, file in zip(molar_mass, files):
    path = os.path.join('raw-data', file)
    # Load the CSV file
    df = pd.read_csv(path, header=None, names=['Wavelength', 'Absorption Coefficient'])

    # Sort the dataframe by wavelength
    df = df.sort_values('Wavelength')

    # Reset the index after sorting
    df = df.reset_index(drop=True)

    # Multiply by 10^-3 as shown in axis label of Fig 2.8 in Kowalski (2009, 26)
    df['Absorption Coefficient'] = df['Absorption Coefficient']*10**-3

    # Covert from L mol-1 cm-1 to mL mol-1 cm-1
    df['Absorption Coefficient'] = df['Absorption Coefficient']*10**3

    # Covert absorption coefficient from mL mol-1 cm-1 to mL mg-1 cm-1 using molar mass
    df['Absorption Coefficient'] = df['Absorption Coefficient'] / M

    # Interpolate at 1 nm intervals
    new_df = pd.DataFrame({'Wavelength': new_wavelength})
    new_df['Absorption Coefficient'] = np.interp(new_wavelength, df['Wavelength'], df['Absorption Coefficient'])

    if file == 'Adenine.csv':
        # Replace first 6 rows with np.NaN as there is no data available in this range
        new_df.loc[:6, 'Absorption Coefficient'] = np.NaN

    new_df.to_csv(f'processed-data/{file}', index=False)

    # Store the new dataframe in the dictionary
    dfs[file] = new_df


