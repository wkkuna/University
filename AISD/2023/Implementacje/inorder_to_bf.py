from math import floor, log2
from queue import Queue


def part(lst):
    complete_levels = floor(log2(len(lst) + 1)) - 1
    nodes_complete = 2 ** (complete_levels + 1) - 1
    remaining_nodes = len(lst) - nodes_complete
    root_position = min(remaining_nodes, 2 **
                        (complete_levels + 1) // 2) + nodes_complete // 2
    return lst[root_position], lst[:root_position], lst[root_position+1:]


def complete_binary_tree(lst):
    q = Queue()
    out = []

    q.put(lst)
    while not q.empty():
        e = q.get()
        rt, l, r = part(e)
        out.append(rt)
        if len(l):
            q.put(l)
        if len(r):
            q.put(r)
    return out
