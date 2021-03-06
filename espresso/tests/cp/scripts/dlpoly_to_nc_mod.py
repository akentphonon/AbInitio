#!python

# Conversion of a DLPOLY trajectory to MMTK's trajectory format.
#
# Usage: dlpoly_to_nc dlpoly_directory nc_file
#

from MMTK import *
from MMTK.Trajectory import Trajectory, SnapshotGenerator, TrajectoryOutput
from Scientific.IO.FortranFormat import FortranLine, FortranFormat
import Numeric, getopt, os, string, sys

usage = """Usage: dlpoly_to_nc [options] dlpoly_directory nc_file

dlpoly_directory must contain the files FIELD and HISTORY.

Options:

  --block-size=number
     specifies the block structure of the netCDF trajectory. The
     default value of 1 optimizes the trajectory for step-by-step access
     to conformations. Larger values favour atom-by-atom access to
     one-particle trajectories for all times, which is required for the
     calculation of dynamic quantities. The highest sensible value is
     the number of steps in the trajectory.


To write the DLPOLY trajectory directly into a netCDF file without
creating an intermediate ASCII file, do the following:

1) Type 'mkfifo HISTORY' in dlpoly_directory.
2) Start dlpoly_to_nc.
3) Start DLPOLY.
"""

_elements2 = ['cl', 'as', 'in', 'tb', 'tl', 'he', 'ar', 'se', 'sn',
'dy', 'pb', 'li', 'br', 'sb', 'ho', 'bi', 'be', 'ca', 'kr', 'te',
'er', 'po', 'sc', 'rb', 'tm', 'at', 'ti', 'sr', 'xe', 'yb', 'rn',
'cs', 'lu', 'fr', 'cr', 'zr', 'ba', 'hf', 'ra', 'mn', 'nb', 'la',
'ta', 'ac', 'ne', 'fe', 'mo', 'ce', 'th', 'na', 'co', 'tc', 'pr',
're', 'pa', 'mg', 'ni', 'ru', 'nd', 'os', 'al', 'cu', 'rh', 'pm',
'ir', 'np', 'si', 'zn', 'pd', 'sm', 'pt', 'pu', 'ga', 'ag', 'eu',
'au', 'am', 'ge', 'cd', 'gd', 'hg', 'cm', 'cf']

field_atom_line = FortranFormat('A8,2F12,3I5')
history_timestep_line = FortranFormat('A8,4I10,F12.6')
history_pbc_line = FortranFormat('3G12.4')

class DLPOLYData:

    def __init__(self, directory):
        self.directory = directory
        self.history = open(os.path.join(self.directory, 'HISTORY'))
        self.title = string.strip(self.history.readline())
        info = FortranLine(self.history.readline(), '2I10')
        if info[1] > 3:
            raise ValueError, "box shape not implemented"
        nvectors = info[0]+1
        self.makeUniverse(info[1], self.readField())
        if nvectors > 1:
            self.universe.initializeVelocitiesToTemperature(0.)

    def checkDirective(self, line, directive):
        return string.upper(line[:len(directive)]) == directive

    def readField(self):
        filename = os.path.join(self.directory, 'FIELD')
        lines = open(filename).readlines()
        while 1:
            if self.checkDirective(lines[0], 'MOLECULES'):
                nspecies = string.atoi(string.split(lines[0])[1])
                break
            if self.checkDirective(lines[0], 'MOLECULAR TYPES'):
                nspecies = string.atoi(string.split(lines[0])[2])
                break
            lines = lines[1:]
        lines = lines[1:]
        species = []
        for i in range(nspecies):
            name = string.strip(lines[0])
            n = string.atoi(string.split(lines[1])[1])
            natoms = string.atoi(string.split(lines[2])[1])
            lines = lines[3:]
            atoms = []
            while natoms > 0:
                data = FortranLine(lines[0], field_atom_line)
                lines = lines[1:]
                atom_name = string.strip(data[0])
                element = string.lower(atom_name[:2])
                if element not in _elements2:
                    element = element[0]
                nrepeat = max(data[3], 1)
                for j in range(nrepeat):
                    atoms.append((element, atom_name))
                natoms = natoms - nrepeat
            while (not self.checkDirective(lines[0], 'FINISH')) \
                  and (not self.checkDirective(lines[0], 'CONSTRAINTS')):
                lines = lines[1:]
            constraints = []
            if self.checkDirective(lines[0], 'CONSTRAINTS'):
                nc = string.atoi(string.split(lines[0])[1])
                lines = lines[1:]
                while nc > 0:
                    l = string.split(lines[0])
                    i1 = int(l[0])-1
                    i2 = int(l[1])-1
                    d = float(l[2])*Units.Ang
                    constraints.append((i1, i2, d))
                    lines = lines[1:]
                    nc = nc - 1
                while not self.checkDirective(lines[0], 'FINISH'):
                    lines = lines[1:]
            lines = lines[1:]
            species.append([name, n, atoms, constraints])
        return species

    def makeUniverse(self, pbc, molecules):
        if pbc == 0:
            self.universe = InfiniteUniverse()
        else:
            self.universe = OrthorhombicPeriodicUniverse((0., 0., 0.))
        number = 0
        for mol_name, mol_count, atoms, constraints in molecules:
            for i in range(mol_count):
                atom_objects = []
                for element, name in atoms:
                    a = Atom(element, name = name)
                    a.number = number
                    number = number + 1
                    atom_objects.append(a)
                if len(atom_objects) == 1:
                    self.universe.addObject(atom_objects[0])
                else:
                    ac = AtomCluster(atom_objects, name = mol_name)
                    for i1, i2, d in constraints:
                        ac.addDistanceConstraint(atom_objects[i1],
                                                 atom_objects[i2],
                                                 d)
                    self.universe.addObject(ac)
        self.universe.configuration()

    def writeTrajectory(self, trajectory_name, block_size=1):
        trajectory = Trajectory(self.universe, trajectory_name, 'w',
                                self.title, block_size=block_size)
        actions = [TrajectoryOutput(trajectory, ["all"], 0, None, 1)]
        snapshot = SnapshotGenerator(self.universe, actions=actions)
        conf = self.universe.configuration()
        vel = self.universe.velocities()
        grad = ParticleVector(self.universe)
        try:
            while 1:
                line = self.history.readline()
                if not line:
                    break
                data = FortranLine(line, history_timestep_line)
                step = data[1]
                natoms = data[2]
                nvectors = data[3]+1
                pbc = data[4]
                dt = data[5]
                step_data = {'time': step*dt}
                if nvectors > 2:
                    step_data['gradients'] = grad
                if pbc:
                    data = FortranLine(self.history.readline(), history_pbc_line)
                    box_x = data[0]*Units.Ang
                    if data[1] != 0. or data[2] != 0.:
                        raise ValueError, "box shape not supported"
                    data = FortranLine(self.history.readline(), history_pbc_line)
                    box_y = data[1]*Units.Ang
                    if data[0] != 0. or data[2] != 0.:
                        raise ValueError, "box shape not supported"
                    data = FortranLine(self.history.readline(), history_pbc_line)
                    box_z = data[2]*Units.Ang
                    if data[0] != 0. or data[1] != 0.:
                        raise ValueError, "box shape not supported"
                    self.universe.setSize((box_x, box_y, box_z))
                for i in range(natoms):
                    self.history.readline()
                    conf.array[i] = map(float,
                                        string.split(self.history.readline()))
                    if nvectors > 1:
                        vel.array[i] = map(float,
                                           string.split(self.history.readline()))
                        if nvectors > 2:
                            grad.array[i] = map(float,
                                             string.split(self.history.readline()))
                Numeric.multiply(conf.array, Units.Ang, conf.array)
                if nvectors > 1:
                    Numeric.multiply(vel.array, Units.Ang/Units.ps, vel.array)
                if nvectors > 2:
                    Numeric.multiply(grad.array, -Units.amu*Units.Ang/Units.ps**2,
                                     grad.array)

                snapshot(data=step_data)
        finally:
            trajectory.close()


try:
    options, file_args = getopt.getopt(sys.argv[1:], '', ['block-size='])
except getopt.GetoptError:
    sys.stderr.write(usage)
    raise SystemExit

block_size = 1
for option, value in options:
    if option == '--block-size':
        block_size = int(value)
        if block_size < 1:
            sys.stderr.write("Block size must be positive.")
            raise SystemExit

if len(file_args) != 2:
    sys.stderr.write(usage)
    raise SystemExit
directory = file_args[0]
nc_file = file_args[1]

if not os.path.exists(os.path.join(directory, 'FIELD')):
    sys.stderr.write("No FIELD file in " + directory + ".\n")
    raise SystemExit
if not os.path.exists(os.path.join(directory, 'HISTORY')):
    sys.stderr.write("No HISTORY file in " + directory + ".\n")
    raise SystemExit


if os.path.exists(nc_file):
    sys.stderr.write('File %s already exists. ' % nc_file)
    while 1:
        answer = raw_input('Overwrite? [y/n] ')
        if answer == 'n':
            raise SystemExit
        if answer == 'y':
            break

data = DLPOLYData(directory)
data.writeTrajectory(nc_file, block_size)
