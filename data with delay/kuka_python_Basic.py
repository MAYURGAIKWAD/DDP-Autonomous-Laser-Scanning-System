import numpy as np
import pandas as pd
from py_openshowvar import openshowvar
client = openshowvar("172.31.1.147",7000)
print (client.can_connect)


################# PREREQUISITES #################

Vel = client.read("$OV_PRO", debug=False)   # Automatic speed, not manual speed from smart pad
Vel_dec = Vel.decode('utf-8')               # $ shows System variables

axis = client.read("$AXIS_ACT", debug=False)
axis_dec = axis.decode('utf-8')
client.write("COM_E6AXIS",axis_dec, debug=False)

pos = client.read("$POS_ACT", debug=False)
p_dec = pos.decode('utf-8')
client.write("COM_E6POS",p_dec, debug=False)

###################START PROGRAMME FROM HERE##################


#client.write("COM_E6POS.X", '900.8' , debug=False)
##client.write("COM_E6POS.Y", '-348.16' , debug=False)
##client.write("COM_E6POS.Z", '1079.149' , debug=False)
