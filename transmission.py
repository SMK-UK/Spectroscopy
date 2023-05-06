'''
Spectroscopic Data Analysis
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023
'''

import spec_funcs as sf
import fit_funcs as ff

# folder containing all the requisite subfolders and data - refrences included
path = r"C:\Users\sk88\Desktop\0222_BB"
# mark energies / wavelengths of interest
woi = [595.24, 604.23, 605.36]
# calibrate wavelength of OSA
calibration = 1.054269
# reference names
refs = "ref", "reference", "R"
# file extension types
exts = (".csv", ".txt", ".CSV")
exceptions = ("notes", "setup", "ignore")

# Load raw data from text or csv file (delimiter is not a problem) and sort into groups - polarisations -> reference / spectrum
folder_list, file_list = sf.dir_interogate(path, exts, exceptions)
path_names = sf.read_files(folder_list, file_list)
ref_names, data_names = sf.search_paths(path_names, refs)
polarisations = sf.find_numbers(ref_names, tail=1)
# extract reference and transmission data
ref_data, ref_metadata = sf.data_extract(ref_names, polarisations)
data_sets, metadata_sets = sf.data_extract(data_names, polarisations)
# calulate the OD and separate x and y components
wave_sets, OD_sets = sf.OD_calc(ref_data, data_sets, correction=True, c_factor=1)
# shift data depending on calibration of OSA
shifted_sets = sf.data_shift(wave_sets, calibration)
# plot data
labels = 'wavelength (nm)', 'OD'
sf.plotter(shifted_sets, OD_sets, keys=polarisations, axis_lbls=labels, lims=[560, 620], shifter=1, woi=woi, save=True, data_labels=folder_list)