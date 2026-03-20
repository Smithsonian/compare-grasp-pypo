
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import PyPO.Colormaps as cmaps

amp_cmap = cmaps.parula
phs_cmap = cmaps.parula

def plotGraspBeam2D(field, comp=0, comp_name='E', title=None, reim=False, vmax=None, vmin=None, norm=True):
    
    comps = ["x", "y", "z"]
    
    if title is None:
        title = f"${comp_name}_{comps[comp]}$"
    else:
        title = f"{title} ${comp_name}_{comps[comp]}$"
    
    if reim:
        if vmax is None:
            vmax = max(np.max(np.real(field.field[:,:,comp])), np.max(np.imag(field.field[:,:,comp])), -np.min(np.real(field.field[:,:,comp])), -np.min(np.imag(field.field[:,:,comp])))
            vmin = -vmax
        else:
            if vmin is None:
                vmin = -vmax
    else:
        if vmax is None:
            vmax = 20*np.log10(np.max(np.abs(field.field[:,:,comp])))
            if vmin is None:
                vmin = 20*np.log10(np.min(np.abs(field.field[:,:,comp])))
            else:
                vmin = vmax + vmin


    fig, ax = plt.subplots(1,2, figsize=(12,5))
    if reim:
        ampplt = ax[0].pcolormesh(field.positions[0], field.positions[1], field.field[:,:,comp].real, cmap=amp_cmap, vmin=vmin, vmax=vmax)
        phsplt = ax[1].pcolormesh(field.positions[0], field.positions[1], field.field[:,:,comp].imag, cmap=amp_cmap, vmin=vmin, vmax=vmax)
        ax[0].set_title("Re(F) (√W)")
        ax[1].set_title("Im(F) (√W)")
    else:
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


def plotBeam2D(grid, field, comp='Ex', farfield=False, correct_phase=1, title=None, vmax=None, vmin=None, norm=True):

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
    if farfield:
        ampplt = ax[0].pcolormesh(np.rad2deg(grid["x"]*np.cos(grid["y"])), np.rad2deg(grid["x"]*np.sin(grid["y"])), 20*np.log10(np.abs(field[comp])), cmap=amp_cmap, vmin=vmin, vmax=vmax)
        phsplt = ax[1].pcolormesh(np.rad2deg(grid["x"]*np.cos(grid["y"])), np.rad2deg(grid["x"]*np.sin(grid["y"])), np.angle(field[comp]*phase_factor), cmap=phs_cmap)
    else:
        ampplt = ax[0].pcolormesh(grid["x"], grid["y"], 20*np.log10(np.abs(field[comp])), cmap=amp_cmap, vmin=vmin, vmax=vmax)
        phsplt = ax[1].pcolormesh(grid["x"], grid["y"], np.angle(field[comp]*phase_factor), cmap=phs_cmap)


    ax[0].set_title("Amplitude (dB)")
    ax[1].set_title("Phase (rad)")

    cax = []
    for a in ax:
        a.set_aspect("equal")
        if farfield:
            a.set_ylabel("Az (°)")
            a.set_xlabel("El (°)")
        else:
            a.set_ylabel("y (mm)")
            a.set_xlabel("x (mm)")

        divider = make_axes_locatable(a)
        cax.append(divider.append_axes('right', size='5%', pad=0.05))

    camp = fig.colorbar(ampplt, cax=cax[0], orientation='vertical')
    cphs = fig.colorbar(phsplt, cax=cax[1], orientation='vertical')

    fig.suptitle(title)

    fig.tight_layout()
    
    return fig, ax

def plotBeamCut(grid, field, cut, gmode='uv', comp='Ex', figax=None, phase=True, farfield=False, correct_phase=0, title=None, label=None, vmax=None, vmin=None, norm=True, **kwargs):
    
    cuts = ["x", "y", "d"]

    if isinstance(cut, int):
        cut = cuts[cut]
    
    # Only works with uv grids over full disc with sizes divisible by 8
    
    shape = grid['x'].shape
    k = field['k']
    
    if cut == 'x':
        if gmode == 'xy':
            x = grid['x'][:,int((shape[1]-1)/2)]
            z = grid['z'][:,int((shape[1]-1)/2)]
            y = field[comp][:,int((shape[1]-1)/2)]
        elif gmode == 'uv':
            x = np.concat((grid['x'][::-1,int(shape[1]/2)], grid['x'][:,0]))
            z = np.concat((grid['z'][::-1,int(shape[1]/2)], grid['z'][:,0]))
            y = np.concat((field[comp][::-1,int(shape[1]/2)], field[comp][:,0]))
        else: # AoE grid
            r = grid['x'][:,int((shape[1]-1)/2)]
            phi = grid['y'][:,int((shape[1]-1)/2)]
            x = np.rad2deg(r*np.cos(phi))
            y = field[comp][:,int((shape[1]-1)/2)]
    elif cut == 'y':
        if gmode =='xy':
            x = grid['y'][int((shape[0]-1)/2),:]
            z = grid['z'][int((shape[0]-1)/2),:]
            y = field[comp][int((shape[0]-1)/2),:]
        elif gmode == 'uv':
            x = np.concat((grid['y'][::-1,int(shape[1]*3/4)], grid['y'][:,int(shape[1]/4)]))
            z = np.concat((grid['z'][::-1,int(shape[1]*3/4)], grid['z'][:,int(shape[1]/4)]))
            y = np.concat((field[comp][::-1,int(shape[1]*3/4)], field[comp][:,int(shape[1]/4)]))
        else: # AoE grid
            r = grid['x'][int((shape[0]-1)/2),:]
            phi = grid['y'][int((shape[0]-1)/2),:]
            x = np.rad2deg(r*np.sin(phi))
            y = field[comp][int((shape[0]-1)/2),:]
    else: # cut == 'd'
        if gmode =='xy':
            # Only works with square grids
            x = np.sign(np.diagonal(grid['x']))*np.sqrt(np.diagonal(grid['x'])**2 + np.diagonal(grid['y'])**2)
            z = np.diagonal(grid.z)
            y = np.diagonal(field[comp])
        elif gmode == 'uv':
            x = np.sqrt(2)*np.concat((grid['x'][::-1,int(shape[1]*5/8)], grid['x'][:,int(shape[1]/8)]))
            z = np.concat((grid['z'][::-1,int(shape[1]*5/8)], grid['z'][:,int(shape[1]/8)]))
            y = np.concat((field[comp][::-1,int(shape[1]*5/8)], field[comp][:,int(shape[1]/8)]))
        else: # AoE grid
            r = np.sign(np.diagonal(grid['y']))*np.diagonal(grid['x'])
            phi = np.diagonal(grid['y'])
            x = np.rad2deg(r)
            y = np.diagonal(field[comp])
    
    if label is None:
        label = f"{cut}-cut ${comp[0]}_{comp[1]}$"
    else:
        label = f"{label} ${comp[0]}_{comp[1]}$"
    
    if vmax is None:
        vmax = 20*np.log10(np.max(np.abs(y)))
        if vmin is None:
            vmin = 20*np.log10(np.min(np.abs(y)))
        else:
            vmin = vmax + vmin

    if figax is None:
        if phase:
            fig, ax = plt.subplots(1,2, figsize=(10,5))
        else:
            fig = plt.figure(figsize=(5,5))
            ax = fig.gca()
    else:
        fig, ax = figax
        
    if isinstance(ax, np.ndarray):
        
        if isinstance(correct_phase, bool):
            correct_phase = int(correct_phase)
        
        if phase and correct_phase:
            phase_factor = np.exp(correct_phase*1j*k*z)
        else:
            phase_factor = np.ones_like(x)
        
        ampplt = ax[0].plot(x, 20*np.log10(np.abs(y)), label=label, **kwargs)
        phsplt = ax[1].plot(x, np.angle(y*phase_factor), label=label, **kwargs)

        ax[0].set_ylabel("Amplitude (dB)")
        ax[1].set_ylabel("Phase (rad)")

        for a in ax:
            if farfield:
                a.set_xlabel("$\theta$ (°)")
            else:
                a.set_xlabel("r (mm)")
            a.legend()
        
        if figax is None:
            ax[0].set_ylim((vmin, vmax+1))
    else:
        ampplt = ax.plot(x, 20*np.log10(np.abs(y)), label=label, **kwargs)

        ax.legend()
        ax.set_ylabel("Amplitude (dB)")
        if farfield:
            ax.set_xlabel("$\theta$ (°)")
        else:
            ax.set_xlabel("r (mm)")
        
        if figax is None:
            ax.set_ylim((vmin, vmax))
        
    if title is not None:
        fig.suptitle(title)

    fig.tight_layout()
    
    return fig, ax


def plotGraspBeamCut(field, cut, grid='rect', comp=0, comp_name='E', figax=None, phase=True, farfield=False, title=None, label=None, vmax=None, vmin=None, norm=True, phase_offset=0, **kwargs):
    
    comps = ["x", "y", "z"]
    cuts = ["x", "y", "d"]

    shape = field.positions[0].shape
    if isinstance(cut, int):
        cut = cuts[cut]
    
    # Only works with uv grids over full disc
    
    if cut == 'x':
        if grid=='rect':
            x = field.positions[0][int(shape[1]/2),:]
            y = field.field[:,int(shape[1]/2), comp]
        else:
            x = field.positions[0][:,0]
            y = field.field[:,0,comp]
    elif cut == 'y':
        if grid=='rect':
            x = field.positions[1][:,int(shape[1]/2)]
            y = field.field[int(shape[0]/2),:,comp]
        else:
            x = field.positions[0][:,int(shape[1]/4) - 1]
            y = field.field[:,int(shape[1]/4) - 1,comp]
    else: # cut == 'd'
        if grid=='rect':
            # Only works with square grids
            x = np.sign(np.diagonal(field.positions[0]))*np.sqrt(np.diagonal(field.positions[0])**2 + np.diagonal(field.positions[1])**2)
            y = np.diagonal(field.field[:,:,comp])
        else:
            x = field.positions[0][:,int(shape[1]/8) - 1]
            y = field.field[:,int(shape[1]/8) - 1,comp]
            
    if not farfield:
        x = x*1e3
    
    if label is None:
        label = f"{cut}-cut ${comp_name}_{comps[comp]}$"
    else:
        label = f"{label} ${comp_name}_{comps[comp]}$"
    
    if vmax is None:
        vmax = 20*np.log10(np.max(np.abs(y)))
        if vmin is None:
            vmin = 20*np.log10(np.min(np.abs(y)))
        else:
            vmin = vmax + vmin

    if figax is None:
        if phase:
            fig, ax = plt.subplots(1,2, figsize=(10,5))
        else:
            fig = plt.figure(figsize=(5,5))
            ax = fig.gca()
    else:
        fig, ax = figax
        
    if isinstance(ax, np.ndarray):
        ampplt = ax[0].plot(x, 20*np.log10(np.abs(y)), label=label, **kwargs)
        phsplt = ax[1].plot(x, np.angle(y*np.exp(1j*phase_offset)), label=label, **kwargs)


        ax[0].set_ylabel("Amplitude (dB)")
        ax[1].set_ylabel("Phase (rad)")

        for a in ax:
            if farfield:
                a.set_xlabel("$\\theta$ (°)")
            else:
                a.set_xlabel("r (mm)")
            a.legend()
        
        if figax is None:
            ax[0].set_ylim((vmin, vmax+1))
    else:
        ampplt = ax.plot(x, 20*np.log10(np.abs(y)), label=label, **kwargs)

        ax.legend()
        ax.set_ylabel("Amplitude (dB)")
        if farfield:
            ax.set_xlabel("$\theta$ (°)")
        else:
            ax.set_xlabel("r (mm)")
        
        if figax is None:
            ax.set_ylim((vmin, vmax))
        
    if title is not None:
        fig.suptitle(title)

    fig.tight_layout()
    
    return fig, ax