#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.db.Table import Table
from vinil.utils.utils import ifelse
from vinil.utils.utils import timestamp

examples = (
            (1, 'MgB2_SP', 'Quantum Espresso', 'Single-Phonon', 'Single-Phonon simualtion', 'MgB2', '25-09-2009', '', True, False),
            (2, 'MgB2_E', 'Quantum Espresso', 'Total Energy', 'Electron simualtion', 'MgB2', '26-09-2009', '', True, False),
            (3, 'MgB2_MP', 'Quantum Espresso', 'Multi-Phonon', 'Multy-Phonon simualtion', 'MgB2', '27-09-2009', '', True, False),
            (4, 'Ni_Energy', 'Quantum Espresso', 'Total Energy', 'Total Energy simualtion', 'Ni', '25-09-2009', '', False, True),
            (5, 'Ni_E_DOS', 'Quantum Espresso', 'Electron DOS', 'Electron DOS simualtion', 'Ni', '26-09-2009', '', False, True),
            (6, 'Ni_Ph_DOS', 'Quantum Espresso', 'Multi-Phonon DOS', 'Multy-Phonon DOS simualtion', 'Ni', '27-09-2009', '', False, True)
            )

class Simulation(Table):

    name = "simulation"
    import pyre.db

    id = pyre.db.varchar(name="id", length=8)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    sname = pyre.db.varchar(name="sname", length=128, default='')
    sname.meta['tip'] = ""

    package = pyre.db.varchar(name="package", length=128, default='')
    package.meta['tip'] = ""

    type = pyre.db.varchar(name="type", length=128, default='')
    type.meta['tip'] = ""

    description = pyre.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = ""

    formula = pyre.db.varchar(name="formula", length=32, default='')
    formula.meta['tip'] = ""

    timeCreated = pyre.db.varchar(name="timeCreated", length=16, default='')
    timeCreated.meta['tip'] = "timeCreated"

    timeModified = pyre.db.varchar(name="timeModified", length=16, default='')
    timeModified.meta['tip'] = "timeModified"

    isFavorite = pyre.db.boolean(name="isFavorite", default=True)   #?
    isFavorite.meta['tip'] = ""

    isExample = pyre.db.boolean(name="isExample", default=False)
    isExample.meta['tip'] = ""

    def updateRecord(self, director, params):
        """
        Updates simulation row (even if key in params is not present).
        'id' ans 'timeCreated' cannot be updated!
        """
        self.sname          = ifelse(params.has_key('sname'), params.get('sname'), self.sname)
        self.package        = ifelse(params.has_key('package'), params.get('package'), self.package)
        self.type           = ifelse(params.has_key('type'), params.get('type'), self.type)
        self.description    = ifelse(params.has_key('description'), params.get('description'), self.description)
        self.formula        = ifelse(params.has_key('formula'), params.get('formula'), self.formula)
        self.timeModified   = timestamp()   # You cannot set 'timeModified' manually
        self.isFavorite     = ifelse(params.has_key('isFavorite'), params.get('isFavorite'), self.isFavorite)
        self.isExample      = ifelse(params.has_key('isExample'), params.get('isExample'), self.isExample)
        
        director.clerk.updateRecord(self)   # Update record



def inittable(db):
    def simulation(id, sname, package, type, description, formula, timeCreated, timeModified, isFavorite, isExample):
        r               = Simulation()
        r.id            = id
        r.sname         = sname
        r.package       = package
        r.type          = type
        r.description   = description
        r.formula       = formula
        r.timeCreated   = timeCreated
        r.timeModified  = timeModified
        r.isFavorite    = isFavorite
        r.isExample     = isExample
        return r


    records = []
    for e in examples:
        records.append(simulation(id        = e[0],
                                  sname     = e[1],
                                  package   = e[2],
                                  type      = e[3],
                                  description = e[4],
                                  formula   = e[5],
                                  timeCreated   = e[6],
                                  timeModified  = e[7],
                                  isFavorite = e[8],
                                  isExample = e[9]))

    for r in records: db.insertRow( r )
    return


def test():
    for e in examples:
        s = ""
        for v in e:
            s += "%s " % v
        print s

if __name__ == "__main__":
    test()



__date__ = "$Oct 5, 2009 8:53:44 AM$"


