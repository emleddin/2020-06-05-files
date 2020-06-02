import simtk as omm
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from simtk.openmm import app

parm_in = "5Y2S_wat.prmtop"
coord_in = "5Y2S_wat_init0.rst"
chk_in = "5Y2S_wat.chk"

outlog = "output.log"
chk_out = "5Y2S_wat_cont.chk"
traj_out = "5Y2S_wat_2.dcd"

prmtop = app.AmberPrmtopFile(parm_in)
inpcrd = app.AmberInpcrdFile(coord_in)

# Using Particle-mesh Ewald
system = prmtop.createSystem(nonbondedMethod = app.PME,
    # with a 10 Angstrom cutoff distance
    nonbondedCutoff = 1.0*nanometers,
    # keeping bonds between hydrogens and heavy atoms at a fixed length
    constraints = app.HBonds,
    # setting the error tolerance for the Ewald
    ewaldErrorTolerance = 0.001,
    # letting waters be flexible instead of solid triangles
    rigidWater = False,
    # maintains the center of the periodic box at the center of mass
    removeCMMotion = True)

# Temperature, Friction Coefficient, Timestep
# This will be added to the larger simulation
thermostat = LangevinIntegrator(300*kelvin, 1/picoseconds, 0.001*picoseconds)

# Pressure, Temperature (only used for calculation),
# Frequency (how frequently the system should update the box size)
barostat = MonteCarloBarostat(1.0*atmosphere, 300.0*kelvin, 25)

# The barostat is added directly to the system rather than the larger
# simulation.
system.addForce(barostat)

# The topology of the system
sim = Simulation(prmtop.topology,
    # The system itself, with all the restraints, barostat, etc.
    system,
    # The thermostat, in this case the LangevinIntegrator we established before
    thermostat)

"""
## Add distance or angle restraints
# Add distance restraints
distance_restraints = HarmonicBondForce()
# First atom index (python starts at zero!), Second atom index, Distance,
# Force Constant
# You can use as many addBond() function calls as you like, if there are
# multiple distances to restrain.
# But be careful not to duplicate any, as they won't overwrite each other,
# just additively stack up.
distance_restraints.addBond(index1, index2, distance*angstroms,
    force*kilocalories_per_mole/angstroms**2)

# Add the collection of distance restraints to your system.
system.addForce(distance_restraints)

# Add angle restraints
angle_restraints = HarmonicAngleForce()
# First, second, and third atom indices, with the second atom as the vertex of
# the angle, the desired angle in radians, and the force constant.
# As above, add as many angle restraints as you need, but be careful not to
# duplicate them.
angle_restraints.addAngle(index1, index2, index3, angle,
    force*kilocalories_per_mole/radians**2)

# Add the collection of angle restraints to the system.
system.addForce(angle_restraints)
"""

"""
## Intended for new simulations!
# Gets the starting position for every atom in the system and
# initializes the simulation
sim.context.setPositions(inpcrd.getPositions(asNumpy=True))
"""

## Restart from Checkpoint

# Establishes the periodic boundary conditions of the system
# based on the box size.
sim.context.getState(getPositions=True, enforcePeriodicBox=True).getPositions()

# Filename to save the state data into.
sim.reporters.append(StateDataReporter(outlog,
    1000,   # number of steps between each save.
    step = True,             # writes the step number to each line
    time = True,             # writes the time (in ps)
    potentialEnergy = True,  # writes potential energy of the system (KJ/mole)
    kineticEnergy = True,    # writes the kinetic energy of the system (KJ/mole)
    totalEnergy = True,      # writes the total energy of the system (KJ/mole)
    temperature = True,      # writes the temperature (in K)
    volume = True,           # writes the volume (in nm^3)
    density = True))         # writes the density (in g/mL)

## Open checkpoint file
with open(chk_in,'rb') as f:
    sim.context.loadCheckpoint(f.read())

# Updates the checkpoint file every 10,000 steps
sim.reporters.append(CheckpointReporter(chk_out,10000))

# Adds another frame to the CHARMM-formatted DCD (which can be easily
# converted to .mdcrd by cpptraj) every 10,000 timesteps.
# It's good practice to keep the trajectory and checkpoint on the same
# write frequency, in case you need to stop a job and resume it later.
sim.reporters.append(DCDReporter(traj_out,10000))

"""
## Intended for new simulations!
# Minimize the system
sim.minimizeEnergy(maxIterations=2000)
"""

# This instructs the program to take 1,000,000 timesteps, which corresponds
# to 1.0 ns of MD based on a 1fs timestep.
sim.step(1000000)
