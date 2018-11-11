# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:11:45 2018

@author: Judy Zhang
"""
import matplotlib.pyplot as plt

filename = "record_phi.txt"
mode = "r"
record  = open(filename, mode) 
record_lines = record.read().splitlines()
seq_list = []
time_list = []
d_list = []
phi_list = []
for i in range(int(len(record_lines)/13)):
    lines = record_lines[i*13:(i+1)*13]
    #record sequence
    seq = int(lines[1].split(' ')[-1])
    seq_list.append(seq)
    #timestamp
    stamp = lines[3:5]
    sec = stamp[0].split(' ')[-1]
    nsec = stamp[1].split(' ')[-1]
    time = int(sec)+int(nsec)/(10**9)
    time_list.append(time)
    #d value
    d = float(lines[6].split(' ')[-1])
    d_list.append(d)
    #phi value
    phi = float(lines[8].split(' ')[-1])
    phi_list.append(phi)
    print(str(seq)+'\n'+str(time)+'\n'+str(d)+'\n'+str(phi))
    
plt.plot(d_list)    
plt.ylabel("d")
plt.xlabel("sequence")
plt.show()


plt.plot(phi_list)
plt.ylabel("phi")
plt.xlabel("sequence")
plt.show()

plt.plot(time_list)
plt.ylabel("time")
plt.xlabel("sequence")
plt.show()





