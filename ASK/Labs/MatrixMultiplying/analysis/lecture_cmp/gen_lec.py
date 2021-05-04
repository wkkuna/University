#!/usr/bin/python3.8
import sys
import os
import subprocess
import csv
import asyncio


def extract(data,n):
    new = data.split("\n")[2:-1]
    return [
        n,
        float(new[0].split()[2]),
        int(new[1].split()[3]),
        float(new[2].split()[4]),
    ]


async def main():

    cwd = os.path.abspath(os.getcwd())
    os.chdir("../../")
    proc = await asyncio.create_subprocess_shell("make clean", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    proc = await asyncio.create_subprocess_shell("make", stdout=asyncio.subprocess.PIPE,  stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    os.chdir(cwd)

    i = [x for x in range(0, 4)]  # functions 0, 1, 2, 3

    j = [x for x in range(32,736,32)]  # test range & accuracy

    pathTest = "./test"
    if not os.path.isdir(pathTest):
        os.mkdir(pathTest)

    cmdTemplate = "./matmult -n {} -p ipc -v {}"

    for iIter in i:

        pathIIter = pathTest + f"/type{iIter}"
        if not os.path.isdir(pathIIter):
            os.mkdir(pathIIter)

        with open(pathIIter+f"/data-{iIter}.cvs", "w") as f:
            env = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            env.writerow(["n","TIME","INS","INS_PER_CYC"])

            for jIter in j:
                cmd = cmdTemplate.format(jIter,iIter)
                os.chdir("../../")
                process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                os.chdir(cwd)
                output, error = await process.communicate()
                toSave = extract(output.decode("utf-8"),jIter)
                env.writerow(toSave)

asyncio.run(main())
