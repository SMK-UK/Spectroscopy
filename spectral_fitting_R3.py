import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
import re
import statistics


total_peak_count = 0 

# Replace 'your_data_file.csv' with the path to your CSV file
data_file = 'C:/Users/aj2063/OneDrive - Heriot-Watt University/Documents/.Documents - Year 1/Q3/Data/spectra_fit_testing/peak_data/peak_data.csv'

# Read data from the CSV file
data = pd.read_csv(data_file, sep=',', header=0, na_values='')

# Create an empty list to store data
formatted_data = []

# Iterate through the input data
for index, row in data.iterrows():
    filename = row['filename']
    peak_num = row['peak_num']
    peaks = row['peaks']

    # If 'peaks' contains a comma, split it and treat as separate integers
    if isinstance(peaks, str) and ',' in peaks:
        peaks = [int(peak) for peak in peaks.split(', ')]
        for peak in peaks:
            formatted_data.append({'filename': filename, 'peak_num': peak_num, 'peak': peak})
    else:
        # Treat 'peaks' as a single integer
        formatted_data.append({'filename': filename, 'peak_num': peak_num, 'peak': int(peaks)})

# Create a dataframe from the formatted data
peak_pos_data = pd.DataFrame(formatted_data)




def lorentzian(x, x0, a, gam):
    return a * gam**2 / (gam**2 + (x - x0)**2)

def fit_multi_lorentzian_and_plot(csv_file, num_peaks, initial_guesses, wavelength_range=None):
    global total_peak_count
    data = pd.read_csv(csv_file, header=None, names=['wavelength', 'intensity'])
    wavelength = data['wavelength']
    intensity = data['intensity']

    # Select a subset of the data based on the specified wavelength range
    if wavelength_range:
        mask = (wavelength >= wavelength_range[0]) & (wavelength <= wavelength_range[1])
        wavelength = wavelength[mask]
        intensity = intensity[mask]

    # Calculate the average intensity between 700 and 800 nm
    avg_intensity = np.mean(intensity[(wavelength >= 700) & (wavelength <= 800)])

    # Subtract the average intensity from the entire dataset to normalize
    intensity -= avg_intensity

    # Initialize parameters and fitting for each peak
    fit_params = []
    peak_info = []  # List to store peak information

    for i in range((num_peaks)):

        x0 = initial_guesses[total_peak_count]
        x_min = x0 - 3
        x_max = x0 + 3
        y_values_in_range = []
        for x, y in zip(wavelength, intensity):
            if x_min <= x <= x_max:
                y_values_in_range.append(y)
       
        max_y = max(y_values_in_range)
        half_max_y = max_y / 2
        closest_x = None
        min_diff = float('inf')

        # Iterate through the data points in the range to find the x value
        for x, y in zip(wavelength, intensity):
            if x_min <= x <= x_max:
                diff = abs(y - half_max_y)
                if diff < min_diff:
                    min_diff = diff
                    closest_x = x
        x_width = (x0 - closest_x) 
        if x_width > 1:
            x_width = 1   

        p0=[x0, max_y, x_width]
        # print(p0)
        params, _ = curve_fit(lorentzian, wavelength, intensity, p0=p0, maxfev=1000000)
        fit_params.append(params)
        # peak information
        filename_reduced = filename.split('_', 1)[0]
        print(f'{filename_reduced}, Peak {i + 1}: x0={params[0]:.2f}, width={params[2]:.2f}')
        peak_info.append(f'{filename_reduced}, Peak {i + 1}: x0={params[0]:.2f}, width={params[2]:.2f}')
        total_peak_count += 1

    # Plot the data and the fitted Lorentzian peaks
    plt.figure(figsize=(10, 6))
    plt.plot(wavelength, intensity, 'bo', label='Data')

    for i in range(num_peaks):
        plt.plot(wavelength, lorentzian(wavelength, *fit_params[i]), label=f'Peak {i + 1}')
        plt.text(fit_params[i][0], max(intensity) * 0.9, f'x0={fit_params[i][0]:.2f}, width={fit_params[i][2]:.2f}', fontsize=10, ha='center')

    plt.legend()
    plt.xlabel('Wavelength')
    plt.ylabel('Intensity')

    # Save the plot
    plot_filename = os.path.splitext(os.path.basename(csv_file))[0] + '_fit.png'
    plt.savefig(os.path.join(directory_path, plot_filename), dpi=300)
    plt.close()
    
    return peak_info


# Directory containing CSV files
directory_path = 'C:/Users/aj2063/OneDrive - Heriot-Watt University/Documents/.Documents - Year 1/Q3/Data/spectra_fit_testing'







## Example: Fitting two peaks with initial guess parameters for each peak
# num_peaks = 2
# initial_guesses = [[882, 0.8, 1], [958, 0.6, 1]]  # Initial guess for two peaks - [lambda, amplitude, width]
num_peaks = peak_pos_data['peak_num'].tolist()
initial_guesses = peak_pos_data['peak'].tolist()

all_peak_info = []  # List to store peak information from all files



for filename in os.listdir(directory_path):
    file_names = [f for f in os.listdir(directory_path) if f.endswith('_spectra.csv')]
    file_names = sorted(file_names)     #sort them alphabetically. 
    if filename.endswith('_spectra.csv'):
        file_path = os.path.join(directory_path, filename)
        peak_info = fit_multi_lorentzian_and_plot(file_path, num_peaks[total_peak_count], initial_guesses, wavelength_range=(700, 1000))
        # file_index += 1  # Increment the current file index

        for info in peak_info:
            match = re.search(r'([^,]+), Peak (\d+): x0=([\d.]+), width=([\d.]+)', info)
            if match:
                filename, peak, x0, width = match.groups()
                all_peak_info.append([filename, int(peak), float(x0), float(width)])
                




# Convert peak information to a DataFrame
peak_info_df = pd.DataFrame(all_peak_info, columns=['Filename', 'Peak', 'x0', 'Width'])

# Save peak information to a CSV
peak_info_df.to_csv(os.path.join(directory_path, 'peak_info.csv'), index=False)

# max_width = max(peak_info_df['Width'])
# width_LQ = max_width*0.2
# width_LMQ = max_width*0.4
# width_UMQ = max_width*0.6
# width_UQ = max_width*0.8

# print(width_LQ)

# color_map = {
#     'width_LQ': 'r',  # Red for width 0.5
#     'width_LMQ': 'g',  # Green for width 0.7
#     'width_UMQ': 'b',  # Blue for width 0.8
#     'width_UQ': 'y',  # Yellow for width_UQ
#     # Define colors for other width ranges based on your data
# }

# # Create a figure and two subplots
# fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# # Create color-coded histogram for 'x0'
# for width in color_map:
#     filtered_x0 = peak_info_df['x0'][peak_info_df['Width'] == width]
#     axes[0].hist(filtered_x0, bins=20, color=color_map[width], label=f'Width {width}', alpha=0.5)

# axes[0].set_xlabel('Peak Position (x0)')
# axes[0].set_ylabel('Frequency')
# axes[0].set_title('Wavelength Position Histogram')
# axes[0].legend()

# # Calculate the mode, mean, and standard deviation for the 'Width' column
# width_mode = statistics.mode(peak_info_df['Width'])
# width_mean = peak_info_df['Width'].mean()
# width_std = peak_info_df['Width'].std()

# print(f"Mode of Width: {width_mode:.2f}")
# print(f"Mean of Width: {width_mean:.2f}")
# print(f"Standard Deviation of Width: {width_std:.2f}")

# # Create color-coded histogram for 'Width'
# for width in color_map:
#     filtered_width = peak_info_df['Width'][peak_info_df['Width'] == width]
#     axes[1].hist(filtered_width, bins=10, color=color_map[width], label=f'Width {width}', alpha=0.5)

# axes[1].set_xlabel('Peak Width')
# axes[1].set_ylabel('Frequency')
# axes[1].set_title('Peak Width Histogram')
# axes[1].legend()

# plt.show()











# Create a histogram of peak positions ('x0')
plt.figure(1)
plt.hist(peak_info_df['x0'], bins=40)  # You can adjust the number of bins as needed
plt.xlabel('Peak Position (x0)')
plt.ylabel('Frequency')
plt.title('Wavelength Position Histogram')

# Calculate the mode, mean, and standard deviation for the 'Width' column
width_mode = statistics.mode(peak_info_df['Width'])
width_mean = peak_info_df['Width'].mean()
width_std = peak_info_df['Width'].std()

print(f"Mode of Width: {width_mode:.2f}")
print(f"Mean of Width: {width_mean:.2f}")
print(f"Standard Deviation of Width: {width_std:.2f}")

# Create a histogram of peak widths
plt.figure(2)
plt.hist(peak_info_df['Width'], bins=10)  # You can adjust the number of bins as needed
plt.xlabel('Peak Width')
plt.ylabel('Frequency')
plt.title('Peak Width Histogram')


plt.show()

