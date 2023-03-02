import OCServo as oc
from OCServo import serial_ports

servo = oc.OCServo(serial_ports()[0])

servo.send(1, 0)
servo.syncsend([1, 2], [90, -90])