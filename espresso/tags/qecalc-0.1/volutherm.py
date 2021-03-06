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
from thermo.thermodyn import PhononThermodynamics
from voluphon import VoluPhon

class VoluTherm():
    def __init__(self, fname, indexRange, prcntVolume, a_range, c_range, e_range):
        """Hexogonal cell for now"""
        import os
        #Initialize and fit from volume expansion:
        self.voluPhon = VoluPhon(fname, prcntVolume)
        self.voluPhon.setPhonons(indexRange, 'polynom', 2, False)
        self.voluPhon.setA(a_range, 'polynom', 1, True)
        self.voluPhon.setC(c_range, 'polynom', 1, True)
        self.voluPhon.setEnergy(e_range, 'polynom', 4, True)

        # prepare QHA program need to generate partial_DOS file
        cmdstr = 'cp ./' + str(indexRange[0]) +'_' + \
                   self.voluPhon.phonQHA.matdynModes + ' ./matdyn.modes'
        os.system(cmdstr)
#        self.voluPhon.phonQHA.loadPhonons()
        os.system('./Partial_phonon_DOS.x < phdos1.in')


    def totalFreeEnergy(self, prcntVolumeValue, *params):
        """Total Free Energy calculation
           How to use:
           File requirements in current directory:
           1) x_matdyn.modes files obtained from QHA
           2) ttrinp_hcp file (in case of hexogonal symmetry) (from QHA program)
           3) phonon_dos.x (from QHA program)
           4) phdos.in
           --------------
           5) phdos1.in
           6) matdyn.modes
           7) tetra.x
           8  Partial_phonon_DOS.x"""
        temperature = params[0]
        # Obtain phonon DOS from Isaev's QHA program:
        print "\nprcntVolumeValue = " ,prcntVolumeValue
        print "a = ", self.voluPhon.a.fittedValue(prcntVolumeValue)
        print "c = ", self.voluPhon.c.fittedValue(prcntVolumeValue)
        self.voluPhon.phonQHA.structure.lattice.a = \
                                   self.voluPhon.a.fittedValue(prcntVolumeValue)
        self.voluPhon.phonQHA.structure.lattice.c = \
                                   self.voluPhon.c.fittedValue(prcntVolumeValue)
        # will set freqs and recompute q-points:
        self.voluPhon.phonQHA.setFreqs( \
                              self.voluPhon.freqs.fittedFreqs(prcntVolumeValue))
        self.voluPhon.phonQHA.dosRelauncher()
        axis, dos = self.voluPhon.phonQHA.DOS()
        phonTherm = PhononThermodynamics(axis, dos)
        Cv = phonTherm.Cv(temperature)
        phononFreeEnergy = phonTherm.freeEnergy(temperature)
        F = self.voluPhon.energy.fittedValue(prcntVolumeValue)+phononFreeEnergy

        print "Total energy, phonon energy = ", \
        self.voluPhon.energy.fittedValue(prcntVolumeValue), phononFreeEnergy
               
        print "Total free energy = ", F
        # energy assumed to be in Ry !!!
        return Cv, F, self.voluPhon.energy.fittedValue(prcntVolumeValue), \
               phononFreeEnergy

    def totalFreeEnergyBrent(self, prcntVolumeValue, *params):
        """Free energy calculation wrapper for brent minimization"""
        temperature = params[0]
        Cv, total, electronic, phonon = \
                            totalFreeEnergy(self, prcntVolumeValue, temperature)
        return total

    def minimizeFreeEnergy(self, temperature):
        import scipy.optimize        
        brentOut=scipy.optimize.brent(self.totalFreeEnergyBrent,(temperature,),
           (self.voluPhon.prcntVolume()[0], self.voluPhon.prcntVolume()[-1]),\
                          tol = 1.e-5, full_output = 1)
        print '\n\nBrentOut:'
        print brentOut
        optPrcntVolume = brentOut[0]
        optFreeEnergy = brentOut[1]
        print "\nOptimized lattice parameters:"
        a = self.voluPhon.a.fittedValue(optPrcntVolume)
        c = self.voluPhon.c.fittedValue(optPrcntVolume)
        print 'a = ', a
        print 'c = ', c
        return a, c, optPrcntVolume


if __name__ == "__main__":
    print "Hello World";

__author__="markovsk"
__date__ ="$Sep 17, 2009 10:51:10 AM$"
