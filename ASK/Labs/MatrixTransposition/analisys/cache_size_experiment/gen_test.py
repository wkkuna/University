#!/usr/bin/python3.8
import os
import csv
import asyncio

def ipcExtract(n, data):
    ipcData = data.split("\n")[2:-1]
    return [
        n,
        float(ipcData[0].split()[2]),
        int(ipcData[1].split()[3]),
        float(ipcData[2].split()[4]),
    ]

def moveAndBack(f):
    async def wrapper(*args, **kwargs):
        cwd = os.path.abspath(os.getcwd())
        os.chdir("../../")
        out = await f(*args, **kwargs)
        os.chdir(cwd)
        return out
    return wrapper

@moveAndBack
async def cleanupMake():
    await(await asyncio.create_subprocess_shell("make clean",
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)).communicate()
    await(await asyncio.create_subprocess_shell("make",
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)).communicate()


@moveAndBack
async def runTest(cmd):
    return await (await asyncio.create_subprocess_shell(cmd,
                                                        stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)).communicate()


def makeDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


async def main():
    await cleanupMake()
    funTypes = [x for x in range(0, 2)]

    matrixSize = [x for x in range(8, 2048, 8)]

    cacheLevels = ["l1", "l2", "l3", "tlb"]

    ipcTemplate = "./transpose -n {} -p ipc -v {}"

    ipcPath = "./ipcTest"
    makeDir(ipcPath)

    ipcPathTemplate = "./ipcTest/"

# Perform Total Cycles and IPC data collection
    for funType in funTypes:

        funTypePath = ipcPathTemplate
        makeDir(funTypePath)

        fileFunPath = funTypePath+f"/ipcData-{funType}.cvs"
        with open(fileFunPath, "a") as f:

            env = csv.writer(f)
            env.writerow(["n", "TIME", "INS", "INS_PER_CYC"])

            for n in matrixSize:
                cmd = ipcTemplate.format(n, funType)
                output, _ = await runTest(cmd)
                toSave = ipcExtract(n, output.decode("utf-8"))
                env.writerow(toSave)

asyncio.run(main())
