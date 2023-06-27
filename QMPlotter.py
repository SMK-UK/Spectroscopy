import matplotlib.pyplot as mp
import os, re

class plotter:

    def __init__(self, x_data:list[float], y_data:list[float]):

        self.x = x_data
        self.y = y_data
        self.colour = 'tab:blue'
        self.title = 'figure'
        self.x_lbl = 'x-values (AU)'
        self.y_lbl = 'y-values (AU)'

        self.linestyle = '-'
        self.marker = None
        self.alpha = 1
        self.label = None

        self.woi: list[float] = []
        self.sec_xeq = (lambda x: x, lambda x: x)
        self.sec_yeq = (lambda x: x, lambda x: x)
        self.shift = 0

    def display(self, zoom: bool=False, sec_x: bool=False, sec_y: bool=False):
        """
        plot self.x and self.y with corresponding kwargs

        Parameters
        ----------

        zoom : choose to only display data within certain bounds
        sec_ax : display a secondary axis

        """
        self.fig, self.ax = mp.subplots()
        
        x = self.x
        y = self.y

        if zoom == True:
            x = self.zoom_x
            y = self.zoom_y
        
        if self.woi:
            for value in self.woi:
                self.ax.axvline(x=value, linestyle='-.')
        if sec_x:
            self.ax.secondary_xaxis('top', functions=(self.sec_xeq))
            self.ax.set_xlabel
        if sec_y:
            self.ax.secondary_yaxis('right', functions=(self.sec_yeq))
            self.ax.set_ylabel

        self.ax.set_title(self.title)
        self.ax.set(xlabel=self.x_lbl, ylabel=self.y_lbl)

        self.ax.plot(x, y, 'x', color=self.colour, linestyle=self.linestyle, 
                     marker=self.marker, alpha=self.alpha, label=self.label)
        self.ax.grid(True, color='silver', linewidth=0.5)

        if self.label: 
            self.ax.legend(loc='best')

        mp.show()

    def save_fig(self, file_name:str, dir=None, fmt='png', res=80):
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
        if dir == None:
            dir = os.getcwd()

        name= os.path.join(dir, file_name)
        
        self.fig.savefig(fname=name, dpi=res, format=fmt, bbox_inches='tight')

    def zoom(self, x_bounds:tuple=(), y_bounds:tuple=()):
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
        x_start = 0
        x_stop = -1
        y_start = 0
        y_stop = -1

        if x_bounds != None:
            for index, value in enumerate(self.x):
                if value <= x_bounds[0]:
                    x_start = index
                if value <= x_bounds[1]:
                    x_stop = index
           
        if y_bounds != None:
            for index, value in enumerate(self.y):
                if value <= y_bounds[0]:
                    y_start = index
                if value <= y_bounds[1]:
                    y_stop = index

        self.zoom_x = self.x[x_start:x_stop]
        self.zoom_y = self.y[y_start:y_stop]
