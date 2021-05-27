import ctypes as ct
from matplotlib import pyplot as plt
import pyllt as llt
import array as arr
import numpy as np
import pandas as pd
from sys import maxsize
from operator import itemgetter 
from numpy import set_printoptions
import threading
import time
import datetime
from py_openshowvar import openshowvar
client = openshowvar("172.31.1.147",7000)
print(client.can_connect)

################# PREREQUISITES #################

Vel = client.read("$OV_PRO", debug=False)   # Automatic speed, not manual speed from smart pad
Vel_dec = Vel.decode('utf-8')               # $ shows System variables

axis = client.read("$AXIS_ACT", debug=False)
axis_dec = axis.decode('utf-8')
client.write("COM_E6AXIS",axis_dec, debug=False)

pos = client.read("$POS_ACT", debug=False)
p_dec = pos.decode('utf-8')
client.write("COM_E6POS",p_dec, debug=False)

################# START PROGRAMME HERE ##################


# Parametrize transmission
scanner_type = ct.c_int(0)

##ReceivedProfileCount = 0
##NeededProfileCount = 1

available_resolutions = (ct.c_uint*4)()   # 4 number of elements but they are empty means it's showing 0
##print(len(available_resolutions))

available_interfaces = (ct.c_uint*6)()   # Interface means/defined for IP address, 6 number of elements but they are empty means it's showing 0
##print(len(available_interfaces))

lost_profiles = ct.c_int()
##print(lost_profiles.value)

# Null pointer if data not necessary
null_ptr_short = ct.POINTER(ct.c_ushort)()
##print(null_ptr_short)
null_ptr_int = ct.POINTER(ct.c_uint)()
##print(null_ptr_int)

# Create instance 
hLLT = llt.create_llt_device(llt.TInterfaceType.INTF_TYPE_ETHERNET)
##print(hLLT)

# Get available interfaces
ret = llt.get_device_interfaces_fast(hLLT, available_interfaces, len(available_interfaces))
if ret < 1:
    raise ValueError("Error getting interfaces : " + str(ret))

# Set IP address
ret = llt.set_device_interface(hLLT, available_interfaces[0], 0)
if ret < 1:
    raise ValueError("Error setting device interface: " + str(ret))

# Connect
ret = llt.connect(hLLT)
if ret < 1:
    raise ConnectionError("Error connect: " + str(ret))

# Get available resolutions
ret = llt.get_resolutions(hLLT, available_resolutions, len(available_resolutions))
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))

# Set max. resolution
resolution = available_resolutions[0]
##print(resolution)     # Output is 1280
ret = llt.set_resolution(hLLT, resolution)
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))


# Declare measuring data arrays

##Allocate correctly sized buffer array
##and fetch the latest received profile raw data from the internal receiving buffer.
## It's fetching 25 number of profiles/sec
## 25 is the minimum number of profiles that the scanner can fetch
## So, here it's fetching the latest received profile or 25th profile
##Here, I am not able to change the profile frequency. It's same 25.
profile_buffer = (ct.c_ubyte*(resolution*64))()      #ct.c_ubyte shows array, so print(profile_buffer.value) this will not work.
##print(len(profile_buffer))

##Allocate buffer for multiple profiles
#FullProfileBuffer = (ct.c_ubyte*(resolution*64*NeededProfileCount))()

x = (ct.c_double * resolution)()
##print(x[2])             ## It shows 0.0 means empty, because no profile has been transferred yet
z = (ct.c_double * resolution)()
intensities = (ct.c_ushort * resolution)()


# Scanner type
ret = llt.get_llt_type(hLLT, ct.byref(scanner_type))
if ret < 1:
    raise ValueError("Error scanner type: " + str(ret))

# Set profile config
ret = llt.set_profile_config(hLLT, llt.TProfileConfig.PROFILE)
if ret < 1:
    raise ValueError("Error setting profile config: " + str(ret))

# Set trigger
ret = llt.set_feature(hLLT, llt.FEATURE_FUNCTION_TRIGGER, llt.TRIG_INTERNAL)
if ret < 1:
    raise ValueError("Error setting trigger: " + str(ret))

# Start transfer
ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
if ret < 1:
    raise ValueError("Error starting transfer profiles: " + str(ret))

# Warm-up time
time.sleep(0.2)     #original value 0.2



#print('diff', diff)
#client.write("COM_E6POS.X",str(diff), debug=False)
##distance_x = 40
##velocity = (float(Vel_dec)/100)*18
##time.sleep(abs(distance_x/velocity))

current_x = client.read('COM_E6POS.X', debug=False)                 ## After scanning(Y) last segment, it won't move in X
curr_x_dec = float(current_x.decode('utf-8'))
print(curr_x_dec)
diff = curr_x_dec + 10



scanner_profile_data = []
robot_data  = []
loop_time=[]

##t = 0
###start = time.time()
##def scanner_robot_DA():
##    global t
##    while t < 1:
##        
##        ret = llt.get_actual_profile(hLLT, profile_buffer, len(profile_buffer), llt.TProfileConfig.PROFILE,
##                                ct.byref(lost_profiles))
##        ret = llt.convert_profile_2_values(hLLT, profile_buffer, resolution, llt.TProfileConfig.PROFILE, scanner_type, 0, 1,
##                                        null_ptr_short, intensities, null_ptr_short, x, z, null_ptr_int, null_ptr_int)
##        #curr_x_dec = client.read('COM_E6POS.X', debug=False)
##        scanner_profile_data.append(np.array(x))
##        scanner_profile_data.append(np.array(z))
##        lst1 = [client.read('COM_E6POS.X', debug=False),client.read('COM_E6POS.Y', debug=False),client.read('COM_E6POS.Z', debug=False),
##        client.read('COM_E6POS.A', debug=False),client.read('COM_E6POS.B', debug=False),client.read('COM_E6POS.C', debug=False)]
##        #lst2 = [lst1[i].decode('utf-8') for i in range(6)]
##        robot_data.append(lst1)
##        t = t + 0.01

#elapsed_time_fl = (time.time() - start)



#start = time.time()
def scanner_robot_DA():
    global curr_x_dec
    while curr_x_dec < diff:
        ######### New lines for time
        #loop_start=datetime.datetime.now()
        #loop_start_stamp=loop_start.timestamp()


        t_scan=datetime.datetime.now()
        t_scan_stamp=t_scan.timestamp()
        ###### timestamp code end 
        #lst2 = []
        
        
        ret = llt.get_actual_profile(hLLT, profile_buffer, len(profile_buffer), llt.TProfileConfig.PROFILE,
                                ct.byref(lost_profiles))
        ret = llt.convert_profile_2_values(hLLT, profile_buffer, resolution, llt.TProfileConfig.PROFILE, scanner_type, 0, 1,
                                        null_ptr_short, intensities, null_ptr_short, x, z, null_ptr_int, null_ptr_int)
        # about 1 ms max

        
        #current_x = client.read('$POS_ACT.X', debug=False)
        #curr_x_dec = float(current_x.decode('utf-8'))
        
        lst1 = [client.read('$POS_ACT.X', debug=False), client.read('$POS_ACT.Y', debug=False),client.read('$POS_ACT.Z', debug=False)]
        #client.read('$POS_ACT.A', debug=False),client.read('$POS_ACT.B', debug=False),client.read('$POS_ACT.C', debug=False)]
        #lst2 = [lst1[i].decode('utf-8') for i in range(6)]
        
             

        #scanner data update
        
        scanner_profile_data.append([t_scan,t_scan_stamp])
        scanner_profile_data.append(np.array(x))
        scanner_profile_data.append(np.array(z))

           

        #Pose data update
        
        
        robot_data.append(np.array(lst1))
        
        
        
        loop_start=datetime.datetime.now()
        loop_start_stamp=loop_start.timestamp()
        
        current_x = client.read('$POS_ACT.X', debug=False)
        curr_x_dec = float(current_x.decode('utf-8'))
        #print("current X: ",current_x, "curr_X_dec :  ", curr_x_dec, "LST1(1): ",lst1[0])
        
        loop_stop=datetime.datetime.now()
        loop_stop_stamp=loop_stop.timestamp()
        loop_time.append([loop_start_stamp,loop_stop_stamp])
        
        #del lst2[:]
        #loop_stop=datetime.datetime.now()
        #loop_stop_stamp=loop_stop.timestamp()
        #loop_time.append([loop_start_stamp,loop_stop_stamp])





##scanner_robot_DA()
##print(scanner_profile_data)
##print(robot_data)



def actuation():
    current_x = client.read('COM_E6POS.X', debug=False)                 ## After scanning(Y) last segment, it won't move in X
    curr_x_dec_1 = float(current_x.decode('utf-8'))
    diff = curr_x_dec_1 + 10
    client.write("COM_E6POS.X",str(diff), debug=False)
    distance_x = 10
    velocity = (float(Vel_dec)/100)*18
    time.sleep(abs(distance_x/velocity))
    

#start = time.time()

t1 = threading.Thread(target = actuation)
t2 = threading.Thread(target = scanner_robot_DA)

t1.start()
t2.start()

t1.join()
t2.join()

#elapsed_time = (time.time() - start)
#print('Time taken: ', start - elapsed_time)

#robot_data = [x.decode('utf-8') for x in robot_data]

#print(scanner_profile_data)
#print(robot_data)

df=pd.DataFrame(scanner_profile_data)
df.to_csv('Multi_threading_scanner_profile_data.csv', index=False, header=False)
#np.savetxt('Multi_threading_scanner_profile_data.csv', scanner_profile_data, delimiter=",")   

df=pd.DataFrame(robot_data)
df.to_csv('Multi_threading_robot_data.csv', index=False, header=False)
#np.savetxt('Multi_threading_robot_data.csv', robot_data, delimiter=",")    

df=pd.DataFrame(loop_time)
df.to_csv('Multi_threading_loop_time_data.csv', index=False, header=False)


    
##print(np.array(x))    # It prints the Full array 
##print(np.array(z))

