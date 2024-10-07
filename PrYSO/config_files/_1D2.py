"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\sk88\Heriot-Watt University Team Dropbox\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\Spectroscopy\Teledyne\03_2036_17\1909\WL"
file                = r"VIS"
# file extension types
exceptions          = ["notes", "setup", "ignore", "Thermal OD", "References_290K"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "References", "R"]
# polarisations
polarisations = ['FAV', 'SAV']
# calibrate wavelength of OSA (nm)
calibration = 1.054269203603
# reference power correction
correction = 70/32
# averaging window length
window = 50
# single temp file?
single = True
# numpy arrays used?
numpy = True


