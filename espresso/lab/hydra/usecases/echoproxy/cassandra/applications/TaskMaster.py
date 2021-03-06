
JOB_MESSAGE = " -> JobTracker"

from twisted.python import log
from twisted.application.internet import TCPClient, TCPServer
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory, ServerFactory

from cassandra.applications.Daemon import Daemon

class JobClient(LineReceiver):
    "Client"
    def connectionMade(self):
        log.msg("JobClient: got new client!")
        self.factory.client   = self    # Save the client


    def lineReceived(self, line):
        log.msg("JobClient: received", repr(line))
        proxy   = self.factory.proxy
        proxy.sendLine(line + JOB_MESSAGE)


class JobTracker(LineReceiver):
    "Server"
    def connectionMade(self):
        log.msg("JobTracker: got new client!")
        self.clientFactory          = self.factory.master.clientFactory()
        self.clientFactory.proxy    = self
#        self.clientFactory.client   = None  # client later become JobClient


    def connectionLost(self, reason):
        log.msg("JobTracker: lost a client!")
        self.factory.client = None


    def lineReceived(self, line):
        log.msg("JobTracker: received", repr(line))
        client      = self.clientFactory.client # JobClient
        client.sendLine(line + JOB_MESSAGE)


class TaskMaster(Daemon):
    
    def __init__(self, basedir, configFileName = "taskmaster.cfg"):
        Daemon.__init__(self, basedir, configFileName)
        self._clientFactory             = ClientFactory()  # Rename? # Later use: pb.PBServerFactory(p)
        self._clientFactory.protocol    = JobClient
        self._serverFactory             = ServerFactory()
        self._serverFactory.protocol    = JobTracker
        self._serverFactory.master      = self

        log.msg("creating TaskMaster")


    def startService(self):
        "Starts service"
        Daemon.startService(self)

        self._setParams()
        self._listen()
        self._connect()


    def clientFactory(self):
        return self._clientFactory


    def serverFactory(self):
        return self._serverFactory


    def _setParams(self):
        self._setConfig()
        if not self._config:
            return

        self._masterPort    = self._config["masterPort"]
        self._workerPort    = self._config["workerPort"]
        self._workerHost    = self._config["workerHost"]
        log.msg("settings parameters from %s config" % self._configFileName)


    def _listen(self):
        "Set service to listen on tcp port"
        masterService = TCPServer(self._masterPort, self._serverFactory)
        masterService.setServiceParent(self)
        log.msg("TaskMaster is listening on port: %d" % self._masterPort)

        
    def _connect(self):
        "Connect to the worker"
        masterClient = TCPClient(self._workerHost, self._workerPort, self._clientFactory)
        masterClient.setServiceParent(self)
        log.msg("TaskMaster connects to Worker")
