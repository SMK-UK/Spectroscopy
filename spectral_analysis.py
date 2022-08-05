from time import perf_counter as tick
import os, re
import numpy as np
import matplotlib.pyplot as mp
import scipy.interpolate as sp
import spec_funcs as sf

# change to gui at later date
polarisations = ["143", "188"]

bg_path = 'C:\\Users\\keena\\Desktop\\New Folder\\Reference'

bg_file_list = []
bg_file_name = []

for root, dirs, files in os.walk(bg_path):
    for file in files:
        if(file.endswith((".csv", ".txt"))):
            bg_file_list.append(os.path.join(root, file))
            bg_file_name.append(file)

bg_wavelength = []
bg_I = []
bg_wave_sets = []
bg_I_sets = []

for index, polarisation in enumerate(polarisations):
    for bg_loc in bg_file_list:
        bg_temp_wave = []
        bg_temp_I = []
        if polarisations[index] in bg_loc:
            with open(bg_loc, 'r', newline='') as raw_file:
                for row in raw_file:
                    if sf.check_str(row) == True:
                        temp = re.split('\t|,|;', row)
                        bg_temp_wave.append(float(temp[0]))
                        bg_temp_I.append(float(temp[1]))
                raw_file.close()
                bg_wavelength.append(bg_temp_wave)
                bg_I.append(bg_temp_I)
bg_wave_sets.append(bg_wavelength)
bg_I_sets.append(bg_I)

# change to gui at later date
path = 'C:\\Users\\keena\\Desktop\\New Folder\\Spectrum'
#path = 'C:\\Users\\keena\\Desktop\\2022_PrYVO_Spectroscopy'

file_list = []
file_name = []

for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith((".csv", ".txt"))):
            file_list.append(os.path.join(root, file))
            file_name.append(file)

folder = [extension.split(os.sep)[-2] for extension in file_list]

wave_sets = []
I_sets = []

for index, polarisation in enumerate(polarisations):
    I = []
    wavelength = []
    for loc in file_list:
        if 'setup' in loc:
            continue
        if polarisations[index] in loc:
                with open(loc, 'r', newline='') as raw_file:
                    temp_wave = []
                    temp_I = []
                    for row in raw_file:
                        if sf.check_str(row) == True:
                            temp = re.split('\t|,|;', row)
                            temp_wave.append(float(temp[0]))
                            temp_I.append(float(temp[1]))
                    raw_file.close()
                    wavelength.append(temp_wave)
                    I.append(temp_I)
    wave_sets.append(wavelength)
    I_sets.append(I)

wavenumber = [[1e7 / value for value in group] for group in wavelength]