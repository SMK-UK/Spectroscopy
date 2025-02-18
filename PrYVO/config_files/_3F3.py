"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\keena\Downloads\0.5_"
file                = r"\0725_BB_IR_COL_T"
# file extension types
exceptions          = ["notes", "setup"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R", "References"]
# polarisations
polarisations = ["80", "95", "110", "125"]
# plot limits
limits = [6575, 6150]
# calibrate wavelength of OSA (nm)
calibration = 1
# reference power correction
correction = 1
# averaging window length
window = 50
