#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# QEcalc              by DANSE Inelastic group
#                     Nikolay Markovskiy
#                     California Institute of Technology
#                     (C) 2010  All Rights Reserved
#
# File coded by:      Nikolay Markovskiy
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from qetask import QETask
from qeparser.pwinput import PWInput
from qeparser.qeoutput import QEOutput

class CPTask(QETask):
    def __init__(self, filename = None,configString = None, cleanOutDir = False,\
                                                            sectionName = None):
        QETask.__init__(self, filename, configString, cleanOutDir)

        self.setParallel()


        # pw main input and output
        configDic = {
        'cpInput': 'cp.in',
        'cpOutput': 'cp.out',
        }

        # QE input file's path containing variables' defaults (will be moved to
        # QE input parser)
        self._path_defaults = {
        'outdir': './',
        'pseudo_dir': './',
        'prefix': 'cp'
        }

        if sectionName == None:
            name = self.name()
        else:
            name = sectionName

        self.setting.section(name, configDic)
        self.input = PWInput( self.setting.get('cpInput') )
        self.output = QEOutput(self.setting, type='cp')


    def cmdLine(self):
        return self._getCmdLine('cp.x', 'cpInput', 'pcputput')


    def name(self):
        return 'cp.x'

    def syncSetting(self):
        """
        When this method is called on launch(), the input file is already
        parsed and will be saved before the run...
        """

        self.input.parse()

        self.setting.syncPathInNamelist('outdir', 'control', 'outdir', \
                                                self.input, self._path_defaults)
        self.setting.syncPathInNamelist('pseudo_dir', 'control', 'pseudo_dir', \
                                                self.input, self._path_defaults)
        self.setting.syncPathInNamelist('prefix', 'control', 'prefix', \
                                                self.input, self._path_defaults)


        # Solve for pseudopotential locations
        species = self.input.structure.atomicSpecies
        for specie in species.keys():
            setattr(self.setting._paths, 'ps' + specie, self.setting.get('pseudo_dir') + species[specie].pseudopotential )