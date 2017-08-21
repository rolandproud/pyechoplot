# -*- coding: utf-8 -*-
"""
.. :module:: plotting
    :synopsis: plotting functions

| Developed by: Roland Proud (RP) <rp43@st-andrews.ac.uk> 
|               Pelagic Ecology Research Group, University of St Andrews
| Contributors:
|
| Maintained by:
| Modification History:      
|
"""
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_pseudo_SSL(Sv_mean,Sv_std,yheight,ypos,col = 100,noise_level = -999):
    '''
    generate sound scattering layer from summary statistics and dimensions
    
    '''
    yheight                   = int(yheight)
    row                       = 3* yheight  
    grid                      = np.ones((row,col)) * 10**(noise_level/10.)
    grid[yheight:2*yheight,:] = np.reshape(np.random.normal(Sv_mean, Sv_std, col*yheight),\
                                (yheight,col))
    grid[grid <= 0]           = 10**(noise_level/10.)
    grid                      = 10*np.log10(grid)
    plot_Sv(grid)
    plt.yticks([yheight,yheight+yheight/2,2*yheight],\
               [str(ypos-yheight/2)[0:5],str(ypos)[0:5],str(ypos+yheight/2)[0:5]])
    
def save_png_plot(folder,filename,dpi = 300):
    '''
    save plot 
    '''
    ## save plot
    fig       = plt.gcf()   
    savedPath = os.getcwd()
    os.chdir(folder)
    fig.savefig(filename + '.png', dpi=dpi, format='png')
    os.chdir(savedPath)
    fig.clf()
    plt.close()
        
def plot_mask(mask):
    '''
    plot mask (any - binary/flag/continuous)
    '''
    ## shape
    row,col = mask.shape
    
    ## plot
    #f, (ax1) = plt.subplots(1, figsize = (20,10))
    p1       = plt.imshow(mask, cmap = plt.cm.spectral,\
            interpolation='nearest',aspect='auto')
    plt.colorbar(p1,pad = 0)
    plt.xlabel('columns',fontsize = 18)
    plt.ylabel('rows',fontsize = 18)

def plot_Sv(Sv,mask = None):
    '''
    :param Sv: gridded Sv values (dB re 1m^-1)
    :type  Sv: 2D numpy.array
    
    :param mask: binary mask (0 - noise; 1 - signal)
    :type  mask: 2D numpy.array
    
    return:
    
    desc: Plot Sv grid, with/without binary mask
    
    defined by RP
    
    status: dev
    
    '''
    ## get echoview colormap
    setup_ek500_cmap()
    ek500_cmap = mpl.cm.get_cmap('ek500')
    ek500_norm = mpl.colors.BoundaryNorm(np.linspace(-89,-34,12), 12, clip=False)
    
    ## add mask
    if mask is not None:
        Sv = np.ma.masked_where(mask == 0,Sv)
    
    ## shape
    row,col = Sv.shape
    
    ## plot
    #f, (ax1) = plt.subplots(1, figsize = (20,10))
    p1       = plt.imshow(Sv, cmap = ek500_cmap,norm = ek500_norm,\
            interpolation='nearest',aspect='auto')
    plt.colorbar(p1,pad = 0)
    plt.xlabel('columns',fontsize = 18)
    plt.ylabel('rows',fontsize = 18)

def setup_ek500_cmap():
    '''
    Creates the ek500 colormap and boundary norm
    Taken from pyecholab (Add ref)
    '''
    float_ek500_cmap_colorlist = [(0.62, 0.62, 0.62),
                            (0.37, 0.37, 0.37),
                            (0.0, 0.0, 1.0),
                            (0.0, 0.0, 0.498),
                            (0.0, 0.749, 0.0),
                            (0.0, 0.498, 0.0),
                            (1.0, 1.0, 0.0),
                            (1.0, 0.498, 0.0),
                            (1.0, 0.0, 0.749),
                            (1.0, 0.0, 0.0),
                            (0.651, 0.325, 0.235),
                            (0.471, 0.235, 0.157)]

    ek500_cmap = \
        mpl.colors.ListedColormap(float_ek500_cmap_colorlist, name='ek500')
    ek500_cmap.set_bad(color='k', alpha=1.0)
    ek500_cmap.set_under('w', alpha=1.0)
    ek500_cmap.set_over(color=float_ek500_cmap_colorlist[-1], alpha=1.0)
    
    if 'ek500' not in mpl.cm.cmap_d:
        mpl.cm.register_cmap('ek500', cmap=ek500_cmap)
    else:
        mpl.cm.cmap_d['ek500'] = ek500_cmap
