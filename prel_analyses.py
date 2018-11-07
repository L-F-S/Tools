    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 11:50:53 2018

@author: lorenzo

For every protein in the dataset, performs preliminarly 
statistical analyses of the various runs:

Histogram of RMDSs

2d Histogram of RMSD vs Native Contacts.

USAGE:
    
# for a complete thorough analysis of all proteins, run:
# EDIT: 0 0 now does 2dfe and fe and nc . (no more rmsd histogram)

python prel_analyses.py 0 0

# to specify a protein, but do every analyisis, do:

python prel_analyses.py prot_folder_name 0

# to specifiy mpore than one protein:

prot1-prot2-prot3

# to specify a protein AND an analysis, do:

python prel_analyses.py prot_folder_name analysisname

# to specify only an analysis:

python prel_analyses.py 0 analysisname

# possyble analyses names: 
# rmsd : only creates rmsd histogram.
# nc: only native contacts histogram.
# 2d: only 2d histogram of both native contacts and rmsd.
# fe: only free energy histogram
# 2dfe: only 2d nc fe histogram

# This presuppone che tutte le cartelle si chiamino proteina.pdb, e dentro abbiano 
# cartelle che si chiamano run_numeri, e che TUTTE queste cartelle siano run funzionanti
# presuppone quindi di aver mandato check-simulations.py
"""


from sys import argv
import os
#import matplotlib.pyplot as plt
#from matplotlib.colors import LogNorm
import numpy as np
#import pandas as pd

#def plot_2d_free_energy(rmsdncfe,protein, full_path_to_graphs):
#    """ takes as input a 3d numpy.array, and plots a heatmap of the first dim
#    vs the second, with the third as the heat value"""
#    
#    rmsd = rmsdncfe[:,0] #?
#    nc = rmsdncfe[:,1]
#    fe = rmsdncfe[:,2]
#    
#    # Create a grid of 100*100 points where to sit the heatmap on.
#    x = np.linspace(min(rmsd), max(rmsd), 1000)
#    y = np.linspace(min(nc), max(nc), 1000)
#    
#    # Create a dataframe that has for columns, the values of rmsd, and for 
#    # index, the values of nc. If a value of rmsd does not have that particular
#    # nc, it should be NaN. Fill the Df with the relative values of fe.
#    
#    DF
#    
#    # Plot this df onto the grid, giving colors as a heatmap
#    
#    im = plt.imshow(fe, cmap='rainbow', interpolation = 'mitchell')
##    plt.contourf(rmsd, nc, fe, 15, cmap='rainbow')
#    
#    plt.xlabel("RMSD")
#    plt.ylabel("Native Contacts")
#    plt.title(protein.rstrip("pdb").rstrip(".")+"\nFree Energy Landscape")
#    figpath = full_path_to_graphs + "/"+protein.rstrip("pdb").rstrip(".")
#    figname = protein.rstrip("pdb").rstrip(".")+"_free_energy_landscape.png"
#    full_path = os.path.join(figpath, figname)
##    plt.savefig(full_path) 
#    plt.show()
#    plt.close()
#    return
    

    
def plot_free_energy(rmsd,f_e,protein, full_path_to_graphs):
    """generates a plot of Free Energy as a function of RMDS, shifted to have 
    the minimum in 0"""
    
    print("Generating free energy plot")
    min_free_energy = min(f_e)
    shifted_f_e = [f - min_free_energy for f in f_e]
    
    plt.plot(rmsd, shifted_f_e)

    plt.xlabel("RMSD")  
    plt.ylabel("Free energy")
    plt.title(protein)
    plt.xticks()
    plt.yticks()

    figpath = full_path_to_graphs + "/"+protein
    figname = protein+"_free_energy.png"
    full_path = os.path.join(figpath, figname)
    plt.savefig(full_path) 
    plt.close()
    return

def twodhistogram(protein, list_of_values, bins, full_path_to_graphs):
    print("Generating 2d RMSD vs NC histogram for protein", protein)

    x = list_of_values[0][0]
    y = list_of_values[1][0]
    plt.figure(figsize=(10,10))
    counts, xbins, ybins, bars = plt.hist2d(x,y, bins=bins, normed=True, range=([[0, 6], [np.min(y), np.max(y)]]), cmap = "rainbow", norm=LogNorm()) #LogNorm scales colors somehow
    plt.xlabel( list_of_values[0][1], fontsize=16)  
    plt.ylabel(list_of_values[1][1], fontsize=16)
    plt.colorbar()
    plt.xticks()
    plt.title(protein)
    
    figpath= full_path_to_graphs +"/"+protein
    figname = protein+"_2d_nc_rmsd.png"
    full_path = os.path.join(figpath, figname)
    plt.savefig(full_path) 
    plt.close()
    return counts, xbins, ybins


def onedhistogram(protein, analysis, values, bins, full_path_to_graphs):
    print("Generating", analysis,"histogram")
        
    if analysis == 'RMSD':
        'returns a probability density'
        counts, bins, bars = plt.hist(values, bins = bins, range=(0,6), weights = np.ones(len(values))/len(values)) #weights serve per normalizzare i bins. non so xke funga così, ma così funge.
    if analysis == 'NC':
        counts, bins, bars = plt.hist(values, bins=bins,  weights = np.ones(len(values))/len(values)) 
    
    plt.xlabel(analysis)
    plt.title(protein)
    
    figpath=full_path_to_graphs+"/"+protein
    figname = protein+"_"+analysis+".png"
    full_path = os.path.join(figpath, figname)
#    if not os.path.isdir("/home/lorenzo.signorini/tirocinio/prove_varie/histograms/"+protein):
#        os.makedirs("/home/lorenzo.signorini/tirocinio/prove_varie/histograms/"+protein)
    plt.savefig(full_path) # la salva nel folde dela proteina    
    plt.close()
    
    # take away first bin because it's useless, and it fucks up the later plots.
    
    bins = bins[1:]
    return counts, bins

####################################
# Free energy calculation
####################################
    
def calculate_free_energy_matrix(rmsd_nc_tuple, protein):
    """takes as input two big lists of values, and returns a matrix of normalized
    counts of occurrences of those values"""
    
    """1. calculate relative frequencies of rmsd and nc values, and sort them (ascending).
    (this has already automatically been done by the plt.hist and plt.hist2d 
    function. Sorry computer.)"""
    rmsd_nc_list = -np.log(pd.Series(rmsd_nc_tuple).value_counts(normalize=True).sort_index())
    print(rmsd_nc_list)
    """this should be a series with a tuple as index, and -the negative logarithms count of 
    occurences of such tuple as valuE"""
    
    """ 2. Create a pd.DataFrame, with rmsd values as columns and nc values as
    index"""
    
    
    """ 3. Fill up the df with counts of occurrences of rmsd(i)+nc(j), and
    normalize them"""
    
    rmsd_nc_list.to_csv("free_energy.tsv", sep = "\t")
    return rmsd_nc_list

    
def rmsd_to_free_energy(probability):
    """converts the probability (histogram) of rmsd into free energy (derives 
    from theory you SHOULD know)"""
    return [-np.log(p) for p in probability]


####################################
# COORDINATES EXTRACTION

def extract_nc_rmsd(protein, full_path_to_prot, do_nc=True, do_rmsd=True):
    """Extract values of NC and RMSD together, for every timestep 
    and every simulation, and save them as a list of tuples. Every tuple
    is an occurrence of a given NC and a given RMSD. This means going through 
    thousands of rmsd and nc files AGAIN. Sorry, computer. This is so inefficient
    it hurts"""
    print("doppia estrazione maifren")
    rmsd=[]
    all_nc=[]
    nc_and_rmsd=[]
    for run in os.listdir():
        if run.startswith("run"):
            print(run)
            os.chdir(full_path_to_prot+"/"+run)
            for subfolder in os.listdir():
                if subfolder.startswith("msd") and do_rmsd == True:
                    os.chdir(full_path_to_prot+"/"+run)
                    f=open(subfolder)
                    msd_values=f.readlines()
                    f.close()
                    curr_rmsd = [float(msd.split(" ")[1].rstrip()) for msd in msd_values]
                    
                    rmsd+=curr_rmsd
#                   os.chdir("../")
                    
                if subfolder.startswith("native") and do_nc == True:
                     os.chdir("native_contacts")
                     firstline = True
                     for nc in os.listdir():
                        f=open(nc)
                        nc_values=f.readlines()
                        f.close()
                        curr_nc = [int(nc.split(" ")[1].rstrip()) for nc in nc_values]
                        if firstline == True:                  
                            total_nc = int(nc_values[0].split(" ")[2].rstrip())
                        all_nc+=curr_nc
                        
                        firstline = False
                
    normalized_nc = [nc/total_nc for nc in all_nc]
    
    print()
    
    """ supponendo ora che i valori di rmsd e nc siano stati appesi in ordine:"""
    if len(rmsd) == len(normalized_nc):
        """crea un file da dare in pasto ad R per fare il grafico della free energy"""
        os.chdir(full_path_to_prot)
        f = open("nc_rmsd.tsv", "a")
        f.write("RMSD\tNC\n")
        for i in range(len(rmsd)):
            nc_and_rmsd.append((rmsd[i],normalized_nc[i])) #TODO se la do a R nn serve manco salvarmela in meoria e sta line la posso cnacellare
            line = str(round(rmsd[i], 2)) + "\t" + str(round(normalized_nc[i],2)) + "\n"    
            f.write(line)
        f.close()
    else:
        raise ValueError("ATTENZIONE!! La lista di RMSD e NC della proteina", protein, "hanno lunghezza diversa!!\nLen(rmsd):" , len(rmsd),"\nLen(nc):", len(normalized_nc))
              

                 
    print("DONE")
    return nc_and_rmsd

    

def extract_nc(protein):
    """ extract the values of the number of native contacts at every step
    from the native_contacts files inside the run folders . Normalizes them,
    and saves them in an array"""
    
    print("extracting Native Contacts values")
    all_nc = []
    for run in os.listdir():
        if run.startswith("run"):
            os.chdir(run)
            os.chdir("native_contacts")
            firstline = True
            for nc in os.listdir():
                f=open(nc)
                nc_values=f.readlines()
                f.close()
                curr_nc = [int(nc.split(" ")[1].rstrip()) for nc in nc_values]
                if firstline == True:                  
                    total_nc = int(nc_values[0].split(" ")[2].rstrip())
                all_nc+=curr_nc
                os.chdir("../../")
                firstline = False
    normalized_nc = [nc/total_nc for nc in all_nc]
    print("DONE")
    return normalized_nc#, total_nc

def extract_rmsd(protein): #todo: cncellalo e fai do_nc=False nell'altor
    """ extract the values from the rmsd* files inside the run folders 
    and saves them in an array."""
    print("extracting RMSD values")
    
    rmsd=[]
    for run in os.listdir():
        if run.startswith("run"):
            os.chdir(run)
            for subfolder in os.listdir():
                if subfolder.startswith("msd"):
                    f=open(subfolder)
                    msd_values=f.readlines()
                    f.close()
                    curr_rmsd = [float(msd.split(" ")[1].rstrip()) for msd in msd_values]
                    
                    rmsd+=curr_rmsd
                    os.chdir("../")                  
                    
    print("DONE")
    return rmsd

######################################
# Analysis pipeline
#####################################

def preprocess(protein, analyses, full_path_to_prot):
    " Takes the protein name, and, according to 'analyses' variable, builds desired histograms"
    
    list_of_values = [] # this will store 1 or 2 tuples, each made by an array and its name.

#    if analyses == 0 or analyses == 3:
#        rmsd = extract_rmsd(protein)
#        nc = extract_nc(protein)  # era anche: nc, total_nc = extrac_nc(protein)
#        list_of_values.append((rmsd,"RMSD"))
#        list_of_values.append((nc,'NC'))
        

    if analyses == 1 or analyses == 4:
         rmsd = extract_rmsd(protein)
         list_of_values.append((rmsd,"RMSD"))

    if analyses == 2:
        nc = extract_nc(protein)  
        list_of_values.append((nc,'NC'))   

    print("\nGenerating Histograms")
    
    ################
    # 1 D graphs 
    
    full_path_to_graphs = full_path_to_prot + "histograms"
    
    for values, analysis in list_of_values:

        counts, bins = onedhistogram(protein,analysis,values,100, full_path_to_graphs)
        
        if analysis == 'RMSD' and (analyses == 0 or analyses == 4):
            free_energy = rmsd_to_free_energy(counts)
            print(free_energy)
            plot_free_energy(bins, free_energy, protein, full_path_to_graphs)

    ##################
    # 2D graphs 
    
    # Print a 2d histogram of nc vs rmsd. 
    if len(list_of_values) == 2:
        counts, xbins, ybins = twodhistogram(protein, list_of_values,100, full_path_to_graphs) 
    
    # Print 2d heatmap of free energy as a function of RMSD and NC
    # Not the most code-efficient way to do it, but I can't be bothered changing
    # the old code.
    if analyses == 0 or 4:
        rmsd_nc = extract_nc_rmsd(protein, full_path_to_prot)
        free_energy_matrix = calculate_free_energy_matrix(rmsd_nc, protein)
        
    print("DONE\n\n")
    
    return


################################    
#   main and Input manager
###############################
    

def wrapper():
    "returns a list of strings with protein names + an int enctrypting the analyses to be done (see 'preprocess' function)"
    
    print("\n--------------------------------------------------\n\nWellcome to your coarse grained molecular dynamics \nsimulations preprocessing unit\n\n--------------------------------------------------\n\n")
    # check which proteins
    if argv[1] == str(0):
        proteins = os.listdir()
        print("Processing all proteins\n")
    else:
        proteins = []
        if "-" in argv[1]:
            proteins = argv[1].split("-")
        else:
            proteins.append(argv[1])
        
    #check which analyses
    if argv[2] == '0':
        analyses = 0
        print("Generating RMSD, native contacts and RMSD vs native\ncontacts histograms.\nGenerating free energy plot\n")
    elif argv[2] == 'rmsd':
        analyses = 1
        print("Generating RMSD histograms\n") 
    elif argv[2] == 'nc':
        analyses = 2
        print("Generating native contacts histograms\n")
   
    elif argv[2] == '2d':
        analyses = 3
        print("Generating 2D native contacts vs RMSD histograms\n")
    elif argv[2] == 'fe':
        analyses = 4
        print("Generating Free energy plot\n")
    else:
        print("invalid analysis argument. Possible arguments: 0, rmsd, nc, 2d, fe")
    return proteins, analyses

def main():
    sim_folder = "/home/lorenzo/home/tirocinio/simulations"  # da cambiare 
    os.chdir(sim_folder)   
    proteins, analyses = wrapper()
    for protein in proteins:
         full_path_to_protein_folder = sim_folder+"/"+protein
         os.chdir(full_path_to_protein_folder)
         print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
         preprocess(protein, analyses, full_path_to_protein_folder)
    return

main()




#####
#from numpy import exp,arange
#from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show
#
## the function that I'm going to plot
#def z_func(x,y):
# return (1-(x**2+y**3))*exp(-(x**2+y**2)/2)
#
#x = arange(-3.0,3.0,0.1)
#y = arange(-3.0,3.0,0.1)
#X,Y = meshgrid(x, y) # grid of point
#Z = z_func(X, Y) # evaluation of the function on the grid
#
#im = imshow(Z,cmap=cm.RdBu) # drawing the function

