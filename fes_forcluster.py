#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 16:13:10 2018

@author: lorenzo

USAGE:
    python3 fes_forcluster.py xvalue
    
    possible values for xvalue: "g","nc"
"""

#####################################################################
#            IMPORTS
#####################################################################

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage.filters import gaussian_filter


###############
# if matplotlib gets stuck in some wierd way, just do this.

from importlib import reload  
#eload(plt)
from matplotlib.colors import LogNorm


#####################################################################
#        PLOT FUNCTION
####################################################################
    
def twoD_free_energy_plot(x,y, sname, xvalue,kind):
    """
     inputs: x,y   : numpy.arrays of the same length
            name   : a string to give a title to the plot
            xvalue : little string to print the name of x
            kind   : another string for the filename. 
     output: a smoothed 2d-free-energy-plot
    """

    
    h, xe, ye, img = plt.hist2d( x, y, bins = 80,  cmap =  plt.cm.jet, norm=LogNorm())
    print("done hstiogram")
    plt.xlim(0,4.5)
    plt.colorbar()

    fh = gaussian_filter(h, 1.14) #1.14
    print(h.shape, h.min(), h.max())
    print(fh.shape, fh.min(), fh.max())
    
    fe = -np.log(fh/fh.max())
    
    #plt.figure(figsize=(100,300))
    
    fig, ax = plt.subplots(figsize=(20,20))
    
    masked_data = np.ma.masked_where(fe > 9, fe)
    ax = plt.gca()
    #cmap:
    #from matplotlib.colors import ListedColormap
    #from matplotlib.colors import Normalize
    
    cmap = plt.cm.jet_r
    #my_cmap = cmap(np.arange(cmap.N)) #get colors
    #my_cmap = ListedColormap(my_cmap)
    #
    #alphas = np.ones(weights.shape)
    #alphas[:, 30:] = np.linspace(1, 0, 70)
    #colors = Normalize(0, 9, clip=True)(weights)
    #
    
    
#    im = ax.imshow(masked_data.T, extent=(0,x.max(),0,1), origin='lower', aspect = 'auto', cmap = cmap, interpolation = 'kaiser')
    levels = np.arange(0,10,0.01)
    #fig, ax = plt.subplots()
    c=ax.contourf(xe[1:], ye[1:],fe.T, origin='lower', cmap = plt.cm.jet_r, levels = levels)
#    d=ax.contour(xe[1:]-0.3, ye[1:]-0.005,fe.T, origin='lower', levels = levels, linestyles='solid', cmap = 'jet_r', linewidths=30, alpha=1)
    plt.ylim(top=5.5)
    plt.xlabel(xvalue.upper(), fontsize = 30)
    plt.ylabel("$RMSD$", fontsize = 30)
    plt.yticks( fontsize = 30 )
    plt.xticks( fontsize = 30 )
    
    #cbar = fig.colorbar(c)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    cbar=plt.colorbar(c, cax=cax)
    cbar.set_label(label='Free Energy [$\epsilon}$]', fontsize=30)
    cbar.ax.tick_params(labelsize=30)
    #cbar.set_clim(0, 9)
    #cbar.set_ticks(0,9)
    
    plt.tight_layout()
    plt.savefig("/ptmp/slor/da/FES"+sname+kind+"_"+xvalue+".png", format = 'png')

    return

##############################################################################
#      Wrapper (navigate through folders, iterate over more structures)
#      launch prel_analyses_only_nc_rmsd.py first
##############################################################################
def user_input():
    if len(sys.argv) <= 1:
        print("USAGE: python3 fes_forcluster.py protname(or [all])  xvalue [g],[nc] (G not implemented yet..), kind [normal] [folded] [equi]")
        exit(1)
    else:
        return sys.argv[1], sys.argv[2], sys.argv[3]
    
def main():
    protnames, xvalue, kind = user_input()
    simulations_folder = "/ptmp/slor/fold" if not kind == 'equi' else "/ptmp/slor/equi"
    os.chdir(simulations_folder)
    protein_folders = [protnames]  if not protnames == "all" else os.listdir()
    for folder in protein_folders:#os.listdir():#"1bzp", "1csp", "1div.n", "1fkb", "1hrc", "1hz6_a", "1imq", "1lmb3", "1pgb", "1poh", "1psf", "1shf_a", "1ten", "1tit", "1ubq", "1urn", "1wit", '2abd', '2ci2', '2pdd', '2vik', '256b']:
        if folder.startswith("1") or folder.startswith("2"):    
            print(folder)  
            coords_file = folder+"_nc_rmsd.tsv" if not kind == 'folded' else folder+"FOLDED_nc_rmsd.tsv"
            g_coords_file = "G_"+folder+".dat"  if not kind == 'folded' else "G_"+folder+"FOLDED.dat"
            
            df=np.loadtxt(simulations_folder+"/"+folder+"/"+coords_file, delimiter='\t') 
            rmsd=df[:,0]           
            x = df[:,1] if xvalue == "nc" else np.loadtxt(simulations_folder+"/"+folder+"/"+g_coords_file, delimiter='\t')[:,1] if xvalue == 'g' else 0
    
            
            twoD_free_energy_plot(x,rmsd,folder, xvalue, kind)

    return

main()