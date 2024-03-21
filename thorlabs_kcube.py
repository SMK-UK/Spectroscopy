"""Main module."""
#class for thorlabs motorized waveplate and stepper motor controller (KCube)

import os
import time
import sys
from tkinter.tix import Control

try:
    import clr
except Exception as e:
    print(e)
    print("please install pythonnet with:        pip install pythonnet")


KinesisDir = "C:\\Program Files\\Thorlabs\\Kinesis" #Input the directory for the kinesis folder in format of given example

clr.AddReference(KinesisDir + "\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference(KinesisDir + "\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference(KinesisDir + "\\Thorlabs.MotionControl.KCube.DCServoCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal 
from dataclasses import dataclass


class Kcube101:
    def __init__(self,devicename,serial_no,homeMotor = True):
        DeviceManagerCLI.BuildDeviceList()
        #super().__init__()
        self.device = KCubeDCServo.CreateKCubeDCServo(serial_no)
        self.serial_no = str(serial_no) # Replace this line with your device's serial number - controller (0)
        self.devicename = devicename #polarization stage = 'PRM1-MZ8',"MTS25-MZ8" for linear stage

        self.device.Connect(self.serial_no) # connect
        
        # Ensure that the device settings have been initialized
        if not self.device.IsSettingsInitialized():
            self.device.WaitForSettingsInitialized(10000) # 10 sec timeout
            assert self.device.IsSettingsInitialized() is True

        self.device_info = self.device.GetDeviceInfo() #Get Controller Device Information and display description
        print(self.device_info.Description)
        self.dev_deviceNumber = self.device_info.DeviceType
        #self.propertylist = self.device.MotorDeviceSettings.FullPropertyList DOESNT WORK
        #print(self.propertylist)
        self.device.StartPolling(50)
        self.load_setconfig_device()
        print('KCube controller is initialized')
        self.load_device_properties()
        self.JogParametersBase = JogParametersBase
        if homeMotor == True:
            self.home_motor()
        elif homeMotor == False:
            pass


    def start_polling(self,timems):
        # Start polling and enable channel
        self.device.StartPolling(timems) # 50 ms polling rate
        time.sleep(.1)
        self.device.EnableDevice()
        time.sleep(.1)

    def load_setconfig_device(self):
        #Load any configuration settings needed by the controller/stage
        config = self.device.LoadMotorConfiguration(self.serial_no,DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        # Get parameters related to homing/zeroing/moving
        #device_settings = ThorlabsInertialMotorSettings.GetSettings(config)

        config.DeviceSettingsName = str(self.devicename)
        config.UpdateCurrentConfiguration()
        self.device.SetSettings(self.device.MotorDeviceSettings,True,False)

    def load_device_properties(self): #stores device settings for easy access
        self.motorlimits = self.device.get_AdvancedMotorLimits()
        self.maxLength_mm =  float(str(self.motorlimits.LengthMaximum))
        self.maxLength_deviceUnit =  int(str(self.motorlimits.LengthMaximum_DeviceUnit))
        self.minLength_mm =  float(str(self.motorlimits.LengthMaximum))
        self.minLength_deviceUnit =  int(str(self.motorlimits.LengthMaximum_DeviceUnit))
        self.maxAcceleration_mm = float(str(self.motorlimits.get_AccelerationMaximum()))
        self.maxAcceleration_deviceUnit = int(str(self.motorlimits.get_AccelerationMaximum_DeviceUnit()))
        self.maxVelocity_mm = float(str(self.motorlimits.get_VelocityMaximum()))
        self.maxVelocity_deviceUnit = int(str(self.motorlimits.get_VelocityMaximum_DeviceUnit()))
        self.velocityUnit = self.motorlimits.get_VelocityUnits()
        self.accelerationUnit = self.motorlimits.get_AccelerationUnits()

    def home_motor(self):
        print('Homing Motor')
        self.device.Home(60000) #in ms



    def move_to_position(self,position,silent=False):
        """
        position: float
        silent: Boolean, silence the output of function

		moves to given position
		
		Returns:
			none
		"""
        if silent is not False:
            pass
        else:
            print('Moving Motor')
        self.device.SetMoveAbsolutePosition(Decimal(position)) 
        self.device.MoveAbsolute(60000)
        if silent is not None:
            pass
        else:
            print('Move complete')

    def move_to_position_deviceUnits(self,position):
        self.device.SetMoveAbsolutePosition_DeviceUnit(position)
        self.device.MoveAbsolute(60000)

    def get_absolute_position(self):
        position = self.device.GetMoveAbsolutePosition(60000)
        print('position = ' + str(position ))
        return theta
    
    def get_position(self):
        """
        finds current position of device
		
		Returns:
			position: Decimal
		"""
        position = self.device.get_Position()
        print('current position is ' + str(position))
        return position
    
    def get_jogparams(self):
        """
        gets the jog parameters which can be set to required settings

        example:
            jog_params = self.device.GetJogParams()
            jog_params.StepSize = Decimal(stepsize)
            jog_params.MaxVelocity = Decimal(maxspeed)
            jog_params.JogMode = JogParamtersBase.JogModes.SingleStep
		
		Returns:
			object: jog_params
		"""
        self.jog_params = self.device.GetJogParams()
        return self.jog_params
    
    def set_jogparams(self,jog_params=None):
        if jog_params is None:
            self.device.SetJogParams(self.jog_params)
        else:
            self.jog_params = jog_params
            self.device.SetJogParams(jog_params)
    
    def set_jog_velocityAcceleration_settings(self, maxVelocity,maxAcceleration=None,velocity_params=None):
        """
        sets the velocity object withing the jog object. required to change if the velocity settings for the jog are to be changed
        same structure as the normal velocity params object, by default sets it to the chossen settigns of the device
		"""
        jog_params = self.device.GetJogParams()
        
        if velocity_params is not None:
            jog_params.VelocityParams = velocity_params
        elif maxVelocity  > self.maxVelocity_mm: 
            print("ERROR - velocity larger than possible values")
        elif maxAcceleration is not None:
            if maxAcceleration > self.maxAcceleration_mm:
                print("ERROR - acceleration larger than possible values") 
        else:
            jog_params.VelocityParams.set_MaxVelocity(Decimal(maxVelocity))
            if maxAcceleration is not None:
                jog_params.VelocityParams.set_Acceleration(Decimal(maxAcceleration))

        self.device.SetJogParams(self.jog_params)

    def start_jog(self,wait_time=0):
        """
        wait_time: int, in milliseconds
		perform a jog of set parameters
		
		Returns:
			none
		"""
        self.device.MoveJog(MotorDirection.Forward,wait_time)
        
    # def jog_positions_singleStep(self,start,end,StepSize,Maxspeed,displaymode=True):
    #     """
	# 	perform a jog of given parameters
		
	# 	Returns:
	# 		none
	# 	"""
    #     self.jog_params = self.device.GetJogParams()
    #     self.jog_params.StepSize = Decimal(StepSize)
    #     self.jog_params.MaxVelocity = Decimal(Maxspeed)
    #     self.jog_params.JogMode = JogParametersBase.JogModes.SingleStep
    #     self.device.SetJogParams(jog_params)
    #     print('Moving motor')
    #     self.device.MoveJog(MotorDirection.Forward,60000)
    #     time.sleep(.25)
    #     if displaymode == True:
    #         while self.IsDeviceBusy():
    #             print(f'{self.device.Position}')

    def get_velocityAcceleration_settings(self): 
        """
		getter function for the velocity parameters object containing all the device settings, change and input into the set velocity paramaeters for more precise control
		
		Returns:
			object: velocity parameters
		"""
        velocity_params = self.device.GetVelocityParams()
        return velocity_params
    
    def set_velocityAcceleration_settings(self, maxVelocity,maxAcceleration=None,velocity_params=None): #inputs as floats the max velocity and acceleration in units of mm/s and mm/s/s, option of inputing object directly
        """
		setter function for the velocity parameters object. option to quickly set the max velocity by inputting a flaot or to give the velocity_params object from getter function. Also changes the jog velocity parameters
		
		Returns:
			none
		"""
        if velocity_params is not None:
            self.device.SetVelocityParams(velocity_params) #takes object from self.device.GetVelocityParams()
        elif maxVelocity  > self.maxVelocity_mm: 
            print("ERROR - velocity larger than possible values")
        elif maxAcceleration is not None:
            if maxAcceleration > self.maxAcceleration_mm:
                print("ERROR - acceleration larger than possible values") 
        else:
            velocity_params = self.device.GetVelocityParams()
            velocity_params.MaxVelocity  = Decimal(maxVelocity) #converts to Decimal format as is used by Thorlabs Kinesis
            if maxAcceleration is not None:
                velocity_params.Acceleration = Decimal(maxAcceleration)
            self.device.SetVelocityParams(velocity_params)


    def is_deviceRunning(self):
        return self.device.IsDeviceBusy()
    
    def turn_off(self):
        self.device.StopPolling()
        self.device.Disconnect()
        print('Device disconnected')