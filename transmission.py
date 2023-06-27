'''
Spectroscopic Data Analysis
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023
'''

import spec_funcs as sf
import fit_funcs as ff

'''
Set-up script  
Select input folder and polarisation  
'''

# folder containing all the requisite subfolders and data - refrences included
path = r"C:\Users\sk88\Desktop\0222_BB"
# mark energies / wavelengths of interest
sigma_woi = [595.24]
pi_woi = [604.23, 605.36]
woi = sigma_woi + pi_woi
# calibrate wavelength of OSA
calibration = 1.054269203603
# reference power correction
correction = 150/50
# reference names
refs = ("ref", "reference", "R")
# file extension types
exts = ('.csv', '.txt', '.CSV')
exceptions = ("notes", "setup", "ignore")
# labels for plots
main_labels = 'wavelength (nm)', 'OD'

'''
Import Raw Spectroscopy Data
Load raw data from csv file (delimiter is not a problem) and sort into groups:
polarisations -> reference / spectrum
'''

folder_list, file_list = sf.dir_interogate(path, exts, exceptions)
path_names = sf.read_files(folder_list, file_list)
ref_names, data_names = sf.search_paths(path_names, refs)
polarisations = sf.find_numbers(ref_names, tail=1)
ref_data, ref_metadata = sf.data_extract(ref_names, polarisations)
data_sets, metadata_sets = sf.data_extract(data_names, polarisations)
wave_sets, od_sets = sf.OD_calc(ref_data, data_sets, correction=True, c_factor=correction)
shifted_sets = sf.data_shift(wave_sets, calibration)

'''
Main calculations
Correct OD for background
Create two data sets - corrected and subtracted 
'''

backgrounds = [[sf.bin_data(od) for od in od_set] for od_set in od_sets]
od_corrected = [[[x - mean_value for x in od] for od, mean_value in zip(od_set, background)] for od_set, background in zip(od_sets, backgrounds)]
od_ground = [od_corrected[i][0] for i in range(len(od_corrected))]
od_subtracted = [[[x-y for x, y in zip(excited, ground)] for excited in od_corrected[i]] for i, ground in enumerate(od_ground)]
minimums = [[min(od_sub) for od_sub in od_sub_set] for od_sub_set in od_subtracted]
od_subtracted =  [[[x - minimum for x in od_sub] for od_sub, minimum in zip(od_sub_set, minimum)] for od_sub_set, minimum in zip(od_subtracted, minimums)]

'''
Find Peaks and Energies
Calculate frequencies, wavenumbers and wavelengths of peaks
'''

corrected_peaks = sf.peak_find(shifted_sets, od_corrected, prom_tol=None, top_tol=0.1, lims=None)
sub_peaks = sf.peak_find(shifted_sets, od_subtracted, prom_tol=None, top_tol=0.01, lims=None)
od_frequencies = sf.peak_freq(od_corrected, shifted_sets, lims=[490, 510])
od_wavenumbers = [[[sf.converter(frequency, d_type=1, c_type=0) for frequency in frequency_set] for frequency_set in frequency_list] for frequency_list in od_frequencies]
od_wavelengths = [[[sf.converter(frequency, d_type=1, c_type=2) for frequency in frequency_set] for frequency_set in frequency_list] for frequency_list in od_frequencies]
sub_frequencies = sf.peak_freq(sub_peaks, wave_sets, lims=[490, 510])
sub_wavenumbers = [[[sf.converter(frequency, d_type=1, c_type=0) for frequency in frequency_set] for frequency_set in frequency_list] for frequency_list in sub_frequencies]
sub_wavelengths = [[[sf.converter(frequency, d_type=1, c_type=2) for frequency in frequency_set] for frequency_set in frequency_list] for frequency_list in sub_frequencies]


'''
Plot datasets
'''
# plot the corrected data
sf.plotter(shifted_sets, od_corrected, keys=polarisations, axis_lbls=main_labels, lims=(560, 620), shifter=0.1, data_indexes=corrected_peaks, woi=woi, save=False, data_labels=folder_list)
# plot the subtracted & correced data
sf.plotter(shifted_sets, od_subtracted, keys=polarisations, axis_lbls=main_labels, lims=(550, 620), shifter=0.1, data_indexes=sub_peaks, woi=woi, save=False, data_labels=folder_list)


