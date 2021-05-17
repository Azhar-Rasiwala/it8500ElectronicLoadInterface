from array import array
import csv, io, time
from dcload import DCLoad

def closeFiles():
    log_file.close()
    load.TurnLoadOff()

def log(obj: object, log_writer = None):
    print(obj)
    if log_writer: 
        log_writer.write(obj.values)

#log_rate: Time between each current setpoint load 
def drawCurrent(load, log_rate, voltage):

    with io.open("current_setpoint.csv", 'r') as input_file:
        currentValue = input_file.read()

    load.SetMaxVoltage(voltage)
    load.setCCCurrent(currentValue)
    load.SetFunction("battery")
    load.TurnLoadOn()

    log_writer = csv.writer(log_file, delimiter=",")
    log_writer.writerow(["Time", "Voltage", "Current", "Power"])

    while(True):
        values = load.GetInputValues().split("\t")
        volts = values[0].replace(' V','')
        amps = values[1].replace(' A','')
        watts = values[2].replace(' W','')
        log({time: load.TimeNow(), volts:volts, amps:amps, watts:watts}, log_writer=log_writer)
        if values[4] == "0x0":
            closeFiles()
            sys.exit("Electronic Load Interface Exiting Test")
        time.sleep(log_rate)

if __name__ == "__main__":
    load = DCLoad()
    PORT = "COM4"
    BAUD = 9600
    VOLTAGE = 120 
    LOG_RATE = 1 # seconds
    load.Initialize(PORT, BAUD)

    log_file = io.open("currentLog.csv", "w+")

    #press ctrl+c to end program 
    try:
        drawCurrent(load, LOG_RATE, VOLTAGE)
    except KeyboardInterrupt:
        closeFiles()
    
    