#!/usr/bin/env python3

# You MUST NOT modify this file without author's consent.
# Doing so is considered cheating!

import os
import pexpect
import unittest
import random
import time
from tempfile import NamedTemporaryFile


class ShellTesterSimple():
    def setUp(self):
        self.child = pexpect.spawn('./shell')
        self.child.setecho(False)
        # self.child.interact()
        self.expect('#')

    def lines_before(self):
        return [line.strip()
                for line in self.child.before.decode('utf-8').split('\r\n')
                if len(line)]

    def lines_after(self):
        return [line.strip()
                for line in self.child.after.decode('utf-8').split('\r\n')
                if len(line)]

    def sendline(self, s):
        self.child.sendline(s)

    def sendintr(self):
        self.child.sendintr()

    def sendcontrol(self, ch):
        self.child.sendcontrol(ch)

    def expect(self, s):
        self.child.expect(s)

    def expect_exact(self, s):
        self.child.expect_exact(s)

    @property
    def pid(self):
        return self.child.pid

    def wait(self):
        self.child.wait()

    def execute(self, cmd):
        self.sendline(cmd)
        self.expect('#')
        return self.lines_before()


class ShellTester(ShellTesterSimple):
    def setUp(self):
        os.environ['LD_PRELOAD'] = './trace.so'
        self.child = pexpect.spawn('./shell')
        self.child.setecho(False)
        self.expect('#')

    def tearDown(self):
        del os.environ['LD_PRELOAD']

    def expect_syscall(self, name, caller=None):
        self.expect('\[(\d+):(\d+)\] %s\(([^)]*)\)([^\r]*)\r\n' % name)

        pid, pgrp, args, retval = self.child.match.groups()
        pid = int(pid)
        pgrp = int(pgrp)
        args = args.decode('utf-8')
        retval = retval.decode('utf-8')
        result = {'pid': pid, 'pgrp': pgrp, 'args': []}

        if args not in ['...', '']:
            for arg in args.split(', '):
                try:
                    result['args'].append(int(arg))
                except ValueError:
                    result['args'].append(arg)

        if caller is not None:
            self.assertEqual(caller, pid)
        if not retval:
            return result
        if retval.startswith(' = '):
            result['retval'] = int(retval[3:])
            return result
        if retval.startswith(' -> '):
            items = retval[5:-1].strip()
            if not items:
                return result
            for item in items.split(', '):
                k, v = item.split('=', 1)
                try:
                    result[k] = int(v)
                except ValueError:
                    result[k] = v
            return result
        raise RuntimeError

    def expect_fork(self, parent=None):
        return self.expect_syscall('fork', caller=parent)

    def expect_execve(self, child=None):
        return self.expect_syscall('execve', caller=child)

    def expect_waitpid(self, pid=None, status=None):
        while True:
            res = self.expect_syscall('waitpid')
            if res['pid'] == pid and res.get('status', None) == status:
                break
        self.assertEqual(status, res.get('status', -1))

    def expect_spawn(self):
        result = self.expect_fork(parent=self.pid)
        self.expect_execve(child=result['retval'])
        return result


class TestShellSimple(ShellTesterSimple, unittest.TestCase):
    def test_redir_1(self):
        nlines = 587
        inf_name = 'include/queue.h'

        # 'wc -l include/queue.h > out'
        with NamedTemporaryFile(mode='r') as outf:
            self.execute('wc -l ' + inf_name + ' >' + outf.name)
            self.assertEqual(int(outf.read().split()[0]), nlines)

        # 'wc -l < include/queue.h'
        lines = self.execute('wc -l < ' + inf_name)
        self.assertEqual(lines[0], str(nlines))

        # 'wc -l < include/queue.h > out'
        with NamedTemporaryFile(mode='r') as outf:
            self.execute('wc -l < ' + inf_name + ' >' + outf.name)
            self.assertEqual(int(outf.read().split()[0]), nlines)

    def test_redir_2(self):
        with NamedTemporaryFile(mode='w') as inf:
            with NamedTemporaryFile(mode='r') as outf:
                n = random.randrange(100, 200)

                for i in range(n):
                    inf.write('a\n')
                inf.flush()

                # 'wc -l < random-text > out'
                self.execute('wc -l ' + inf.name + ' >' + outf.name)
                self.assertEqual(outf.read().split()[0], str(n))

    def test_pipeline_1(self):
        lines = self.execute('grep LIST include/queue.h | wc -l')
        self.assertEqual(lines[0], '46')

    def test_pipeline_2(self):
        lines = self.execute(
                'cat include/queue.h | cat | grep LIST | cat | wc -l')
        self.assertEqual(lines[0], '46')

    def test_pipeline_3(self):
        with NamedTemporaryFile(mode='r') as outf:
            self.execute(
                    'cat < include/queue.h | grep LIST | wc -l > ' + outf.name)
            self.assertEqual(int(outf.read().split()[0]), 46)

    def test_fd_leaks(self):
        # 'ls -l /proc/self/fd'
        lines = self.execute('ls -l /proc/self/fd')
        self.assertEqual(len(lines), 5)
        for i in range(3):
            self.assertIn('%d -> /dev/pts/' % i, lines[i + 1])
        self.assertIn('3 -> /proc/', lines[4])

        # 'ls -l /proc/self/fd | cat'
        lines = self.execute('ls -l /proc/self/fd | cat')
        self.assertEqual(len(lines), 5)
        self.assertIn('pipe:', lines[2])

        # 'echo test | ls -l /proc/self/fd'
        lines = self.execute('echo test | ls -l /proc/self/fd')
        self.assertEqual(len(lines), 5)
        self.assertIn('pipe:', lines[1])

        # 'echo test | ls -l /proc/self/fd | cat'
        lines = self.execute('echo test | ls -l /proc/self/fd | cat')
        self.assertEqual(len(lines), 5)
        self.assertIn('pipe:', lines[1])
        self.assertIn('pipe:', lines[2])

        # check shell 'ls -l /proc/$pid/fd'
        lines = self.execute('ls -l /proc/%d/fd' % self.pid)
        self.assertEqual(len(lines), 5)
        for i in range(4):
            self.assertIn('%d -> /dev/pts/' % i, lines[i + 1])

    def test_exitcode_1(self):
        # 'true &'
        self.sendline('true &')
        self.expect_exact("running 'true'")
        self.sendline('jobs')
        self.expect_exact("exited 'true', status=0")

        # 'false &'
        self.sendline('false &')
        self.expect_exact("running 'false'")
        self.sendline('jobs')
        self.expect_exact("exited 'false', status=1")

        if False:
            # 'exit 42 &'
            self.sendline('exit 42 &')
            self.expect_exact("running 'exit 42'")
            self.sendline('jobs')
            self.expect_exact("exited 'exit 42', status=42")

    def test_kill_suspended(self):
        self.sendline('cat &')
        self.expect_exact("running 'cat'")
        self.sendline('jobs')
        self.expect_exact("suspended 'cat'")
        self.sendline('pkill -9 cat')
        self.expect_exact("killed 'cat' by signal 9")

    def test_resume_suspended(self):
        self.sendline('cat &')
        self.expect_exact("running 'cat'")
        self.sendline('jobs')
        self.expect_exact("suspended 'cat'")
        self.sendline('fg')
        self.expect_exact("continue 'cat'")
        self.sendintr()
        self.sendline('jobs')
        # expect something ?

    def test_kill_jobs(self):
        self.sendline('sleep 1000 &')
        self.expect_exact("[1] running 'sleep 1000'")
        self.sendline('sleep 2000 &')
        self.expect_exact("[2] running 'sleep 2000'")
        self.sendline('jobs')
        self.expect_exact("[1] running 'sleep 1000'")
        self.expect_exact("[2] running 'sleep 2000'")
        self.sendline('kill %2')
        self.sendline('jobs')
        self.expect_exact("[1] running 'sleep 1000'")
        self.expect_exact("[2] killed 'sleep 2000' by signal 15")
        self.sendline('kill %1')
        self.sendline('jobs')
        self.expect_exact("[1] killed 'sleep 1000' by signal 15")

    def test_kill_at_quit(self):
        self.sendline('sleep 1000 &')
        self.expect_exact("[1] running 'sleep 1000'")
        self.sendline('sleep 2000 &')
        self.expect_exact("[2] running 'sleep 2000'")
        self.sendline('jobs')
        self.expect_exact("[1] running 'sleep 1000'")
        self.expect_exact("[2] running 'sleep 2000'")
        self.sendcontrol('d')
        self.expect_exact("[1] killed 'sleep 1000' by signal 15")
        self.expect_exact("[2] killed 'sleep 2000' by signal 15")


class TestShellWithSyscalls(ShellTester, unittest.TestCase):
    def stty(self):
        with NamedTemporaryFile(mode='r') as sttyf:
            self.execute('stty -a')
            return sttyf.read()

    def test_quit(self):
        self.sendline('quit')
        self.wait()

    def test_sigint(self):
        self.sendline('sleep 10')
        child = self.expect_spawn()['retval']
        self.sendintr()
        self.expect_waitpid(pid=child, status='SIGINT')
        self.expect('#')

    def test_sigtstp(self):
        self.sendline('cat')
        child = self.expect_spawn()['retval']
        self.sendcontrol('z')
        self.expect_waitpid(pid=child, status='SIGTSTP')
        self.sendline('fg 1')
        self.expect_waitpid(pid=child, status='SIGCONT')
        self.sendcontrol('d')
        self.expect('#')

    def test_terminate_tstped(self):
        self.sendline('cat')
        child = self.expect_spawn()['retval']
        self.sendcontrol('z')
        self.expect_waitpid(pid=child, status='SIGTSTP')
        self.sendline('kill %1')
        time.sleep(0.1)
        self.expect_waitpid(pid=child, status='SIGCONT')
        self.expect_waitpid(pid=child, status='SIGTERM')
        self.sendline('jobs')
        self.expect_exact("[1] killed 'cat' by signal 15")

    def test_terminate_ttined(self):
        self.sendline('cat &')
        child = self.expect_spawn()['retval']
        self.expect_waitpid(pid=child, status='SIGTTIN')
        self.sendline('kill %1')
        time.sleep(0.1)
        self.expect_waitpid(pid=child, status='SIGCONT')
        self.expect_waitpid(pid=child, status='SIGTERM')
        self.sendline('jobs')
        self.expect_exact("[1] killed 'cat' by signal 15")

    def test_termattr_1(self):
        stty_before = self.stty()
        self.sendline('less shell.c')
        child = self.expect_spawn()['retval']
        self.sendline('q')
        self.expect_waitpid(pid=child, status=0)
        self.expect('#')
        stty_after = self.stty()
        self.assertEqual(stty_before, stty_after)

    def test_termattr_2(self):
        stty_before = self.stty()
        self.sendline('less shell.c')
        child = self.expect_spawn()['retval']
        time.sleep(0.25)
        self.sendcontrol('z')
        self.expect_waitpid(pid=child, status='SIGTSTP')
        self.sendline('kill %1')
        self.expect_waitpid(pid=child, status='SIGTERM')
        self.sendline('jobs')
        self.expect_exact("[1] killed 'less shell.c' by signal 15")
        stty_after = self.stty()
        self.assertEqual(stty_before, stty_after)


if __name__ == '__main__':
    os.environ['PATH'] = '/usr/bin:/bin'
    os.environ['LC_ALL'] = 'C'

    unittest.main()
