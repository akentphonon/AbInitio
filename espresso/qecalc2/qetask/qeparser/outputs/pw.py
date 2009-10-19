#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# QEcalc              by DANSE Inelastic group
#                     Brent Fultz
#                     California Institute of Technology
#                     (C) 2009  All Rights Reserved
#
# File coded by:      Nikolay Markovskiy
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import string
from qe_io_dict import *
import numpy
from baseoutput import BaseOutput

class Output(BaseOutput):

    def __init__(self):
        BaseOutput.__init__(self)
        self.parsers = {
                    'total energy'       : self.getTotalEnergy,
                    'lattice parameters' : self.getLatticeParameters,
                    'stress'             : self.getStress,
                    'forces'             : self.getForces,
                   }

    def getTotalEnergy(self, pwscfOutput):
        'Extract total energy value from pwscf output'
        #read Espresso output into memory:
        pwscfOut = read_file(pwscfOutput)
        key = find_key_from_marker_string(pwscfOut, '!', 'total energy')
        words = string.split(pwscfOut[key])
        return ([float(words[4])], 'Ry')

    def getLatticeParameters(self, pwscfOutput):
        """Extract lattice parameters after pwscf geometry optimization
           Returns a list of 6 parameters: A, B, C, cos(BC), cos(AC), cos(AB)"""
        # Not Functional !
        return None
        from qelattice import QELattice
        # obtain lattice from PWSCF input file:
        lat = QELattice(fname = pwscfInput)
        pwscfOut = read_file(pwscfOutput)
        key_a_0 = find_key_from_string(pwscfOut, 'lattice parameter (a_0)')
        a_0 = float( string.split( pwscfOut[key_a_0] )[4] )
        if lat.type == 'traditional': a_0 = a_0*0.529177249 # convert back to angstrom
        keyEnd = max( find_all_keys_from_marker_string(pwscfOut, '!', 'total energy') )
        keyCellPar = find_key_from_string_afterkey(pwscfOut, keyEnd, \
                                                  'CELL_PARAMETERS (alat)') + 1
        latticeVectors = [[float(valstr)*a_0 for valstr in string.split( pwscfOut[keyCellPar] ) ],
                         [ float(valstr)*a_0 for valstr in string.split( pwscfOut[keyCellPar+1] ) ],
                         [ float(valstr)*a_0 for valstr in string.split( pwscfOut[keyCellPar+2] ) ]]
        lat.setLatticeFromQEVectors(lat.ibrav, latticeVectors)
        return [lat.a, lat.b, lat.c, lat.cBC ,lat.cAC , lat.cAB]

    def getStress(self, pwscfOutput):
        '''Extract total stress in kbar after pwscf launch or geometry optimization'''
        pwscfOut = read_file(pwscfOutput)
        key = find_last_key_from_string(pwscfOut, 'total   stress  (Ry/bohr**3)') + 1
        stress = [[float(val) for val in string.split( pwscfOut[key] )[3:] ],
                  [float(val) for val in string.split( pwscfOut[key+1] )[3:] ],
                  [float(val) for val in string.split( pwscfOut[key+2] )[3:] ]]
        return (stress, 'Ry/bohr**3')

    def getForces(self, pwscfOutput):
        pwscfOut = read_file(pwscfOutput)
        key = find_last_key_from_string(pwscfOut, 'Forces acting on atoms (Ry/au):') + 2
        forces = []
        while 'atom' in pwscfOut[key]:
            forces.append([float(val) for val in string.split( pwscfOut[key] )[6:]])
            key = key + 1
        return (forces, 'Ry/au')

if __name__ == "__main__":
    print "Hello World";

__author__="Nikolay Markovskiy"
__date__ ="$Oct 18, 2009 6:52:35 PM$"