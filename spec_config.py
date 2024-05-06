"""
Config file for spectroscopy measurements

"""
# Path to load data from and arguments used to disriminate files loaded
root                = "C:/Users/keena/Desktop"
file                = "0222_BB"
# file extension types
exceptions          = ["notes", "setup", "ignore", "Thermal OD"]
extensions          = ['.csv', '.txt', '.CSV']
# reference names
refs                = ["ref", "reference", "R"]
# calibrate wavelength of OSA (nm)
calibration = 1.054269203603
# reference power correction
correction = 345/50
# averaging window length
window = 50

# Wavelengths of interest

woi = dict(

    a = 1,

),

data_indexes = dict(

    time = 0,
    sp_trans = 1,
    sp_ref = 2,
    cp_trans = 3,
    cp_ref = 4

)


