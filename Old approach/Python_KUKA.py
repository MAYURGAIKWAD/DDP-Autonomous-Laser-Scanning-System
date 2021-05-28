import numpy as np
import pandas as pd
from py_openshowvar import openshowvar

import datetime #used for timestamp


client = openshowvar("172.31.1.147",7000)
print (client.can_connect)


################# PREREQUISITES #################

Vel=client.read('$OV_PRO')        # Gives value of automatic speed, not manual speed
Vel_dec=Vel.decode('utf-8')
print(Vel_dec)

Vel=client.read('$VEL_ACT')       # Showing 0
Vel_dec=Vel.decode('utf-8')
print(Vel_dec)

Vel=client.read('$VEL_CP_T1')       
Vel_dec=Vel.decode('utf-8')
print(Vel_dec)

axis = client.read("$AXIS_ACT")
axis_dec=axis.decode('utf-8')
#print(axis_dec)
a1=client.write("COM_E6AXIS",axis_dec)
b1=a1.decode('utf-8')
#print(b1)


pos=client.read("$POS_ACT")
p_dec=pos.decode('utf-8')
#print(p_dec)
p1=client.write("COM_E6POS",p_dec)
q1=p1.decode('utf-8')
#print(q1)


frame=client.read("$POS_ACT")
fr=frame.decode('utf-8')
#print(fr)
f1=client.write("COM_FRAME",fr)
g1=f1.decode('utf-8')
#print(g1)


pos1=client.read("$POS_ACT")
p1_dec=pos1.decode('utf-8')
#print(p1_dec)
s1=client.write("COM_POS",p1_dec)
t1=s1.decode('utf-8')
#print(t1)



###################START PROGRAMME FROM HERE##################


client.write("COM_E6POS.X", '824.8' , debug=False)
client.write("COM_E6POS.Y", '-348.16' , debug=False)
client.write("COM_E6POS.Z", '1079.149' , debug=False)

## getting timestamps from system

ct = datetime.datetime.now() 
print("current time:-", ct) 
  
# ts store timestamp of current time 
ts = ct.timestamp() 
print("timestamp:-", ts) 