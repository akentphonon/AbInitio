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

"""
Notes on database classes implementation:
1. There are two alternative ways to perform action (update, create, delete) on database class:
    - Directly use clerk's methods (e.g. Clerk.updateRecord(record)) by passing the class object
        Pros: Saves extra call
        Cons: Not very convenient to write
    - Use DBTable methods (e.g. DBTable.updateRecord(params) by passing dictionary of parameters
      (e.g. params = {"id": 5, "name": "Hi", ...})
      Pros: Convenient for handling table forms?
2. Using DBTable methods does not require passing director every time you use it.
"""

from vinil.utils.utils import timestamp, newid, setname, ifelse
from pyre.db.Table import Table

NO_UPDATE   = ["timeCreated", "id"]
STAMPED     = ["timeCreated", "timeModified"]

class DBTable(Table):
    """ Abstract class for all the database tables"""
    
    def __init__(self, director, clerk):
        """
        clerk     - is set for actual managing database records
        idd       - is id generator
        """
        super(DBTable, self).__init__()
        self._clerk     = clerk
        self._director  = director


    def __init__(self):
        super(DBTable, self).__init__()
        self._clerk     = None
        self._director  = None


    def setClerk(self, clerk):
        self._clerk = clerk


    # Do I need it?
    def setIDD(self, idd):
        self._idd  = idd


    def setDirector(self, director):
        self._director  = director
        self._clerk     = director.clerk


    def updateRecord(self, params):
        """Tries to update record, otherwise complains"""
        for column in self.getColumnNames():
            if self._noUpdate(column):  # Do not updated values
                continue

            if self._stamp(column):     # Time is updated either to user specified value or to timestamp
                setattr(self, column, ifelse(params.get(column), params.get(column), timestamp()))
                continue

            setattr(self, column, setname(params, self, column))

        try:
            self._clerk.updateRecord(self)   # Commit to database
        except:
            raise   # Complain


    def createRecord(self, params):
        """Tries to create record, otherwise complains"""
        for column in self.getColumnNames():
            if self._id(column):
                setattr(self, column, ifelse(params.get(column), params.get(column), newid(self._director)))
                continue

            if self._stamp(column):
                setattr(self, column, ifelse(params.get(column), params.get(column), timestamp()))
                continue

            setattr(self, column, setname(params, self, column))

        try:
            self._clerk.insertRecord(self)   # Commit to database
        except:
            raise   # Complain
            

    def _noUpdate(self, value):
        """Value that should not be updated"""
        if value in NO_UPDATE:
            return True

        return False

    def _stamp(self, value):
        """Value that should be time stamped"""
        if value in STAMPED:
            return True

        return False

    def _id(self, value):
        if value == 'id':
            return True

        return False


    def deleteRecord(self):
        """Deletes record"""
        if self._clerk:
            self._clerk.deleteRecord(self, id=getattr(self, 'id'))


__date__ = "$Nov 6, 2009 11:25:22 AM$"


