'''
Spectroscopic Data Analysis
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023
'''

import spec_funcs as sf
import fit_funcs as ff

# folder containing all the requisite subfolders and data - refrences included
path = "C:\\Users\\sk88\\Desktop\\0215_Unpolished"
# mark energies / wavelengths of interest
woi = [595.27, 604.23, 605.40]
# reference names
refs = "ref", "reference", "R"
# file extension types
exts = (".csv", ".txt", ".CSV")
exceptions = ("notes", "setup", "ignore")