import MDAnalysis as mda

propka_output="../2-propka_output/p09m0bn8cm.pqr"
pdb_out="5Y2S_ph7_protonated.pdb"

system = mda.Universe(propka_output, format="PQR", dt=1.0, in_memory=True)

## Remove the segment IDs (w/o this, `SYST` gets annoyingly printed by element)
for atom in system.atoms:
    atom.segment.segid = ''

system.atoms.write(pdb_out)
