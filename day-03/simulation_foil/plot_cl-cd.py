#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:04:23 2022

@author: sandro
"""

import numpy as np
import matplotlib.pyplot as mpl

# MatPlotLib set fonts
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['DejaVu Serif']

# MatPlotLib set LaTeX use
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{siunitx}'


def plot_data(data, pdf_name):
    
    aa = data[0]
    cd = data[1]
    cl = data[2]
    
    fig, host = mpl.subplots()
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    
    p1, = host.plot(aa, cl, "g-", label=r'$C_\mathrm{L}$')
    p2, = par1.plot(aa, cd, "b-", label=r'$C_\mathrm{D}$')
    
    #host.set_xlim(0, 2)
    #host.set_ylim(0, 2)
    #par1.set_ylim(0, 4)
    #par2.set_ylim(1, 65)

    host.set_xlabel(r"Angle $\alpha$ [deg]")
    host.set_ylabel(r"$C_\mathrm{L}$")
    par1.set_ylabel(r"$C_\mathrm{D}$")
    
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    
    tkw = dict(size=4, width=1.5) # color axis ticks
    host.tick_params(axis='x', **tkw)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    

    host.grid(True)
    mpl.title('Force coefficients NACA-0012')
    
    fig.savefig(pdf_name)

# --------------------------------


angle = [0, 1, 2, 3, 5, 10, 15, 20]
cd = [0.00211979, 0.00215423, 0.00226832, 0.00245277, 0.00304126, 0.00693299, 0.0161569, 0.0308364]
cl = [-2.88251e-05, 0.00995757, 0.0198912, 0.029715, 0.0488138, 0.0848729, 0.0307398, 0.073176]

data = np.array([angle, cd, cl])

plot_data(data, 'cl-cd_plot.pdf')
