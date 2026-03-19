
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import PyPO.Colormaps as cmaps

amp_cmap = cmaps.parula
phs_cmap = cmaps.parula

def plotGraspBeam2D(field, comp=0, comp_name='E', title=None, vmax=None, vmin=None, norm=True):
    
    comps = ["x", "y", "z"]
    
    if title is None:
        title = f"${comp_name}_{comps[comp]}$"
    else:
        title = f"{title} ${comp_name}_{comps[comp]}$"
    
    if vmax is None:
        vmax = 20*np.log10(np.max(np.abs(field.field[:,:,comp])))
        if vmin is None:
            vmin = 20*np.log10(np.min(np.abs(field.field[:,:,comp])))
        else:
            vmin = vmax + vmin


    fig, ax = plt.subplots(1,2, figsize=(12,5))
    ampplt = ax[0].pcolormesh(field.positions[0], field.positions[1], 20*np.log10(np.abs(field.field[:,:,comp])), cmap=amp_cmap, vmin=vmin, vmax=vmax)
    phsplt = ax[1].pcolormesh(field.positions[0], field.positions[1], np.angle(field.field[:,:,comp]), cmap=phs_cmap)


    ax[0].set_title("Amplitude (dB)")
    ax[1].set_title("Phase (rad)")

    cax = []
    for a in ax:
        a.set_aspect("equal")
        a.set_ylabel("y (mm)")
        a.set_xlabel("x (mm)")

        divider = make_axes_locatable(a)
        cax.append(divider.append_axes('right', size='5%', pad=0.05))

    camp = fig.colorbar(ampplt, cax=cax[0], orientation='vertical')
    cphs = fig.colorbar(phsplt, cax=cax[1], orientation='vertical')

    fig.suptitle(title)

    fig.tight_layout()
    
    return fig, ax


def plotBeam2D(grid, field, comp='Ex', correct_phase=1, title=None, vmax=None, vmin=None, norm=True):

    k = field["k"]
    
    if correct_phase:
        phase_factor = np.exp(correct_phase*1j*k*grid['z'])
    else:
        phase_factor = np.ones_like(grid['z'])
    
    if title is None:
        title = f"${comp[0]}_{comp[1]}$"
    else:
        title = f"{title} ${comp[0]}_{comp[1]}$"
    
    if vmax is None:
        vmax = 20*np.log10(np.max(np.abs(field[comp])))
        if vmin is None:
            vmin = 20*np.log10(np.min(np.abs(field[comp])))
        else:
            vmin = vmax + vmin


    fig, ax = plt.subplots(1,2, figsize=(12,5))
    ampplt = ax[0].pcolormesh(grid["x"], grid["y"], 20*np.log10(np.abs(field[comp])), cmap=amp_cmap, vmin=vmin, vmax=vmax)
    phsplt = ax[1].pcolormesh(grid["x"], grid["y"], np.angle(field[comp]*phase_factor), cmap=phs_cmap)


    ax[0].set_title("Amplitude (dB)")
    ax[1].set_title("Phase (rad)")

    cax = []
    for a in ax:
        a.set_aspect("equal")
        a.set_ylabel("y (mm)")
        a.set_xlabel("x (mm)")

        divider = make_axes_locatable(a)
        cax.append(divider.append_axes('right', size='5%', pad=0.05))

    camp = fig.colorbar(ampplt, cax=cax[0], orientation='vertical')
    cphs = fig.colorbar(phsplt, cax=cax[1], orientation='vertical')

    fig.suptitle(title)

    fig.tight_layout()
    
    return fig, ax