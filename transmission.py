import os, re
import numpy as np
import matplotlib.pyplot as mp
import scipy.interpolate as sp
import spec_funcs as sf
from scipy.fftpack import fft, fftfreq
from natsort import natsorted

# change to gui at later date
# polarisations as written in file names
polarisations = ["143", "188"]

# folder containing all the requisite subfolders and data - refrences included
path = "C:\\Users\\keena\\Desktop\\New Folder"

# choose to focus on a particular wavelength range
zoom = 1
lower = 590
upper = 610

# initialise lists
file_list = []
folder_list = []
bg_wavelengths = []
bg_Is = []
wave_sets = []
I_sets= []
I_0 = []
freq = []
OD = []
starts = []
stops = []

# holder removes first folder from lists so only actual data is used
holder = 0
# walk through directory and extract all relevant files
for root, dirs, files in os.walk(path):
    if holder == 1:
        folder_list.append(root)
        temp =[]
        for file in files:
            if(file.endswith((".csv", ".txt"))):
                # ignore collection data notes
                if "notes" in file or "setup" in file:
                    continue
                else:
                    temp.append(file)
        file_list.append(temp)
    else:
        holder = 1

'''
filter through files and seperate transmission data into groups:
polarisation > references > separators eg. temperature > transmission sets
'''
for polarisation in polarisations:
    wavelengths = []
    Is = []
    for index, folder in enumerate(folder_list):
        for file in file_list[index]:
            dataset = os.path.join(folder, file)
            if polarisation in dataset:
                # check for reference data
                # add flag if no reference!
                if "ref" in dataset or "reference" in dataset:
                    bg_temp_wave = []
                    bg_temp_I = []
                    with open(dataset, 'r', newline='') as raw_file:
                        for row in raw_file:
                            if sf.check_str(row) == True:
                                temp = re.split('\t|,|;', row)
                                bg_temp_wave.append(float(temp[0]))
                                bg_temp_I.append(float(temp[1]))
                        raw_file.close()
                    bg_wavelengths.append(bg_temp_wave)
                    bg_Is.append(bg_temp_I)
                else:
                    temp_wave = []
                    temp_I =[]
                    with open(dataset, 'r', newline='') as raw_file:
                        for row in raw_file:
                            if sf.check_str(row) == True:
                                temp = re.split('\t|,|;', row)
                                temp_wave.append(float(temp[0]))
                                temp_I.append(float(temp[1]))
                        raw_file.close()
                    wavelengths.append(temp_wave)
                    Is.append(temp_I)
    wave_sets.append(wavelengths)
    I_sets.append(Is)

    '''
interpolate reference data for each file - avoids issue of wavelength array length mismatch

'''
# cycle through polarisations
for idx_1 in range(len(polarisations)):
    temp_I_0 = []
    temp_OD = []
    # generate spline co-effs
    spline_coeffs = sp.splrep(bg_wavelengths[idx_1], bg_Is[idx_1])
    # calculate referenece for each wavelength subset
    for idx_2, wavelength in enumerate(wave_sets[idx_1]):
        temp_I_0.append(sp.splev(wavelength, spline_coeffs))
        temp_OD.append(np.log10(np.abs(temp_I_0[idx_2]/I_sets[idx_1][idx_2])))
    I_0.append(temp_I_0)
    OD.append(temp_OD)

# zoom function for wavelength range
if zoom == 1:
    for index, waves in enumerate(wave_sets):
        start = []
        stop = []
        for wave in waves:
            for idx, value in enumerate(wave):
                if value <= lower:
                    temp_start = idx
                if value <= upper:
                    temp_stop = idx
            start.append(temp_start)
            stop.append(temp_stop)
        starts.append(start)
        stops.append(stop)
elif zoom != 1:
    for index, waves in enumerate(wave_sets):
        start = []
        stop = []
        for wave in waves:
            start.append(0)
            stop.append(-1)
        starts.append(start)
        stops.append(stop)

# normaise the OD
OD_norm = OD / np.nanmax(OD)

for idx_1, polarisation in enumerate(polarisations):
    
    fig_1, ax_1 = mp.subplots(figsize=(8, 5))
    ax_1.set_title(str('Half-Wave Plate: ' + str(polarisation)))
    ax_1.set(xlabel='Wavelength (nm)', ylabel='OD Normalised')
    sec_ax = ax_1.secondary_xaxis('top', functions= (lambda x: 1e7 / x, lambda x: 1e7 / x))
    sec_ax.set_xlabel('Wavenumber (cm$^{-1}$)')
    ax_1.grid(True)
    ax_1.grid(True, color='silver', linewidth=0.5)

    shift = 0

    for idx_2, wave in enumerate(wave_sets[index]):
        lbl = os.path.split(folder_list[idx_2])
        data = OD_norm[idx_1][idx_2] + shift
        ax_1.plot(wave[start[idx_2]:stop[idx_2]], data[start[idx_2]:stop[idx_2]], color=None, marker=None, linestyle='-', alpha=0.8, label=lbl[1])
        
        shift += 0.05
    
    ax_1.legend(loc='best', fontsize=8)