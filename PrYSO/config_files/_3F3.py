"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\sk88\Heriot-Watt University Team Dropbox\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\Spectroscopy\Teledyne\03_2036_17\1909\WL"
file                = r"IR"
# file extension types
exceptions          = ["notes", "setup", "ignore", "Thermal OD"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R"]
# polarisations
polarisations = ['FAV', 'SAV']
# calibrate wavelength of OSA (nm)
calibration = 1
# reference power correction
correction = 1
# averaging window length
window = 50
# single temp file?
single = False
# numpy arrays used?
numpy = False

# plot limits 
limits = [6750,6300]
# wavelengths of interest (1/cm)
exp_levels = ([6459, 6554, 6568, 6639], '--','green')
theory_levels = ([6417, 6467, 6535, 6575, 6643, 6661, 6725], '--','blue')
ir_woi = [theory_levels, exp_levels]

