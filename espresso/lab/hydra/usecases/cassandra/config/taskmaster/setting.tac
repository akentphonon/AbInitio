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

from twisted.application import service
from twisted.python.logfile import LogFile
from twisted.python.log import ILogObserver, FileLogObserver
from cassandra.applications.TaskMasterDaemon import TaskMasterDaemon

basedir     = r'/home/dexity/danse-workspace/AbInitio/espresso/lab/hydra/usecases/cassandra/config/taskmaster'
configfile  = r'taskmaster.cfg'

application = service.Application('taskmaster')
logfile     = LogFile.fromFullPath("twistd.log")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

TaskMasterDaemon(basedir, configfile).setServiceParent(application)


__date__ = "$Apr 6, 2010 10:57:59 AM$"


