
from a2s.players import players

"""
https://developer.valvesoftware.com/wiki/Server_queries#A2S_RULES

https://github.com/Yepoleb/python-a2s
"""

TIMEOUT = 5

addr = ('37.230.137.20',26900) # relax-pve
addr = ('83.220.174.163',26900) # russian-zombieland
addr = ('109.230.239.71',26900) # dirty loot
data = players(addr,timeout=10)
for p in data:
    print(p.name) # empty :(
