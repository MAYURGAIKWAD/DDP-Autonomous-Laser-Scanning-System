import datetime
#format long
import time
avg_delay=0
for i in range(1, 100):
        t_scan = datetime.datetime.now()
        t_scan_stamp = t_scan.timestamp()
        time.sleep(.1)
        t_pose = datetime.datetime.now()
        t_pose_stamp = t_pose.timestamp()
        avg_delay+=(t_pose_stamp - t_scan_stamp)
        print(i," : ", (t_pose_stamp - t_scan_stamp))
avg_delay=avg_delay/99
print("average delay = ", avg_delay)
print("t_scan : ", t_scan)
print ("t_pose : ", t_pose)
