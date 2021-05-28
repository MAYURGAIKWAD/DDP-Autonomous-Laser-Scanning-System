import ctypes as ct
import time
from matplotlib import pyplot as plt
import pyllt as llt
import numpy as np
import datetime
# Parametrize transmission
scanner_type = ct.c_int(0)

# Init profile buffer and timestamp info
timestamp = (ct.c_ubyte*16)()
available_resolutions = (ct.c_uint*4)()
available_interfaces = (ct.c_uint*6)()
lost_profiles = ct.c_int()
shutter_opened = ct.c_double(0.0)
shutter_closed = ct.c_double(0.0)
profile_count = ct.c_uint(0)

# Null pointer if data not necessary
null_ptr_short = ct.POINTER(ct.c_ushort)()
null_ptr_int = ct.POINTER(ct.c_uint)()

# Create instance 
hLLT = llt.create_llt_device(llt.TInterfaceType.INTF_TYPE_ETHERNET)

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
ret = llt.set_resolution(hLLT, resolution)
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))

# Declare measuring data arrays
profile_buffer = (ct.c_ubyte*(resolution*64))()
x = (ct.c_double * resolution)()
z = (ct.c_double * resolution)()

######### New lines for time stamp
tc=datetime.datetime.now()
tstamp=tc.timestamp()
###### timestamp code end   

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
time.sleep(0.2)

ret = llt.get_actual_profile(hLLT, profile_buffer, len(profile_buffer), llt.TProfileConfig.PROFILE,
                             ct.byref(lost_profiles))
if ret != len(profile_buffer):
    raise ValueError("Error get profile buffer data: " + str(ret))

ret = llt.convert_profile_2_values(hLLT, profile_buffer, resolution, llt.TProfileConfig.PROFILE, scanner_type, 0, 1,
                                null_ptr_short, intensities, null_ptr_short, x, z, null_ptr_int, null_ptr_int)
if ret & llt.CONVERT_X is 0 or ret & llt.CONVERT_Z is 0 or ret & llt.CONVERT_MAXIMUM is 0:
    raise ValueError("Error converting data: " + str(ret))

# Output of profile count
for i in range(16):         ########## what is the significance of 16
    timestamp[i] = profile_buffer[resolution * 64 - 16 + i]

llt.timestamp_2_time_and_count(timestamp, ct.byref(shutter_opened), ct.byref(shutter_closed), ct.byref(profile_count))
##print(profile_count.value)

##for i in range(1280):
##    print(z[i])
    
##p1=max(np.array(z))
##p2=min(np.array(z))
##print("max z= " + str(p1))
##print("min z= " + str(p2))

##print(np.array(x))
##print(np.array(z))
# Stop transmission

profile=[]
profile.append([tc,tstamp])
profile.append(np.array(x))
profile.append(np.array(z))
np.savetxt('grind polished surface.csv', profile, fmt='%.3f', delimiter=",")    ##This is perfect, fmt='%.3f' gives 3 digit after decimal point.

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

plt.figure(facecolor='white')
plt.subplot(211)
plt.grid()
plt.xlabel('x')
plt.ylabel('z')
plt.xlim(-60, 60)
plt.ylim(25, 350)
plt.plot(x, z, 'g.', label="z", lw=2)
plt.subplot(212)
plt.grid()
plt.xlabel('x')
plt.ylabel('intensities')
plt.xlim(-60, 60)
plt.ylim(0, 1200)
plt.plot(x, intensities, 'r.', label="intensities", lw=1)
##plt.show()
