"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\keena\Desktop"
file                = r"\0203"
# file extension types
exceptions          = ["notes", "setup"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R", "References"]
# polarisations
polarisations = ["FAV", "SAV"]
# plot limits
limits = [17500, 16000]
# calibrate wavelength of OSA (nm)
calibration = 1.054269203603
# reference power correction
correction = 34/42
# averaging window length
window = 50