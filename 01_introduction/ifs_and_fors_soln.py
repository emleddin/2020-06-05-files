## Use Python 3

MD_programs = ['AMBER', 'CHARMM', 'GROMACS', 'LAMMPS', 'TINKER']

for program in MD_programs:
    if program == "TINKER":
        continue
    else:
        print("You don't have to convert from {} format to XYZ. Yet.".format(program))
