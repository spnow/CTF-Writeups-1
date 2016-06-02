import angr
import logging



def main():
    logging.getLogger('angr.path_group').setLevel(logging.DEBUG)
    project = angr.Project("./fairlight")

    argv1 = angr.claripy.BVS("argv1",14*8)
    initial_state = project.factory.path(args=["./fairlight",argv1])


    pg = project.factory.path_group(initial_state)

    pg.explore(find=0x401a41, avoid=0x40074d)
    print pg.found
    found = pg.found[0]

    solution = found.state.se.any_str(argv1)

    print repr(solution)
    solution = solution[:solution.find("\x00")]
    print solution
    return solution

main()
