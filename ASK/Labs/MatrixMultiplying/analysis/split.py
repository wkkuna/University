#!/bin/python3

import sys
import os


def main():
    filename = str(sys.argv[1])
    path = str(sys.argv[2])

    path += "/"
    if not os.path.isdir("./" + path):
        os.mkdir(path)

    fn = [
        path + "L1.txt",
        path + "L2.txt",
        path + "L3.txt",
        path + "TLB.txt",
    ]

    ff = []

    for x in fn:
        ff.append(open(x, "w"))

    with open(filename, "r") as root_file:
        i = 0
        for l in root_file.readlines():
            ff[i % len(fn)].writelines(l)
            i += 1

    for x in ff:
        x.close()


main()
