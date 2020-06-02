import MDAnalysis as mda
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from MDAnalysis.analysis import align, rms, hbonds

#------------------------#
#       Input Files      #
#------------------------#
## Load in the parmtop
prm = '../03_openmm/5Y2S_wat.prmtop'

## Load in the trajectory files
file1 = '../03_openmm/5Y2S_wat.dcd'

## Load in the prepared initial structure
pdb = '../02_structure_preparation/5-leap/5Y2S_wat.pdb'

#--------------------------------#
#     Outfiles and Run Info      #
#--------------------------------#
rmsd_out = '5Y2S_rmsd.dat'


rmsd_plot = '5Y2S_RMSD.png'

## Select residues/atoms of interest to calculate RMSD, hbonds, & RMSF
ROI = 'resid 1:261'

## Load in the trajectory
system = mda.Universe(prm, file1, format='DCD', dt=1.0)

## Reference (Crystal PDB)
ref = mda.Universe(pdb)

#----------------------#
#         RMSD         #
#----------------------#
## Select atoms for RMSD
resnames = system.select_atoms(ROI)
resnames_ref = ref.select_atoms(ROI)

## Get the RMSDs
rmsd = mda.analysis.rms.RMSD(resnames, resnames_ref)
rmsd.run()

## Create a Pandas dataframe with info
rmsd_df =  pd.DataFrame(columns = ['#Frame', 'RMSD'])
for i in range(len(rmsd.rmsd)):
    rmsd_df = rmsd_df.append({
    ## First indice is frame, then info is Frame, Time, RMSD aka [0, 1, 2]
    "#Frame" : rmsd.rmsd[i][0],
    "RMSD" : rmsd.rmsd[i][2]
    }, ignore_index=True)

## Round to 4 digits
rmsd_df = rmsd_df.round(4)

rmsd_df.to_csv(rmsd_out, sep='\t', index=False, encoding='utf8', header=True)

#----------------------#
#        Plots         #
#----------------------#
plt.plot(rmsd_df['#Frame'], rmsd_df['RMSD'])
plt.xlabel('Time (ps)')
plt.ylabel('RMSD ($\AA$)')
plt.savefig(rmsd_plot, dpi=300)
