"""
Config file for PrYVO IR measurements
"""

# Path to load data from and arguments used to disriminate files loaded
root                = r"C:\Users\keena\Downloads\0222_BB"
file                = r"\0222_BB"
# file extension types
exceptions          = ["notes", "setup"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R", "References"]
# polarisations
polarisations = ["86", "100", "110", "131"]
# plot limits
limits = [17500, 16000]
# calibrate wavelength of OSA (nm)
calibration = 1.054269203603
# reference power correction
correction = 34/42
# averaging window length
window = 50