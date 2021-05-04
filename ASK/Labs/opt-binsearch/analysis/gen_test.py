#!/usr/bin/python3.8
import os
import csv
import asyncio
import argparse

orderIndex = "/2"

def ipcExtract(n, data):
    data = data.split("\n")
    return [
        n,                            # log2(row.len)
        2**n * 2**n / 1024,           # array size [KiB]
        int(data[3].split()[1]),      # searches   
        float(data[4].split()[2]),    # time
        int(data[5].split()[3]),      # total instructions
        float(data[6].split()[4]),    # instructions per cycle
    ]

def cacheExtract(n, data):
    cache0 = data.split("\n")[5].split()
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

async def ipcRun(ipcTemplate, n, times, version, path):
    makeDir(path)
    print("Performing IPC test")
    file0Path = path+"/ipcData-0.cvs"
    file1Path = path+"/ipcData-1.cvs"
    with open(file0Path, "a") as f0:
        with open(file1Path, "a") as f1:
            env0 = csv.writer(f0)
            env1 = csv.writer(f1)
            header = ["n", "size[KiB]", "searches", "time",
            "total instructions", "instructions per cycle"]
            env0.writerow(header)
            env1.writerow(header)
            
            for v in version:
                print("V:", v)
                for t in times:
                    print("T:", t)
                    for i in n:
                        print("N:",i)
                        cmd = ipcTemplate.format(i,t,v)
                        output, _ = await runTest(cmd)
                        data = ipcExtract(i, output.decode("utf-8"))
                        if v == 0:
                            env0.writerow(data)
                        elif v == 1:
                            env1.writerow(data)

async def cacheRun(cacheTemplate, n, levels, times, version, path):
    makeDir(path)

    file0Path = path+"/cacheData-0.cvs"
    file1Path = path+"/cacheData-1.cvs"
    print("Performing cache test")
    with open(file0Path, "a") as f0:
        with open(file1Path, "a") as f1:
            env0 = csv.writer(f0)
            env1 = csv.writer(f1)
            row = ['n', 'size[KiB]','searches']
            row.extend(levels)
            env0.writerow(row)
            env1.writerow(row)
            

            for v in version:
                for t in times:
                    print("T:",t)
                    for i in n:
                        print("N:",i)
                        data = [i,2**i * 2**i / 1024, t]
                        for level in levels:
                            cmd = cacheTemplate.format(i,level,t,v)
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
    n = [x for x in range(0, 26)]               # 31 is max
    cacheLevels = ['l1', 'l2', 'l3', 'tlb', 'branch']
    times = [10,15,25]


    ipcTemplate = "./binsearch -S 0x5bab3de5da7882ff -n {} -p ipc -t {} -v {}"
    runTemplate = "./binsearch -S 0x5bab3de5da7882ff -n {} -p {}  -t {} -v {}"

    # Perform total cycles and IPC test
    if t == 0:
        print('ipc test')
        await ipcRun(ipcTemplate, n, times, version, "./ipcTest")

    # Perform instructrion order and program efficiency test
    if t == 1:
        print('order test')
        global orderIndex
        order = "./orderTest"
        makeDir(order)
        await ipcRun(ipcTemplate, n, times, [1], order+orderIndex)

    # Perform branch missprediction test
    if t == 2:
        print('Cache test')
        await cacheRun(runTemplate, n, cacheLevels, times, version, "./cacheTest")


if __name__ == '__main__':
    asyncio.run(main())