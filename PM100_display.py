import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import matplotlib as mp
import os, re

class PM100_Display:

    def __init__(self, dir, fname):

        self.path = os.path.join(dir, fname)
        pow_data = pd.read_csv(path, header=12, delimiter=';')
        self.pow_times = list(pow_data['Time of day (hh:mm:ss) '])
        pow_1 = [x.replace(',','.') for x in pow_data['Power (W)']]
        pow_1_float = [float(x) for x in pow_1]
        self.pow_1_mw = [x*1e3 for x in pow_1_float]
        if 'Power (W).1' in pow_data.columns.tolist():
           pow_2 = [x.replace(',','.') for x in pow_data['Power (W).1']]
           pow_2_float = [float(x) for x in pow_2]
           self.pow_2_mw = [x*1e3 for x in pow_2_float]

    def power_plot(self, dbl_plt=False, wavelength:list=[], optional:list=[]):

        fig, ax = plt.subplots()

        ax.plot(self.pow_times, self.pow_1_mw, 'b', label=wavelength[0])
        ax.set_ylabel(wavelength[0] + ' Power (mW) ' + optional[0], color='b')
        ax.set_xlabel('Time (hh:mm:ss)')

        if self.pow_2_mw:
            ax_twn = ax.twinx()
            ax_twn.plot(self.pow_times, self.pow_2_mw,'r', label=wavelength[1])
            ax_twn.set_ylabel(wavelength[1] + 'Power (mW) ' + optional[1],color='r')
        
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2000))
        ax.xaxis.set_tick_params(labelrotation=45)

        fig.autofmt_xdate()

        plt.title(optional[2])
        plt.xlabel('Date')