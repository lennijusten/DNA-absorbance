import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.style as style

# Get a list of all CSV files in the 'processed-data' directory
files = os.listdir('processed-data')

def generate_combined_df(files):
    # Initialize an empty dataframe to hold the combined data
    combined_df = pd.DataFrame()

    for file in files:
        # Load the CSV file
        df = pd.read_csv(f'processed-data/{file}')

        # If combined_df is empty, copy the 'Wavelength' column from df
        if combined_df.empty:
            combined_df['Wavelength'] = df['Wavelength']

        # Add the 'Absorption' column to combined_df
        # Use the file name (without the extension) as the column name
        column_name = os.path.splitext(file)[0]
        combined_df[column_name] = df['Absorption']

    # Calculate the mean and standard deviation of absorption at each wavelength
    combined_df['Mean Absorption Coefficient'] = combined_df.iloc[:, 1:].mean(axis=1)
    combined_df['Absorption Coefficient Std Dev'] = combined_df.iloc[:, 1:-1].std(axis=1)

    combined_df.to_csv('data-table.csv')
    return combined_df


combined_df = generate_combined_df(files)


def plot_data(df):
    # Use an academic style for the plot
    style.use('seaborn-whitegrid')

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Plot the absorption coefficient
    plt.plot(df['Wavelength'], df['Adenine'], linestyle='solid', color='black', label='Adenine')
    plt.plot(df['Wavelength'], df['Cytosine'], linestyle='dotted', color='black', label='Cytosine')
    plt.plot(df['Wavelength'], df['Guanine'], linestyle='dashed', color='black', label='Guanine')
    plt.plot(df['Wavelength'], df['Thymine'], linestyle='dashdot', color='black', label='Thymine')

    # # Plot the mean absorption coefficient with a line
    # plt.plot(df['Wavelength'], df['Mean Absorption Coefficient'], color='red', label='Mean Absorption Coefficient')
    #
    # # Add a shaded region for the standard deviation
    # plt.fill_between(df['Wavelength'],
    #                  df['Mean Absorption Coefficient'] - df['Absorption Coefficient Std Dev'],
    #                  df['Mean Absorption Coefficient'] + df['Absorption Coefficient Std Dev'],
    #                  color='gray', alpha=0.3, label='Standard Deviation')

    # Add labels and title
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorption Coefficient (ml mg-1 cm-1)')
    plt.title('Absorption Coefficients of the DNA Nucleotides')

    # Add a legend
    plt.legend()

    plt.savefig('DNA-absorption-coefficient.png', dpi=300)

    # Show the plot
    plt.show()

# Call the function to plot the data
plot_data(combined_df)