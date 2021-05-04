#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <readline/readline.h>
#include <readline/history.h>

#include "ext2fs.h"

/* clang-format off */
static const char *ext2_ft_name[] = {
  [EXT2_FT_UNKNOWN] = "???",
  [EXT2_FT_REG] = "reg",
  [EXT2_FT_DIR] = "dir",
  [EXT2_FT_CHRDEV] = "cdev",
  [EXT2_FT_BLKDEV] = "bdev",
  [EXT2_FT_FIFO] = "fifo",
  [EXT2_FT_SOCK] = "sock",
  [EXT2_FT_SYMLINK] = "slnk",
};
/* clang-format on */

typedef int (*func_t)(char *arg);

typedef struct {
  const char *name;
  func_t func;
} command_t;

static uint32_t curdir = EXT2_ROOTINO;

static int do_chdir(char *arg) {
  uint32_t ino;
  uint8_t type;
  int error;

  if ((error = ext2_lookup(curdir, arg, &ino, &type)))
    return error;

  if (type != EXT2_FT_DIR)
    return ENOTDIR;

  curdir = ino;
  return 0;
}

static int do_list(char *arg) {
  uint32_t ino = curdir;
  int error;

  if (arg != NULL) {
    uint8_t type;

    if ((error = ext2_lookup(curdir, arg, &ino, &type)))
      return error;

    if (type != EXT2_FT_DIR)
      return ENOTDIR;
  }

  ext2_dirent_t de;
  uint32_t off = 0;
  while (ext2_readdir(ino, &off, &de)) {
    printf("%8d  %4s  '%.*s'\n", de.de_ino, ext2_ft_name[de.de_type],
           de.de_namelen, de.de_name);
  }

  return 0;
}

static void hexdump(uint8_t *data, size_t offset, size_t size) {
  bool was_empty = false;
  bool is_empty;

  size = min(size, BLKSIZE);

  for (unsigned i = 0; i < size; i += 16, was_empty = is_empty) {
    is_empty = true;

    for (unsigned j = i; j < min(size, i + 16); j++) {
      if (data[j]) {
        is_empty = false;
        break;
      }
    }

    if (is_empty) {
      if (!was_empty)
        puts("*");
      continue;
    }

    printf("%08lx:", i + offset);
    for (unsigned j = i; j < i + 16; j++) {
      if (j % 8 == 0)
        putchar(' ');
      if (j < size)
        printf(" %02x", data[j]);
      else
        printf("   ");
    }
    printf(" |");
    for (unsigned j = i; j < min(size, i + 16); j++) {
      uint8_t c = data[j];
      putchar(isprint(c) ? c : '.');
    }
    printf("|\n");
  }
}

static int do_read(char *arg) {
  uint32_t ino;
  int error;

  if ((error = ext2_lookup(curdir, arg, &ino, NULL)))
    return error;

  struct stat st;
  ext2_stat(ino, &st);

  if (!(st.st_mode & S_IFREG))
    return EINVAL;

  uint8_t data[BLKSIZE];
  size_t pos = 0;
  size_t len = st.st_size;
  while (len > 0) {
    size_t cnt = min(len, BLKSIZE);
    if ((error = ext2_read(ino, data, pos, cnt)))
      return error;
    hexdump(data, pos, cnt);
    len -= cnt;
    pos += cnt;
  }

  return 0;
}

static int do_stat(char *arg) {
  uint32_t ino;
  int error;

  if ((error = ext2_lookup(curdir, arg, &ino, NULL)))
    return error;

  struct stat st;
  ext2_stat(ino, &st);

  mode_t mode = st.st_mode;
  const char *type = "???";

  if (S_ISDIR(mode))
    type = "directory";
  else if (S_ISCHR(mode))
    type = "character device";
  else if (S_ISBLK(mode))
    type = "block device";
  else if (S_ISREG(mode))
    type = "regular file";
  else if (S_ISLNK(mode))
    type = "symbolic link";

  char modestr[10] = "rwxrwxrwx\0";
  char mtim[26]; /* 26 as in manual page */
  char atim[26];
  char ctim[26];

  for (int i = 0; i < 9; i++)
    if (!(st.st_mode & (1 << (8 - i))))
      modestr[i] = '-';

  ctime_r(&st.st_ctime, (char *)&ctim);
  ctime_r(&st.st_atime, (char *)&atim);
  ctime_r(&st.st_mtime, (char *)&mtim);

  printf("i-node : %ld\n"
         "type   : %s\n"
         "mode   : %s\n"
         "user   : %d\n"
         "group  : %d\n"
         "size   : %ld\n"
         "blocks : %ld\n"
         "links  : %ld\n"
         "ctime  : %s"
         "atime  : %s"
         "mtime  : %s",
         st.st_ino, type, modestr, st.st_uid, st.st_gid, st.st_size,
         st.st_blocks, st.st_nlink, ctim, atim, mtim);
  return 0;
}

static int do_readlink(char *arg) {
  uint32_t ino;
  int error;

  if ((error = ext2_lookup(curdir, arg, &ino, NULL)))
    return error;

  struct stat st;
  ext2_stat(ino, &st);

  char symlink[st.st_size + 1];
  if ((error = ext2_readlink(ino, symlink, st.st_size)))
    return error;

  symlink[st.st_size] = '\0';
  printf("%s -> %s\n", arg, symlink);
  return 0;
}

/* Print all number of data blocks for given i-node. */
static int do_blocks(char *arg) {
  uint32_t ino;
  uint8_t type;
  int error;

  if ((error = ext2_lookup(curdir, arg, &ino, &type)))
    return error;

  if (type != EXT2_FT_DIR && type != EXT2_FT_REG)
    return ENOTSUP;

  struct stat st;
  ext2_stat(ino, &st);

  uint32_t blkidx = 0;
  while ((blkidx * BLKSIZE < (uint32_t)st.st_size))
    printf("%ld ", ext2_blkaddr_read(ino, blkidx++));
  puts("");

  return 0;
}

/* Test if i-node is in use. */
static int do_testi(char *arg) {
  if (!arg)
    return EINVAL;
  uint32_t ino = strtol(arg, NULL, 10);
  int res = ext2_inode_used(ino);
  if (res == EINVAL)
    return res;
  printf("i-node %d is %s\n", ino, res ? "used" : "free");
  return 0;
}

/* Test if block is in use. */
static int do_testb(char *arg) {
  if (!arg)
    return EINVAL;
  uint32_t blk = strtol(arg, NULL, 10);
  int res = ext2_block_used(blk);
  if (res == EINVAL)
    return res;
  printf("block %d is %s\n", blk, res ? "used" : "free");
  return 0;
}

/* clang-format off */
static command_t commands[] = {
  {"cd", do_chdir},
  {"ls", do_list},
  {"stat", do_stat},
  {"read", do_read},
  {"readlink", do_readlink},
  {"blocks", do_blocks},
  {"testi", do_testi}, 
  {"testb", do_testb}, 
  {NULL, NULL},
};
/* clang-format on */

static int doit(char *line) {
  char *name = strsep(&line, " ");

  if (line && !strlen(line))
    line = NULL;

  for (command_t *cmd = commands; cmd->name; cmd++) {
    if (strcmp(name, cmd->name))
      continue;
    return cmd->func(line);
  }

  return ENOTSUP;
}

int main(void) {
  int error;

  if ((error = ext2_mount("debian9-ext2.img")))
    return error;

  while (true) {
    char *line = readline("# ");

    if (line == NULL)
      break;

    if (strlen(line)) {
      add_history(line);
      if ((error = doit(line)))
        fprintf(stderr, "ERROR: %s!\n", strerror(error));
    }
    free(line);
  }

  return 0;
}
