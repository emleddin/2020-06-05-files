import MDAnalysis as mda

#------------------------#
#       Input Files      #
#------------------------#
## Load in the parmtop
prm = '../03_openmm/5Y2S_wat.prmtop'

## Load in the trajectory files
file1 = '../03_openmm/5Y2S_wat.dcd'

#--------------------------------#
#     Outfiles and Run Info      #
#--------------------------------#
outfile = '5Y2S_final_frame.pdb'

## Load in the trajectory
system = mda.Universe(prm, file1, format='DCD', dt=1.0)

with mda.Writer(outfile, multiframe=False) as pdb:
    system.trajectory[-1]
    pdb.write(system)
