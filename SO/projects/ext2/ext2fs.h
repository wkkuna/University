#pragma once

#include <stdint.h>
#include <stddef.h>
#include <unistd.h>
#include <sys/cdefs.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/queue.h>

#include "ext2fs_defs.h"

#ifndef min
#define min(a, b)                                                              \
  ({                                                                           \
    __typeof__(a) _a = (a);                                                    \
    __typeof__(b) _b = (b);                                                    \
    _a < _b ? _a : _b;                                                         \
  })
#endif

#ifndef howmany
#define howmany(x, y) (((x) + (y)-1) / (y))
#endif

#ifndef __unused
#define __unused __attribute__((unused))
#endif

#define BLKSIZE 1024UL /* size of data stored in the buffer */

/*
 * Extended filesystem 2 types and functions.
 */

/* Low-level functions. */
int ext2_block_used(uint32_t blkaddr);
int ext2_inode_used(uint32_t ino);
long ext2_blkaddr_read(uint32_t ino, uint32_t blkidx);

/* High-level functions. */
int ext2_read(uint32_t ino, void *data, size_t pos, size_t len);
int ext2_readdir(uint32_t ino, uint32_t *offp, ext2_dirent_t *de);
int ext2_readlink(uint32_t ino, char *buf, size_t buflen);
int ext2_stat(uint32_t ino, struct stat *st);
int ext2_lookup(uint32_t ino, const char *name, uint32_t *ino_p,
                uint8_t *type_p);
int ext2_mount(const char *imgpath);
