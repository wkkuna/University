#define FUSE_USE_VERSION 30

#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <fuse_lowlevel.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "ext2fs.h"

typedef struct fuse_file_info fuse_file_info_t;

static void e2fs_getattr(fuse_req_t req, fuse_ino_t ino,
                         fuse_file_info_t *fi __unused) {
  struct stat st;
  int error;

  if (ino == 1)
    ino = EXT2_ROOTINO;

  memset(&st, 0, sizeof(st));
  if ((error = ext2_stat(ino, &st))) {
    fuse_reply_err(req, error);
    return;
  }

  fuse_reply_attr(req, &st, 1.0);
}

static void e2fs_lookup(fuse_req_t req, fuse_ino_t parent, const char *name) {
  uint32_t ino;
  int error;

  if (parent == 1)
    parent = EXT2_ROOTINO;

  if ((error = ext2_lookup(parent, name, &ino, NULL))) {
    fuse_reply_err(req, error);
    return;
  }

  struct fuse_entry_param e;
  memset(&e, 0, sizeof(e));
  e.ino = ino;
  e.attr_timeout = 1.0;
  e.entry_timeout = 1.0;

  if ((error = ext2_stat(e.ino, &e.attr))) {
    fuse_reply_err(req, error);
    return;
  }

  fuse_reply_entry(req, &e);
}

static void e2fs_readdir(fuse_req_t req, fuse_ino_t ino, size_t size,
                         off_t _off, fuse_file_info_t *fi __unused) {
  int error;

  if (ino == 1)
    ino = EXT2_ROOTINO;

  ext2_dirent_t de;
  uint32_t off = _off;
  if (!ext2_readdir(ino, &off, &de)) {
    fuse_reply_buf(req, NULL, 0);
    return;
  }

  void *buf = malloc(size);
  assert(buf != NULL);
  struct stat st;
  if ((error = ext2_stat(de.de_ino, &st))) {
    fuse_reply_err(req, error);
    return;
  }
  size = fuse_add_direntry(req, buf, size, de.de_name, &st, off);
  error = fuse_reply_buf(req, buf, size);
  assert(error == 0);
  free(buf);
}

static void e2fs_readlink(fuse_req_t req, fuse_ino_t ino) {
  int error;

  if (ino == 1)
    ino = EXT2_ROOTINO;

  struct stat st;
  if ((error = ext2_stat(ino, &st))) {
    fuse_reply_err(req, error);
    return;
  }

  char symlink[st.st_size + 1];
  if ((error = ext2_readlink(ino, symlink, st.st_size))) {
    fuse_reply_err(req, error);
    return;
  }

  symlink[st.st_size] = '\0';
  fuse_reply_readlink(req, symlink);
}

static void e2fs_open(fuse_req_t req, fuse_ino_t ino, fuse_file_info_t *fi) {
  int error;

  if (ino == 1)
    ino = EXT2_ROOTINO;

  struct stat st;
  if ((error = ext2_stat(ino, &st))) {
    fuse_reply_err(req, error);
    return;
  }

  if (S_ISDIR(st.st_mode)) {
    fuse_reply_err(req, EISDIR);
    return;
  }

  if ((fi->flags & 3) != O_RDONLY) {
    fuse_reply_err(req, EACCES);
    return;
  }

  fuse_reply_open(req, fi);
}

static void e2fs_read(fuse_req_t req, fuse_ino_t ino, size_t size, off_t off,
                      fuse_file_info_t *fi __unused) {
  int error;

  if (ino == 1)
    ino = EXT2_ROOTINO;

  struct stat st;
  if ((error = ext2_stat(ino, &st))) {
    fuse_reply_err(req, error);
    return;
  }

  if (!S_ISREG(st.st_mode) || (off > st.st_size)) {
    fuse_reply_err(req, EINVAL);
    return;
  }

  size = min(size, (size_t)(st.st_size - off));

  void *buf = malloc(size);
  assert(buf != NULL);
  ext2_read(ino, buf, off, size);
  error = fuse_reply_buf(req, buf, size);
  assert(error == 0);
  free(buf);
}

static void e2fs_statfs(fuse_req_t req, fuse_ino_t ino __unused) {
  struct statvfs statfs;
  memset(&statfs, 0, sizeof(statfs));
  fuse_reply_statfs(req, &statfs);
}

static struct fuse_lowlevel_ops e2fs_oper = {
  .lookup = e2fs_lookup,
  .getattr = e2fs_getattr,
  .readdir = e2fs_readdir,
  .readlink = e2fs_readlink,
  .open = e2fs_open,
  .read = e2fs_read,
  .statfs = e2fs_statfs,
};

int main(int argc, char *argv[]) {
  struct fuse_args args = FUSE_ARGS_INIT(argc, argv);
  struct fuse_chan *ch;
  struct fuse_session *se;
  char *mountpoint;
  int multithreaded, foreground, err = -1;

  if ((err = ext2_mount("debian9-ext2.img"))) {
    fprintf(stderr, "Cannot open 'debian9-ext2.img': %s!\n", strerror(err));
    return EXIT_FAILURE;
  }

  if (!fuse_parse_cmdline(&args, &mountpoint, &multithreaded, &foreground) &&
      (ch = fuse_mount(mountpoint, &args))) {
    if ((se = fuse_lowlevel_new(&args, &e2fs_oper, sizeof(e2fs_oper), NULL))) {
      if (fuse_set_signal_handlers(se) != -1) {
        fuse_session_add_chan(se, ch);
        err = fuse_session_loop(se);
        fuse_remove_signal_handlers(se);
        fuse_session_remove_chan(ch);
      }
      fuse_session_destroy(se);
    }
    fuse_unmount(mountpoint, ch);
  }
  fuse_opt_free_args(&args);

  return err ? 1 : 0;
}
