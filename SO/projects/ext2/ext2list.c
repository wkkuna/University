#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "md5.h"
#include "ext2fs.h"

static void showfile(const char *path, uint32_t ino) {
  struct stat sb[1];

  memset(sb, 0, sizeof(struct stat));
  ext2_stat(ino, sb);

  printf("path=%s ino=%ld mode=%o nlink=%ld uid=%d gid=%d "
         "size=%ld atime=%ld mtime=%ld ctime=%ld",
         path, sb->st_ino, sb->st_mode, sb->st_nlink, sb->st_uid, sb->st_gid,
         sb->st_size, sb->st_atime, sb->st_mtime, sb->st_ctime);

  switch (sb->st_mode & S_IFMT) {
    case S_IFREG: {
      uint8_t data[BLKSIZE];
      size_t pos = 0;
      size_t len = sb->st_size;
      MD5_CTX ctx;

      MD5Init(&ctx);

      while (len > 0) {
        size_t cnt = min(len, BLKSIZE);
        if (ext2_read(ino, data, pos, cnt))
          break;
        MD5Update(&ctx, data, cnt);
        len -= cnt;
        pos += cnt;
      }

      char md5sum[MD5_DIGEST_STRING_LENGTH];
      MD5End(&ctx, md5sum);
      printf(" md5=%s", md5sum);
      break;
    }
    case S_IFLNK: {
      char symlink[sb->st_size + 1];
      if (ext2_readlink(ino, symlink, sb->st_size)) {
        strcpy(symlink, "?");
      } else {
        symlink[sb->st_size] = '\0';
      }
      printf(" target=%s", symlink);
      break;
    }
    default:
      break;
  }
  putchar('\n');
}

static void listdir(const char *path, uint32_t ino) {
  char newpath[strlen(path) + EXT2_MAXNAMLEN + 2];

  ext2_dirent_t de;
  uint32_t off = 0;
  while (ext2_readdir(ino, &off, &de)) {
    if (strncmp(de.de_name, ".", de.de_namelen) == 0)
      continue;
    if (strncmp(de.de_name, "..", de.de_namelen) == 0)
      continue;

    strcpy(newpath, path);
    strcat(newpath, "/");
    strcat(newpath, de.de_name);

    showfile(newpath, de.de_ino);

    if (de.de_type == EXT2_FT_DIR)
      listdir(newpath, de.de_ino);
  }
}

int main(void) {
  if (ext2_mount("debian9-ext2.img"))
    exit(EXIT_FAILURE);

  showfile(".", EXT2_ROOTINO);
  listdir(".", EXT2_ROOTINO);
  exit(EXIT_SUCCESS);
}
