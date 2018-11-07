#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 15:05:10 2018

@author: lorenzo

Performs some checks on the Jobs (Not on the simulations themselves).
"""

import os
import pandas as pd
from datetime import datetime
import numpy as np

os.chdir("/home/lorenzo.signorini/tirocinio/jobs")

###############################
# check for errors in execution
##############################
NO_ERRORS = True
for file in os.listdir():
    if file.startswith("err"):
        f=open(file)
        if len(f.readline())==0:
            continue
        else:
            NO_ERRORS = False
            print("\n".join([l for l in f.readlines()]))
        f.close()
        
if NO_ERRORS == True:
    print("No error messages in any submission.")

#################################
#    calculate avg execution time of a single job
#################################

def diff_times_in_seconds(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    if t2.hour < 4 and t1.hour > 20:
        return(24*60*60-t1_secs+t2_secs)
    return( np.abs(t2_secs - t1_secs))




times_list = []

for file in os.listdir():
    if file.startswith("out"):
        
        times = pd.read_table(file)
        start = datetime.strptime(str(times.head(1)).split()[5], '%H:%M:%S').time()
        end = datetime.strptime(str(times.tail(1)).split()[14], '%H:%M:%S').time()      
        exec_time_secs = diff_times_in_seconds(start, end)
        times_list.append(exec_time_secs)

print("average execution time of last", len(times_list), "jobs:", (sum(times_list)/len(times_list))/3600, "hours")
        
        
