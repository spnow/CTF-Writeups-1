import angr
import logging


logging.getLogger('angr.path_group').setLevel(logging.DEBUG)

def get_byte(s, i):
    pos = s.size() / 8 - 1 - i
    return s[pos * 8 + 7 : pos * 8]

exe = 'a.out'
start_ = 0x4005da # before call
good = 0x4005e8 # skipped over
bad = 0x4005f4 # call print flag
mem = 0x00602048

flag_len = 8

p = angr.Project(exe,load_options={"auto_load_libs":False})

#state = p.factory.blank_state(addr=start_)
# state.regs.rdi = mem
# s = state
# argv=[exe, state.se.BVS('arg1', flag_len*8)]

# s.mem[mem:] = argv[1]

# for i in xrange(flag_len):
    # # We want those flags to be printable characters
    # byte = get_byte(argv[1], i)
    # state.add_constraints(byte >= 0x20)
    # state.add_constraints(byte <= 0x7e)

# path = p.factory.path(state=state)

# ex = p.surveyors.Explorer(find=(good, ), enable_veritesting=True)
# ex.run()
# print "done"
# print ex.found
# possible_flags = ex.found[0].state.se.any_n_int(argv[1],10)

# for f in possible_flags:
	# print hex(f)
proj = angr.Project("a.out", load_options={"auto_load_libs":False})
path_group = proj.factory.path_group(threads=4)
path_group.explore(find=good, avoid=bad)
print path_group.found
print path_group.found[0].state.posix.dumps(1)

