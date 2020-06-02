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
hbond_out = '5Y2S_hbond.dat'

## Select residues/atoms of interest to calculate RMSD, hbonds, & RMSF
ROI = 'resid 1:261'

## Load in the trajectory
system = mda.Universe(prm, file1, format='DCD', dt=1.0)

## Reference (Crystal PDB)
ref = mda.Universe(pdb)

#----------------------#
#     Set-up HBA       #
#----------------------#
## Test for AMBER
# class HydrogenBondAnalysis_AMBER(HydrogenBondAnalysis):
class HydrogenBondAnalysis_AMBER(mda.analysis.hbonds.HydrogenBondAnalysis):
    # use tuple(set()) here so that one can just copy&paste names from the
    # table; set() takes care for removing duplicates. At the end the
    # DEFAULT_DONORS and DEFAULT_ACCEPTORS should simply be tuples.
    #
    #: default heavy atom names whose hydrogens are treated as *donors*
    #: (see :ref:`Default atom names for hydrogen bonding analysis`);
    #: use the keyword `donors` to add a list of additional donor names.
    DEFAULT_DONORS = {
        'AMBER': tuple(set([
            'N','OG','OG1','OE2','OH','NH1','NH2','NZ','OH','N2','ND1','NE', \
            'NE1','NE2','N2','N3','N4','N6','O5\'', 'OD2', ])),
        'CHARMM27': tuple(set([
            'N', 'OH2', 'OW', 'NE', 'NH1', 'NH2', 'ND2', 'SG', 'NE2', 'ND1', \
            'NZ', 'OG', 'OG1', 'NE1', 'OH'])),
        'GLYCAM06': tuple(set(['N', 'NT', 'N3', 'OH', 'OW'])),
        'other': tuple(set([]))}
    #
    #: default atom names that are treated as hydrogen *acceptors*
    #: (see :ref:`Default atom names for hydrogen bonding analysis`);
    #: use the keyword `acceptors` to add a list of additional acceptor names.
    DEFAULT_ACCEPTORS = {
        'AMBER': tuple(set([
            'O','OD1','OD2','OE1','OE2','N','ND1','NE2','NZ','OG','OG1','O1',\
            'O2','O4','O6','N1','N3','N6','N7','O1P','O2P','O3\'','O4\'','OH'])),
        'CHARMM27': tuple(set([
            'O', 'OC1', 'OC2', 'OH2', 'OW', 'OD1', 'OD2', 'SG', 'OE1', 'OE1', \
            'OE2', 'ND1', 'NE2', 'SD', 'OG', 'OG1', 'OH'])),
        'GLYCAM06': tuple(set(['N', 'NT', 'O', 'O2', 'OH', 'OS', 'OW', 'OY', 'SM'])),
        'other': tuple(set([]))}

#----------------------#
#         HBA          #
#----------------------#
# hbond_df =  pd.DataFrame(columns = ['#Frame', 'RMSD'])
# hbond = mda.analysis.hbonds.HydrogenBondAnalysis(system, distance=3.0, \
#  angle=120.0, pbc=True)

hbond = HydrogenBondAnalysis_AMBER(system, ROI, ROI, distance=3.0, angle=135.0, \
 forcefield='AMBER', pbc=True)
hbond.run()

## Save by frequency
new_hbond_df = pd.DataFrame(hbond.count_by_type())
new_hbond_df = new_hbond_df.sort_values(by=['frequency'], ascending=False)

new_hbond_df.to_csv(hbond_out, sep='\t', index=False, encoding='utf8', header=True)
