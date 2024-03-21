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
# calibrate wavelength of OSA
calibration = 1.054269203603
# reference power correction
correction = 345/50
# averaging window length
window = 50

config_params = dict(

    # Index positions for relevant column data in excel files
    
    data_indexes = dict(

    time = 0,
    sp_trans = 1,
    sp_ref = 2,
    cp_trans = 3,
    cp_ref = 4

    ),

    # Index positions for trimming the data

    trim_indexes = dict(
    
    trig                = 50026, 
    ref_off             = 300,
    off                 = 1100, 
    ramp                = 65026,

    ),

    # Guess T1 times for the data

    guess_ref_T1 = 1E-6,
    guess_T1 = 10E-6

)

