import Ice

"""
Ice.loadSlice("Murmur.ice")
comm = Ice.initialize()
proxy = "Meta:tcp -h 127.0.0.1 -p 6502"
prx = comm.stringToProxy(proxy)
"""

class IcedMurmur(object):
    """
    Provides several small wrapper functions to ease the use
    of the ice interface
    """
    def __init__(self,slice = "Murmur.ice",proxy = "Meta:tcp -h 127.0.0.1 -p 6502"):
        Ice.loadSlice(slice)
        import Murmur
        ice = Ice.initialize()
        prx = ice.stringToProxy(proxy)
        self.murmur = Murmur.MetaPrx.checkedCast(prx)
        self.Murmur = Murmur
    
    def registerPlayer(self, server, name, password, email =""):
        pid = server.registerPlayer(name)
        player = server.getRegistration(pid)
        self.updatePlayer(server, player, name, password, email)
        return pid
    
    def updatePlayer(self, server, player,
                   name = None,
                   password = None,
                   email = None):
        if name: player.name = name
        if password: player.pw = password
        if email: player.email = email
        server.updateregistration(player)
        return player
    
    def createServer(self, port = None):
        server = self.murmur.newServer()
        if port:
            server.setConf('port', str(port))
        return server
    
    def getServer(self, port):
        baseport = int(self.murmur.getDefaultConf()['port'])
        for server in self.murmur.getAllServers():
            cport = server.getConf('port')
            if cport: cport = int(cport)
            else:
               cport = baseport + server.id() - 1
            if port == cport:
                return server
        return None
    
    def getPlayer(self, server, name):
        players = server.getRegisteredPlayers(name)
        for player in players:
            if player.name == name:
                return player
        return None

if __name__ == '__main__':
    murmur = IcedMurmur()
    s = murmur.getServer(64738)
    #print murmur.murmur.getDefaultConf()
    #for i in dir(s):
    #    print i
    #print s.getUsers()[2].channel
    users = s.getUsers()
    #print type(users)

    #print users

    for i in users:
        print users[i].address
        print users[i].channel
        users[i].channel = 2
        print users[i].userid
        s.setState(users[i])
    """
    for i in s.getUsers():
        print k.channel
    """
