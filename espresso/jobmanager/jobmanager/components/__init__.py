# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def dds():
    from DataStorage import DataStorage
    return DataStorage('dds', 'dds')

# ? Can't find SSHer.csaccessor()
# Factory for SSHer, uses ssher.pml config file
def ssher(name='ssher', facility='csaccessor'):
    from SSHer import SSHer
    return SSHer(name=name, facility=facility)

## Redo
#def buildjob(*args, **kwds):
#    from JobBuilder import JobBuilder
#    builder = JobBuilder()
#    return builder(*args, **kwds)
#
## Redo
#def retrieveresults(*args, **kwds):
#    from ComputationResultsRetriever import ComputationResultsRetriever
#    retriever = ComputationResultsRetriever()
#    return retriever(*args, **kwds)

#def spawn(command, dry_run = 0, env = None):
#    from spawn import spawn
#    return spawn(command, dry_run, env)

# version
__id__ = "$Id$"

# End of file 
