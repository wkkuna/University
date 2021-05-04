#!/usr/bin/python3.8
import os
import csv
import asyncio
import argparse

orderIndex = "/7"

def ipcExtract(n, s, data):
    data = data.split("\n")
    return [
        n,                            # log2(row.len)
        data[1].split()[5],           # seed
        2**n * 2**n / 1024,           # array size [KiB]
        int(data[3].split()[1]),      # walks
        2**s,                         # steps      
        int(data[4].split()[3]),      # total instructions
        float(data[5].split()[4]),    # instructions per cycle
        float(data[6].split()[2]),    # time
        int(data[7].split()[4])       # accured elements (sum)
    ]

def cacheExtract(n, data):
    cache0 = data.split("\n")[4].split()
    return float(cache0[len(cache0)-1][:-1])
    
def moveAndBack(f):
    async def wrapper(*args, **kwargs):
        cwd = os.path.abspath(os.getcwd())
        os.chdir("../")
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

async def ipcRun(ipcTemplate, n, steps, version, path):
    makeDir(path)
    print("Performing IPC test")
    file0Path = path+"/ipcData-0.cvs"
    file1Path = path+"/ipcData-1.cvs"
    with open(file0Path, "a") as f0:
        with open(file1Path, "a") as f1:
            env0 = csv.writer(f0)
            env1 = csv.writer(f1)
            env0.writerow(["n", "seed", "size[KiB]", "walks", 
            "steps", "total instructions", "instructions per cycle",
                "time", "accrued elements(sum)"])
            env1.writerow(["n", "seed", "size[KiB]", "walks", 
            "steps", "total instructions", "instructions per cycle",
                "time", "accrued elements(sum)"])
            
            for v in version:
                print("V:", v)
                for s in steps:
                    print("S:",s)
                    for i in n:
                        print("N:",i)
                        cmd = ipcTemplate.format(i,s,v)
                        output, _ = await runTest(cmd)
                        data = ipcExtract(i, s, output.decode("utf-8"))
                        if v == 0:
                            env0.writerow(data)
                        elif v == 1:
                            env1.writerow(data)

async def cacheRun(cacheTemplate, n, Levels, steps, version, path):
    makeDir(path)

    file0Path = path+"/cacheData-0.cvs"
    file1Path = path+"/cacheData-1.cvs"
    print("Performing cache test")
    with open(file0Path, "a") as f0:
        with open(file1Path, "a") as f1:
            env0 = csv.writer(f0)
            env1 = csv.writer(f1)
            row = ['n', 'size[KiB]']
            row.append('steps')
            row.extend(Levels)
            env0.writerow(row)
            env1.writerow(row)
            

            for v in version:
                for i in n:
                    print("N:",i)
                    for s in steps:
                        print("S:",s)
                        data = [i,2**i * 2**i / 1024, s]
                        for level in Levels:
                            cmd = cacheTemplate.format(i,level, s,v)
                            output, _ = await runTest(cmd)
                            data0 = cacheExtract(i, output.decode("utf-8"))
                            data.append(data0)
                        if v == 0:
                            env0.writerow(data)
                        elif v == 1:
                            env1.writerow(data)


async def main():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--test', required=True)
        args = parser.parse_args()

    t = int(args.test)

    await cleanupMake()

    version = [x for x in range(0,2)]
    n = [x for x in range(0, 16)]           # 15 is max
    cacheLevels = ['l1', 'l2', 'l3', 'tlb']
    steps = [x for x in range(0,30)]        # 30 is max


    ipcTemplate = "./randwalk -S 0x593d3feeb3dc9b71 -n {} -p ipc -s {} -t 5 -v {}"
    runTemplate = "./randwalk -S 0x593d3feeb3dc9b71 -n {} -p {} -s {} -t 5 -v {}"

    # Perform Total Cycles and IPC data collection
    if t == 0:
        print('ipc test')
        await ipcRun(ipcTemplate, [10], steps, version, "./ipcTest")

    if t == 1:
        print('size test')
        await ipcRun(ipcTemplate, n, [15] , version, "./sizeTest")
        await cacheRun(runTemplate, n, cacheLevels, [15], version, "./sizeTest")
        await cacheRun(runTemplate, n, ['branch'], [15], version, "./sizeTest/branchTest")

    if t == 2:
        print('order test')
        global orderIndex
        order = "./orderTest"
        makeDir(order)
        await ipcRun(ipcTemplate, [10], steps, [1], order+orderIndex)

    if t == 3:
        print('branch missprediction test')
        await cacheRun(runTemplate, [10], ['branch'], steps, version, "./branchTest")


if __name__ == '__main__':
    asyncio.run(main())