import ctypes as ct
import time
from matplotlib import pyplot as plt
import pyllt as llt
import array as arr
import numpy as np
import pandas as pd

# Parametrize transmission
Number_of_Profiles = 1

master_list=[]
for i in range (Number_of_Profiles):
    scanner_type = ct.c_int(0)
    ##print(scanner_type)

    # Init profile buffer and timestamp info
    timestamp = (ct.c_ubyte*16)()      # 16 number of elements but they are empty means it's showing 0
    ##print(len(timestamp))

    available_resolutions = (ct.c_uint*4)()   # 4 number of elements but they are empty means it's showing 0
    ##print(len(available_resolutions))

    available_interfaces = (ct.c_uint*6)()    # Interface means/defined for IP address, 6 number of elements but they are empty means it's showing 0
    ##print(len(available_interfaces))

    lost_profiles = ct.c_int()
    ##print(lost_profiles)

    shutter_opened = ct.c_double(0.0)
    ##print(shutter_opened)

    shutter_closed = ct.c_double(0.0)
    ##print(shutter_closed)

    profile_count = ct.c_uint(0)
    ##print(profile_count)

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
    profile_buffer = (ct.c_ubyte*(resolution*64))()
    ##print(len(profile_buffer))

    x = (ct.c_double * resolution)()
    ##print(x[2])             ## It shows 0.0 means empty, because no profile has been transferred yet
    z = (ct.c_double * resolution)()
    intensities = (ct.c_ushort * resolution)()

    ##list1=[]
    ##print(len(x))     # Output is 1280
    ##print(len(z))     # Output is 1280

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

    # Set exposure time
    ret = llt.set_feature(hLLT, llt.FEATURE_FUNCTION_EXPOSURE_TIME, 100)
    if ret < 1:
        raise ValueError("Error setting exposure time: " + str(ret))

    # Set idle time
    ret = llt.set_feature(hLLT, llt.FEATURE_FUNCTION_IDLE_TIME, 3900)
    if ret < 1:
        raise ValueError("Error idle time: " + str(ret))

    # Start transfer
    ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
    if ret < 1:
        raise ValueError("Error starting transfer profiles: " + str(ret))

    # Warm-up time
    time.sleep(0.2)     #original value 0.2

    ret = llt.get_actual_profile(hLLT, profile_buffer, len(profile_buffer), llt.TProfileConfig.PROFILE,
                                 ct.byref(lost_profiles))
    if ret != len(profile_buffer):
        raise ValueError("Error get profile buffer data: " + str(ret))

    ret = llt.convert_profile_2_values(hLLT, profile_buffer, resolution, llt.TProfileConfig.PROFILE, scanner_type, 0, 1,
                                    null_ptr_short, intensities, null_ptr_short, x, z, null_ptr_int, null_ptr_int)
    #del x[:]
    #del z[:]
    list1=[]
    list2=[]
    #del list1[:]
    #del list2[:]
##    for i in range (1280):
##        print(x[i])
    if ret & llt.CONVERT_X is 0 or ret & llt.CONVERT_Z is 0 or ret & llt.CONVERT_MAXIMUM is 0:
        raise ValueError("Error converting data: " + str(ret))
##    xx=x.tolist()
##    zz=z.tolist()
    listxx=[]
    for j in range (1280):
        listxx.append(x[j])
    master_list.append(listxx)
    listzz=[]
    for k in range (1280):
        listzz.append(z[k])
    master_list.append(listzz)
    
    print("Profile number " + str(i+1) + " is received")        ## At this line, we have already received the profiles

    # Output of profile count
    for i in range(16):
        timestamp[i] = profile_buffer[resolution * 64 - 16 + i]
        

    llt.timestamp_2_time_and_count(timestamp, ct.byref(shutter_opened), ct.byref(shutter_closed), ct.byref(profile_count))
    ##print(profile_count.value)

    # Stop transmission
    ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 0)
    if ret < 1:
        raise ValueError("Error stopping transfer profiles: " + str(ret))

    # Disconnect
    ret = llt.disconnect(hLLT)
    if ret < 1:
        raise ConnectionAbortedError("Error while disconnect: " + str(ret))

    # Delete
    ret = llt.del_device(hLLT)
    if ret < 1:
        raise ConnectionAbortedError("Error while delete: " + str(ret))

#print(master_list)
df=pd.DataFrame(master_list)
#print(df.to_string(index=False))
df.to_csv('final_csv_python1.csv', index=False)

    
##    for i in range (1280):
##        list1.append(x[i])
##        list1 = list(np.around(np.array(list1),3))
##        list2.append(z[i])
##        list2 = list(np.around(np.array(list2),3))
        
##df11 = pd.DataFrame(list(zip(list1, list2)))
##df11.to_csv('try97.csv')
        


'''
# save numpy array as csv file
from numpy import asarray
from numpy import savetxt
# define data
data = asarray(x)
# save to csv file
savetxt('data1.csv', data)


list1=[]
for i in range (1280):
    list1.append(x[i])
list1 = list(np.around(np.array(list1),3))
print(list1)

list2=[]
for i in range (1280):
    list2.append(z[i])
list2 = list(np.around(np.array(list2),3))
print(list2)
'''

##if ret & llt.CONVERT_X is 0 or ret & llt.CONVERT_Z is 0 or ret & llt.CONVERT_MAXIMUM is 0:
##    raise ValueError("Error converting data: " + str(ret))
##
### Output of profile count
##for i in range(16):
##    timestamp[i] = profile_buffer[resolution * 64 - 16 + i]
##    
##
##llt.timestamp_2_time_and_count(timestamp, ct.byref(shutter_opened), ct.byref(shutter_closed), ct.byref(profile_count))
####print(profile_count.value)
##
### Stop transmission
##ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 0)
##if ret < 1:
##    raise ValueError("Error stopping transfer profiles: " + str(ret))
##
### Disconnect
##ret = llt.disconnect(hLLT)
##if ret < 1:
##    raise ConnectionAbortedError("Error while disconnect: " + str(ret))
##
### Delete
##ret = llt.del_device(hLLT)
##if ret < 1:
##    raise ConnectionAbortedError("Error while delete: " + str(ret))

plt.figure(facecolor='white')
plt.subplot(211)
plt.grid()
plt.xlabel('x')
plt.ylabel('z')
plt.xlim(-60, 60)
plt.ylim(25, 150)
plt.plot(x, z, 'g.', label="z", lw=2)

##for i in range(10):
##    for i in range (1280):
##        print(x[i])
##    for i in range (1280):
##        print(z[i])

##plt.subplot(212)
##plt.grid()
##plt.xlabel('x')
##plt.ylabel('intensities')
##plt.xlim(-60, 60)
##plt.ylim(0, 1200)
##plt.plot(x, intensities, 'r.', label="intensities", lw=1)

##IMP:IMP:IMP:IMP:IMP:IMP:IMP:IMP:IMP:IMP
##When reading to and from your CSV file include the argument index=False so for example:
##df.to_csv(filename, index=False)
##and to read from the csv
##df.read_csv(filename, index=False)

##df.style.hide_index()




