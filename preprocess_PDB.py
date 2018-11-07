########################################àà
########MAI USATO QUESTO FILE ma è bello quindi ormai lo tengo

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:24:19 2018

@author: lorenzo

This script takes as input a PDB file of a protein, and outputs an 'input_file'
for the Polymer_MD_mpi program.

Before creating input_file, checks that every C_\alpha is exactly 3.8 AA away
from its neighbour.

input_file should have coordinates of only C_\alpha.
Coordinates  should be in natural units (i.e. regular coordinates
divided by 3.8, so as to keep covalent C-C bond distance = 1)
every C_\alpha should also have velocity coordinates explicitly set to 0.00

---------------------------------------------------------------------------
This script assumes that PDB are the exact chain wanted, 
which is most likely false.

---------------------------------------------------------------------------
USAGE:
in a terminal: type

python preprocess_PDB.py original/proteinfilename.pdb
"""

from Bio.PDB import *
from sys import argv
import math

#########################################
#    Obtain chain of C_\alpha from PDB
#########################################


def naturalize(coordinates):      
        return [round(i/3.8, 3) for i in coordinates]


def check_distance(previousCA, currentCA, line):
    if not previousCA == -1:
         dist = math.sqrt((previousCA[0]-currentCA[0])**2 + (previousCA[1] -\
                         currentCA[1])**2 + (previousCA[2] - currentCA[2])**2)
         if round(dist, 1) == 3.8 or round(dist, 1)==3.9:
            return 
         else:
            print("distance: ", dist, "  rounded: ", round(dist))
            print(line)
            raise Exception("C_alpha not at right distance. Terminating.")
    return

def extract_coords(line):
    line = line.split()
    x = float(line[6])
    y = float(line[7])
    z = float(line[8])
    return [x,y,z]


def full_prot_to_calpha(PDB):
   
    """initialize a string to store the coordinates in"""
    c_alpha_with_velocities = ""
    
    """temp variable to store the previous CA in order to compute distances"""
    previous_CA_coords = -1
    beads_count = 0
    for line in PDB.readlines():
        
        """read PDB line by line. Only keep lines starting with 'ATOM'"""
        if line.startswith("ATOM"):
            
            """Only keep lines That are CA"""
            if "CA" in line:
            
                """extact coordinates and convert them to natural units"""
                coordinates = extract_coords(line)
                
                """check that no C_\alpha is missing, and that no C_\alpha 
                    has ambiguous coordinates"""
                check_distance(previous_CA_coords, coordinates, line)
                
                """convert to natural units"""
                coordinates = naturalize(coordinates)
                
                """updeate previous_CA and c_alpha_with_velocities and beads_count """
                previous_CA_coords = coordinates
                c_alpha_with_velocities += "\t".join([str(i) for i in coordinates]) + "\t0.000\t0.000\t0.000\n"
                beads_count +=1
    print("Beads found: ", beads_count)            
    return c_alpha_with_velocities


def Calpha_from_PDB():
    
    filename = argv[1]
    print("+++++++++++++++++++++++++++++++++++++++\nLoading {}\n".format(filename))
    
    """create identifier string from filename, by removing .pdb suffix and path.
    this will be used by the biopython parser to assign an id to the structure
    WARNING: this works specifically for my folder structure."""
    identifier = filename.rstrip(".pdb").lstrip("original/")
    
    """Load PDB file:"""
    PDB = open(filename)
    
    c_alpha_with_velocities = full_prot_to_calpha(PDB)
    
    PDB.close()
    
    return c_alpha_with_velocities, identifier


############################
#    create input file
############################


def getNbeads(calpha_chain):
    return 100


def generate_header(Nbeads):
        """input_file header template:
            
            #read_chain     0 
            #Nbeads         set to n_c-alpha
            #timestep       0.0005
            #Nsteps         7000000
            #FENE_bond      1.5
            #FENE_kappa     30.0
            #dump_traj      5000
            #RV             4.0
            #epsilon        1.0
            #tau_frict      1.0
            #temp           0.1
            #niters         1
            
            #Coordinates"""

            
        return "#read_chain     0\n#Nbeads         {}\n#timestep       0.0005\n\
#Nsteps         7000000\n#FENE_bond      1.5\n#FENE_kappa     30.0\n#dump_traj\
      5000\n#RV             4.0\n#epsilon        1.0\n#tau_frict      1.0\n#temp\
           0.1\n#niters         1\n\n#Coordinates".format(Nbeads)


def create_input_file(calpha_chain, protein_id):
    """input_file should have .kaw extension"""
    print("Generating input file..")
    Nbeads = getNbeads(calpha_chain)
    filename = "input_files/"+protein_id+".kaw"
    f = open(filename, 'w')
    header = generate_header(Nbeads)
    f.write(header+"\n"+calpha_chain)
    f.close()
    return


##########################
#   main
#########################

if __name__=="__main__":
    
    """ Obtain chain of C_\alpha from PDB file """
    calpha_chain, protein_id = Calpha_from_PDB()
    
    """generate the input_file for Polymer_MD"""
    create_input_file(calpha_chain, protein_id)
    
    print("Done.")

    
