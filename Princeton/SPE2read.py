#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 16:18:39 2016

@author: raphaelproux

This library allows to read SPE2 files produced by Princeton Instruments WinSpec software (old spectrometers).

Partly based on pyspec package by (c) Stuart B. Wilkins 2010
Adapted to specific use for a map
(A map is a series of frames with one region of interest only)

This is a python 3 library tested with python 3.6 - RProux 17/10/2017


IMPORTANT NOTE: needs the xmltodict package to work. 
If not installed install it using PIP typing "pip install xmltodict" in a terminal

"""

import numpy as np
import time

class SPE2file():
    """First note: you probably should use the SPE2map class below which provides a standardized interface to the data.

    Class to read SPE2 files from Princeton CCD cameras
    -------- EXTRACTED FROM THE PYSPEC PACKAGE 11/2016 --------
    R. Proux 15/11/2016 added readWavelengths() and self.SPEversion in _readHeader()

    Most of the attributes documented below are copy/pasted from the SPE file specification. 
    Look in a WinSpec manual (version > 2.5) for more details.
    
    Attributes:
        AbsorbLive (short): On/Off
        AbsorbMode (WORD): Reference Strip or File
        ADCBitAdj (WORD): ADC bit adjust
        ADCOffset (WORD): ADC offset
        ADCRate (WORD): ADC rate
        ADCRes (WORD): ADC resolution
        ADCType (WORD): ADC type
        allROI (int16): Probably nothing (ROIs not supported)
        AmpHiCapLowNoise (WORD): Amp Switching Mode
        CanDoVirtualChip (short): T/F Cont/Chip able to do Virtual Chip
        ControllerVersion (short): hardware version
        DATASTART (int): constant, number of bytes to the end of header (start of data)
        DATEMAX (int): constant, number of characters describing the date
        DelayTime (float): Used with Async Mode
        DetectorType (short): CCD/DiodeArray type
        DetTemperature (float): Detector Temperature Set
        Exposure (float): alternative exposure, in sec.
        fname (str): filename 
        Gain (WORD): gain
        GeometricOps (WORD): geometric ops: rotate 0x01, reverse 0x02, flip 0x04
        LogicOutput (short): definition of output BNC
        NCOMMENTS (int): constant, number of comments to read
        NumROI (int): number of ROIs used. if 0 assume 1.
        NumROIExperiment (int): May be more than the 10 allowed in this header (if 0, assume 1)
        ShutterControl (WORD): Normal, Disabled Open, Disabled Closed.
        SPEversion (float): version of this file header
        TEXTCOMMENTMAX (int): number of characters in a comment.
        ThresholdMax (float): Threshold maximum value
        ThresholdMaxLive (short): On/Off
        ThresholdMin (float): Threshold minimum value
        ThresholdMinLive (short): On/Off
        TIMEMAX (int): constant, number of characters describing the time
        TimingMode (short): Timing mode
        TriggerDiode (short): Trigger diode
    """

    TEXTCOMMENTMAX = 80
    DATASTART = 4100
    NCOMMENTS = 5
    DATEMAX = 10
    TIMEMAX = 7
    
    def __init__(self, fname=None, fid=None):
        """
        This function initializes the class and, if either a filename or fid is
            provided, opens the datafile and reads the contents.

        Parameters:
            fname (str, optional): Filename of SPE file
            fid (file, optional): File ID object of open stream (NOTE: never tested)
        """
        
        self._fid = None
        self.fname = fname
        if fname is not None:
            self.openFile(fname)
        elif fid is not None:
            self._fid = fid

        if self._fid:
            self.readData()
            self._fid.close()

    def __str__(self):
        """Provide a text representation of the file.
        
        Returns:
            str: string representation of the measurements' characteristics.
        """
        s =  "Filename      : %s\n" % self.fname
        s += "Data size     : %d x %d x %d\n" % (self._size[::-1])
        s += "CCD Chip Size : %d x %d\n" % self._chipSize[::-1]
        s += "File date     : %s\n" % time.asctime(self._filedate)
        s += "Exposure Time : %f\n" % self.Exposure
        s += "Num ROI       : %d\n" % self.NumROI
        s += "Num ROI Exp   : %d\n" % self.NumROIExperiment
        s += "Contoller Ver.: %d\n" % self.ControllerVersion
        s += "Logic Output  : %d\n" % self.LogicOutput
        s += "Timing Mode   : %d\n" % self.TimingMode
        s += "Det. Temp     : %d\n" % self.DetTemperature
        s += "Det. Type     : %d\n" % self.DetectorType
        s += "Trigger Diode : %d\n" % self.TriggerDiode
        s += "Delay Time    : %d\n" % self.DelayTime
        s += "Shutter Cont. : %d\n" % self.ShutterControl
        s += "Absorb Live   : %d\n" % self.AbsorbLive
        s += "Absorb Mode   : %d\n" % self.AbsorbMode
        s += "Virtual Chip  : %d\n" % self.CanDoVirtualChip
        s += "Thresh. Min L : %d\n" % self.ThresholdMinLive
        s += "Thresh. Min   : %d\n" % self.ThresholdMin
        s += "Thresh. Max L : %d\n" % self.ThresholdMaxLive
        s += "Thresh. Max   : %d\n" % self.ThresholdMax
        s += "Geometric Op  : %d\n" % self.GeometricOps
        s += "ADC Offset    : %d\n" % self.ADCOffset
        s += "ADC Rate      : %d\n" % self.ADCRate
        s += "ADC Type      : %d\n" % self.ADCType
        s += "ADC Resol.    : %d\n" % self.ADCRes
        s += "ADC Bit. Adj. : %d\n" % self.ADCBitAdj
        s += "ADC Gain      : %d\n" % self.Gain
        
        i = 0
        for roi in self.allROI:
            s += "ROI %-4d      : %-5d %-5d %-5d %-5d %-5d %-5d\n" % (i,roi[0], roi[1], roi[2],
                                                                  roi[3], roi[4], roi[5])
            i += 1
        
        s += "\nComments :\n"
        i = 0
        for c in self._comments:
            s += "%-3d : " % i
            i += 1
            s += c
            s += "\n"
        return s

    def __getitem__(self, n):
        """
        Return the array with zdimension n
        This method can be used to quickly obtain a 2-D array of the data
        
        Args:
            n (int): get nth frame in the data
        
        Returns:
            numpy array: the nth frame of the data (1D array)
        """
        return self._array[n]

    def getData(self):
        """Return the array of data
        
        Returns:
            numpy array: the complete data array (2D array)
        """
        return self._array

    def getBinnedData(self):
        """Return the binned (sum of all frames) data
        
        Returns:
            numpy array: the sum of all frames (1D array)
        """
        return self._array.sum(0)

    def readData(self):
        """Read all the data into the class"""
        self._readHeader()
        self._readSize()
        self._readComments()
        self._readAllROI()
        self._readDate()
        self._readWavelengths()
        self._readArray()

    def openFile(self, fname):
        """Open a SPE file"""
        self._fname = fname
        self._fid = open(fname, "rb")

    def getWavelengths(self):
        """Return the wavelengths vector.
        
        Returns:
            numpy array: wavelengths vector for the file
        """
        return self._wavelengths

    def getSize(self):
        """Return a tuple of the size of the data array
        
        Returns:
            tuple: size of data array (nb of frames, nb of pixels on y axis (1 for simple spectra), nb of pixels on x axis)  
        """
        return self._size
    def getChipSize(self):
        """Return a tuple of the size of the CCD chip
        
        Returns:
            tuple: size of CCD chip (nb of pixels on y axis, nb of pixels on x axis)
        """
        return self._chipSize
    def getVirtualChipSize(self):
        """
        Return the virtual chip size
        
        Returns:
            tuple: size of virtual chip (nb of pixels on y axis, nb of pixels on x axis)
        """
        return self._vChipSize

    def getComment(self, n=None):
        """
        Return the comments in the data file.
        
        Args:
            n (int, optional): If n is not provided (default None), then all the comments 
            are returned as a list of string values. If n is provided then the n'th comment is returned.
        
        Returns:
            list or str: comments in a list of strings, or simple string if nth comment selected.
        """
        
        if n is None:
            return self._comments
        else:
            return self._comments[n]

    def _readAtNumpy(self, pos, size, ntype):
        """
        Reads a number from the file.
        
        Args:
            pos (int): Position in the file in bytes
            size (int): Number of elements to read (-1 for all items)
            ntype (data-type): Type of number (number of bytes to read = sizeof(ntype) * size)
        
        Returns:
            number or numpy array: numpy array of read numbers if several numbers (size > 1). Simple number otherwise.
        """
        self._fid.seek(pos)
        return np.fromfile(self._fid, ntype, size)

    def _readAtString(self, pos, size):
        """
        Reads a string from the file.
        
        Args:
            pos (int): Position in the file in bytes.
            size (int): Number of characters to be read (-1 for all characters)
        
        Returns:
            str: string read from file.
        """
        self._fid.seek(pos)
        return str(self._fid.read(size).rstrip(chr(0).encode('ascii')), encoding='utf-8')

    def _readInt(self, pos):
        """
        Reads one integer from the file
        
        Args:
            pos (int): Position in the file in bytes
        
        Returns:
            int: integer number read from the file.
        """
        return self._readAtNumpy(pos, 1, np.int16)[0]
    
    def _readFloat(self, pos):
        """Reads one float from the file
        
        Args:
            pos (int): Position in the file in bytes
        
        Returns:
            float: float number read from the file.
        """
        return self._readAtNumpy(pos, 1, np.float32)[0]

    def _readHeader(self):
        """
        This routine contains all other information
        """
        self.ControllerVersion = self._readInt(0)
        self.LogicOutput = self._readInt(2)
        self.AmpHiCapLowNoise = self._readInt(4)
        self.TimingMode = self._readInt(8)
        self.Exposure = self._readFloat(10) * 1000.
        self.DetTemperature = self._readFloat(36)
        self.DetectorType = self._readInt(40)
        self.TriggerDiode = self._readInt(44)
        self.DelayTime = self._readFloat(46)
        self.ShutterControl = self._readInt(50)
        self.AbsorbLive = self._readInt(52)
        self.AbsorbMode = self._readInt(54)
        self.CanDoVirtualChip = self._readInt(56)
        self.ThresholdMinLive = self._readInt(58)
        self.ThresholdMin = self._readFloat(60)
        self.ThresholdMaxLive = self._readInt(64)
        self.ThresholdMax = self._readFloat(66)
        self.ADCOffset = self._readInt(188)
        self.ADCRate = self._readInt(190)
        self.ADCType = self._readInt(192)
        self.ADCRes = self._readInt(194)
        self.ADCBitAdj = self._readInt(196)
        self.Gain = self._readInt(198)
        self.GeometricOps = self._readInt(600)
        
        # added
        self.SPEversion = self._readFloat(1992)

    def _readAllROI(self):
        """
        Determines the number of ROIs. However, note this library does not support multiple ROIs (untested and not likely!!).
        """
        self.allROI = self._readAtNumpy(1512, 60, np.int16).reshape(-1,6)
        self.NumROI = self._readAtNumpy(1510, 1, np.int16)[0]
        self.NumROIExperiment = self._readAtNumpy(1488, 1, np.int16)[0]
        if self.NumROI == 0:
            self.NumROI = 1
        if self.NumROIExperiment == 0:
            self.NumROIExperiment = 1
    
    def _readDate(self):
        """
        Reads the date of the measurement from the file.
        """
        _date = self._readAtString(20, self.DATEMAX)
        _time = self._readAtString(172, self.TIMEMAX)
        self._filedate = time.strptime(_date + _time, "%d%b%Y%H%M%S")
        
    def _readSize(self):
        """
        Reads all the size records of the header (data size, chip size, virtual chip size if ROIs) 
        and determines the recorded data type.
        
        Raises:
            Exception: If the data type is not known.
        """
        xdim = self._readAtNumpy(42, 1, np.int16)[0]
        ydim = self._readAtNumpy(656, 1, np.int16)[0]
        zdim = self._readAtNumpy(1446, 1, np.uint32)[0]
        dxdim = self._readAtNumpy(6, 1, np.int16)[0]
        dydim = self._readAtNumpy(18, 1, np.int16)[0]
        vxdim = self._readAtNumpy(14, 1, np.int16)[0]
        vydim = self._readAtNumpy(16, 1, np.int16)[0]
        dt = np.int16(self._readAtNumpy(108, 1, np.int16)[0])
        data_types = (np.float32, np.int32, np.int16, np.uint16)
        if (dt > 3) or (dt < 0):
            raise Exception("Unknown data type")
        self._dataType = data_types[dt]
        self._size = (zdim, ydim, xdim)
        self._chipSize = (dydim, dxdim)
        self._vChipSize = (vydim, vxdim)
        
    def _readComments(self):
        """
        Reads all the comments. Class internal use only, please use the getComment() getter method to access them.
        """ 
        self._comments = []
        for n in range(5):
            self._comments.append(
                self._readAtString(200 + (n * self.TEXTCOMMENTMAX), self.TEXTCOMMENTMAX))

    def _readArray(self):
        """
        Reads the data array. Class internal use only, please use the getData() getter method to access the data.
        """
        self._fid.seek(self.DATASTART)
        self._array = np.fromfile(self._fid, dtype=self._dataType, count=-1)
        self._array = self._array.reshape(self._size)
        
    def _readWavelengths(self):
        """
        Calculates the wavelength vector using the calibration coefficients recorded in the file. 
        Class internal use only, please use the getWavelength() getter method to access the data.
        """
        polyCoeffs = self._readAtNumpy(3263, 6, np.double)
        self._wavelengths = np.poly1d(polyCoeffs[::-1])(np.array(range(self._size[2])))