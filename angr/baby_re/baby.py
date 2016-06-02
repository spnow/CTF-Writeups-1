
import claripy
import logging
import angr

FIND_ADDR  = 0x040294b
AVOID_ADDR = (0x0402941) 



logging.getLogger('angr.path_group').setLevel(logging.DEBUG)
p = angr.Project("baby-re",load_options={"auto_load_libs":False})

pg = p.factory.path_group(threads=4)
pg.explore(find=FIND_ADDR,avoid=AVOID_ADDR)

print pg.found[0].state.posix.dumps(1)
