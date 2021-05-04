#!/usr/bin/env python3

import hashlib
import os
import sys


def listdir(dirpath):
    with os.scandir(dirpath) as it:
        for entry in sorted(it, key=lambda e: e.name):
            sb = entry.stat(follow_symlinks=False)
            line = ('path={} ino={} mode={:o} nlink={} uid={} gid={} '
                    'size={} atime={} mtime={} ctime={}'
                    .format(entry.path, sb.st_ino, sb.st_mode, sb.st_nlink,
                            sb.st_uid, sb.st_gid, sb.st_size, int(sb.st_atime),
                            int(sb.st_mtime), int(sb.st_ctime)))
            if entry.is_file(follow_symlinks=False):
                with open(entry.path, 'rb') as f:
                    line += ' md5=' + hashlib.md5(f.read()).hexdigest()
            if entry.is_symlink():
                line += ' target=' + os.readlink(entry.path)
            print(line)

            if entry.is_dir(follow_symlinks=False):
                listdir(entry.path)


if __name__ == "__main__":
    os.chdir(sys.argv[1])
    listdir('.')
