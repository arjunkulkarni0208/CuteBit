from cvzone.SerialModule import SerialObject
from time import sleep

car = SerialObject("COM11", 115200, digits=1) # Note: digits=2 for [move, emotion]

sleep(2)
packet = [1]
car.sendData(packet)
sleep(4)
packet = [0]
car.sendData(packet)