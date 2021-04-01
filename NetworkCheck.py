'''
Created on Mar 30, 2021

@author: daily
'''

import os
import time
import datetime

ip_list = ["8.8.8.8", "8.8.4.4"]
wait_time = 60

def ip_check():
    system_time = datetime.datetime.now()
    ymd = system_time.strftime("%d/%m/%Y")
    hms = system_time.strftime("%H:%M:%S")
    global tasklist
    tasklist = ""
    for ip in range(len(ip_list)):
        response = os.popen(f"ping " + ip_list[ip]).read()
        if "Received = 4" in response and ip == 0:
            tasklist += ymd + "\t" + hms + "\t" + ip_list[ip] + "\tUP\t1.0"
        elif "Received = 4" not in response and ip == 0:
            tasklist += ymd + "\t" + hms + "\t" + ip_list[ip] + "\tDOWN\t0.0"
        elif "Received = 4" in response and ip > 0:
            tasklist += "\n" + ymd + "\t" + hms + "\t" + ip_list[ip] + "\tUP\t1.0"
        elif "Received = 4" not in response and ip > 0:
            tasklist += "\n" + ymd + "\t" + hms + "\t" + ip_list[ip] + "\tDOWN\t0.0"
    return tasklist

while 1:
    outfile = open("network_log.txt", "a")
    output = ip_check()
    print("Checking IPs...")
    print(output, file=outfile)
    print(output)
    outfile.close()
    time.sleep(wait_time)