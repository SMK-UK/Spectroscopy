"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\sk88\Heriot-Watt University Team Dropbox\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\Spectroscopy\Teledyne\03_2036_17"
file                = r"test"
# file extension types
exceptions          = ["notes", "setup", "ignore", "Thermal OD", "References_290K"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "References", "R"]
# polarisations
polarisations = ['FAV']
# calibrate wavelength of OSA (nm)
calibration = 1.054269203603
# reference power correction
correction = 1
# averaging window length
window = 50
# single temp file?
single = False
# numpy arrays used?
numpy = True

# plot limits 
limits = [17000, 16400]
# wavelengths of interest (1/cm)
exp_levels = ([16502, 16561, 16723, 17001, 17297], '--','green')
site_1 = ([6417, 6467, 6535, 6575, 6643, 6661, 6725], '--','red')
ir_woi = [site_1, exp_levels]

