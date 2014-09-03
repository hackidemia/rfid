import sys
from time import sleep

class SerialDevice(object):
  def __init__(self, baudrate, **kwargs):
    try:
      import serial
    except ImportError:
      print "You need to install the serial module"
      sys.exit(1)

    self.baudrate = baudrate
    self.timeout = kwargs.pop("timeout", 0.1)
    self.enabled = True;

    if not hasattr(SerialDevice, 'sp'):
      SerialDevice.sp = serial.Serial("/dev/ttyUSB0", baudrate=self.baudrate, timeout=self.timeout)
    else:
      print "Another SerialDevice exists. Only one serial device may be instantiated at a time."
      self.enabled = False;

  def readline(self):
    if self.enabled:
      return SerialDevice.sp.readline()
    else:
      return ''

  def read(self, size):
    if self.enabled:
      return SerialDevice.sp.read(size)
    else:
      return ''

  def __del__(self):
    if self.enabled:
      SerialDevice.sp.close()

class ID12LA(SerialDevice):
  def __init__(self):
    SerialDevice.__init__(self, 9600)

  def get_last_scan(self):
    data = self.readline()
    if len(data) > 0:
      # Read and discard the ETX byte
      self.read(1)
      # The actual id consists of the 10 characters after the STX byte
      return data[1:11]
    else:
      return None

  def wait_for_scan(self):
    rfid = None
    while rfid == None:
      sleep(.1)
      rfid = self.get_last_scan()

    return rfid