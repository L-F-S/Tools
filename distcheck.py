#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:24:19 2018

@author: lorenzo

coordinates start at 14th line
"""


from sys import argv
import math

#########################################
#    check distance of ca from .kaw file
#########################################


def check_distance(previousCA, currentCA, line, linecount):
    if not previousCA == -1:
        dist = math.sqrt((previousCA[0]-currentCA[0])**2 + (previousCA[1] - currentCA[1])**2 + (previousCA[2] - currentCA[2])**2)
        if round(dist, 1) == 1.0 or round(dist, 1)==1.1:
            return 
        else:
            print("distance: ", dist, "  rounded: ", round(dist))
            print("line n  ", linecount)
            print(line)
            raise Exception("C_alpha not at right distance. Terminating.")
    return

def extract_coords(line):
    line = line.split()
    x = float(line[0])
    y = float(line[1])
    z = float(line[2])
    return [x,y,z]


def check_distance_wrapper(kaw):
   

    beads_count = 0
    linecount = 1
    previous_CA_coords = -1
    for line in kaw.readlines():
        if linecount > 13:
            coordinates = extract_coords(line)
            check_distance(previous_CA_coords, coordinates, line, beads_count)
            previous_CA_coords = coordinates
            beads_count += 1
        linecount +=1
    print("Beads found: ", beads_count)            
    return 


def main():
    
    filename = argv[1]
    print("+++++++++++++++++++++++++++++++++++++++\nLoading {}\n".format(filename))
    
    """create identifier string from filename, by removing .pdb suffix and path.
    this will be used by the biopython parser to assign an id to the structure
    WARNING: this works specifically for my folder structure."""
    identifier = filename.rstrip(".pdb").lstrip("original/")
    
    """Load PDB file:"""
    kaw = open(filename)
    
    check_distance_wrapper(kaw)
    
    kaw.close()
    
    return 

main()
    
