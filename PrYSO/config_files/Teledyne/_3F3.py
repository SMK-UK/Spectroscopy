"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\keena\Downloads\03_2036_17\0203"
file                = r"\SMF"
# file extension types
exceptions          = ["notes", "setup"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R", "References"]
# polarisations
polarisations = ["FAV", "SAV"]
# plot limits
limits = [6700, 6300]
# calibrate wavelength of OSA (nm)
calibration = 1
# reference power correction
correction = 1
# averaging window length
window = 50
