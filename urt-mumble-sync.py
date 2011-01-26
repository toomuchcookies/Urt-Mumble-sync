import re
import time

from pyquake3 import PyQuake3
from icetest import IcedMurmur

urtserver = 'localhost:27960'

murmur = IcedMurmur()
s = murmur.getServer(64738)

q = PyQuake3(urtserver, rcon_password='setapassword')
q.update()
print 'The name of %s is %s, running map %s with %s player(s).' % (q.get_address(), q.vars['sv_hostname'], q.vars['mapname'], len(q.players))

q.rcon_update()

playerregexp = re.compile('^([0-9]*): (.*) (BLUE|RED) k:([0-9]+) d:([0-9]+) ping:[0-9]+ .*$')

while True:
    #q.update()
    #print 'The name of %s is %s, running map %s with %s player(s).' % (q.get_address(), q.vars['sv_hostname'], q.vars['mapname'], len(q.players))
    players = q.rcon('players')
    pp = {}
    for i in players[1].split('\n'):
        player = playerregexp.match(i)
        if player:
            pp[player.group(2)] = player.group(3)

    users = s.getUsers()
    for i in users:
        if users[i].name in pp:
            if pp[users[i].name] == 'RED' and users[i].channel != 1:
                users[i].channel = 1
                s.setState(users[i])
                print users[i].name, "switched to RED"
            elif pp[users[i].name] == 'BLUE' and users[i].channel != 2:
                users[i].channel = 2
                s.setState(users[i])
                print users[i].name, "switched to BLUE"
    time.sleep(1)
    
