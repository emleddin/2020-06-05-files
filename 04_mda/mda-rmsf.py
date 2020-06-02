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
rmsf_out = '5Y2S_rmsf.dat'

rmsf_plot = '5Y2S_RMSF.png'

## Select residues/atoms of interest to calculate RMSD, hbonds, & RMSF
ROI = 'resid 1:261'

## Load in the trajectory
system = mda.Universe(prm, file1, format='DCD', dt=1.0)

## Reference (Crystal PDB)
ref = mda.Universe(pdb)

#----------------------#
#         RMSF         #
#----------------------#
## Select group of residues
resnames = system.select_atoms(ROI)
## Get residue weights
res_weights = mda.lib.util.get_weights(resnames, weights='mass')

## Run for individual residues
rmsf = mda.analysis.rms.RMSF(resnames)
rmsf.run()

## Apply weights to the by-atom fluctuations
weight_rmsf = []
for atom in range(len(rmsf.rmsf)):
    ## weight_rmsf = fluctuation * atom_mass / residue_mass
    weight_rmsf.append( (rmsf.rmsf[atom] *
     ( res_weights[atom] / rmsf.atomgroup[atom].residue.mass)) )

## Combine into by-residue value
byres_rmsf = resnames.accumulate(weight_rmsf, compound='residues')

## Create a Pandas dataframe with info
rmsf_df =  pd.DataFrame(columns = ['#Res', 'AtomicFlx'])
for i in range(len(byres_rmsf)):
    rmsf_df = rmsf_df.append({
    "#Res" : resnames.residues[i].resnum,
    "AtomicFlx" : byres_rmsf[i]
    }, ignore_index=True)

## Round to 4 digits
rmsf_df = rmsf_df.round(4)

rmsf_df.to_csv(rmsf_out, sep='\t', index=False, encoding='utf8', header=True)

#----------------------#
#        Plots         #
#----------------------#

plt.plot(rmsf_df['#Res'], rmsf_df['AtomicFlx'])
plt.xlabel('Residue')
plt.ylabel('RMSF ($\AA$)')
plt.savefig(rmsf_plot, dpi=300)
