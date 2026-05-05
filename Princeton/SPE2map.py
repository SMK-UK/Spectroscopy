from SPE2read import SPE2file
import numpy as np

class SPE2map:
    """Class which adapts the SPE2file class to be used in map handling programs in a standardized way. 

    Reliable attributes (standardized interface): data, exposureTime, nbOfFrames, regionSize, SPEversion and wavelength.
    
    Attributes:
        data (numpy array): numpy array containing the frames
        exposureTime (float): exposure time of each frame in seconds
        nbOfFrames (int): number of frames recorded in the file
        pyspecFile (SPE2file object): SPE2file object handling the file reading (internal)
        regionSize (tuple): size of a frame (nb of pixels along y (1 for a simple spectrum), nb of pixels along x)
        SPEversion (float): SPE version of the file (should be 2.xxx)
        wavelength (numpy array): array of floats containing the wavelengths read from the file calibration constants.
    """
    
    def __init__(self, fname=None, fid=None):
        """
        This function initializes the class and, if either a filename or fid is
            provided, opens the datafile and reads the contents.

        Parameters:
            fname (str, optional): Filename of SPE file
            fid (file, optional): File ID object of open stream (NOTE: never tested)
        """
        
        self.pyspecFile = SPE2file(fname=fname, fid=fid)
        if self.pyspecFile._fid is not None:
            self._readData()
            
    def _readData(self):
        """
        Reads the data from the SPE2file object. Internal use only.
        """
        self.wavelength = self.pyspecFile.getWavelengths()
        self.regionSize = self.pyspecFile.getSize()[1:]
        self.nbOfFrames = self.pyspecFile.getSize()[0]
        self.exposureTime = self.pyspecFile.Exposure
        self.data = self.pyspecFile.getData()
        self.SPEversion = self.pyspecFile.SPEversion

    def getSpectra(self, frame=0):
        """
        Returns the Spectra 
        """
        intensity = self.data[frame, 0, :]/self.exposureTime/1000
        wavelength = self.wavelength
        
        return wavelength, intensity