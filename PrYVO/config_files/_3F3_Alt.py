"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\keena\Downloads\0.5_"
file                = r"\0824_BB_IR_COL_T"
# file extension types
exceptions          = ["notes", "setup"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R", "References"]
# polarisations
polarisations = ["95", "110", "125", "140"]
# plot limits
limits = [7100, 6200]
# calibrate wavelength of OSA (nm)
calibration = 1
# reference power correction
correction = 1
# averaging window length
window = 50