'''
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023

Functions designed to plot data
'''

from math_funcs import zoom
from numpy import linspace
import matplotlib.pyplot as mp
import os

def plot_spectra(x_data, y_data, data_indexes = [], keys = list[str], shifter: int or float=0,
            axis_lbls = None, sec_axis = True, save = False, 
            data_labels = [], lims: tuple = (), woi: list = [], res = 80):
    """
    zoom in on a particular area of interest in a dataset

    Parameters
    ----------

    data : list / array - data to perform zoom
    bounds : tuple - lower and upper bounds of the region of interest

    Returns
    -------

    start, stop : start and stop index for the zoomed data
    """

    data_lbl = None
    lower = 0
    upper = -1

    for m, key in enumerate(keys):
        fig, ax = mp.subplots()
        ax.grid(True, color='silver', linewidth=0.5)
        if axis_lbls:
            ax.set_title('Halfwave Plate: ' + key)
            ax.set(xlabel=axis_lbls[0], ylabel=axis_lbls[1])
        if sec_axis:
            sec_ax = ax.secondary_xaxis('top', functions=
                                        (lambda x: 1e7/x, lambda x: 1e7/x))
            sec_ax.set_xlabel('Wavelength (nm)')
        if woi:
            for woi_set in woi:
                for vline in woi_set[0]:
                    ax.axvline(x=vline, linestyle=woi_set[1], color=woi_set[2], linewidth='2')
        shift = 0
        for o, x in enumerate(x_data[m]):
            y = y_data[m][o] + shift
            plot_colour = mp.cm.winter(linspace(0, 1, len(x_data[m])))
            if lims:
                lower, upper = zoom(x, lims)
            if data_labels:
                data_lbl = os.path.split(data_labels[o])[1]
            ax.plot(x[lower:upper], y[lower:upper], color=plot_colour[o],
                    linestyle='-', linewidth=0.8, alpha=1, label=data_lbl)
            shift += shifter

        ax.legend(loc='best', fontsize=8)
        fig.tight_layout()

        if save:
            folder = os.path.split(data_labels[0])[0]
            region = str(round(x[lower])) + '_' + str(round(x[upper])) + '_' + key
            name = os.path.join(folder, region + '.png')

            fig.savefig(fname=name, dpi=res, format='png', bbox_inches='tight')
