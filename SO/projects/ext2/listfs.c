#define _GNU_SOURCE
#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <sys/stat.h>
#include <unistd.h>

#include "md5.h"

static int showfile(const char *path) {
  struct stat sb[1];

  memset(sb, 0, sizeof(struct stat));

  (void)lstat(path, sb);

  printf("path=%s ino=%ld mode=%o nlink=%ld uid=%d gid=%d "
         "size=%ld atime=%ld mtime=%ld ctime=%ld",
         path, sb->st_ino, sb->st_mode, sb->st_nlink, sb->st_uid, sb->st_gid,
         sb->st_size, sb->st_atime, sb->st_mtime, sb->st_ctime);

  switch (sb->st_mode & S_IFMT) {
    case S_IFREG: {
      char *md5sum = MD5File(path, NULL);
      printf(" md5=%s", md5sum);
      free(md5sum);
      break;
    }
    case S_IFLNK: {
      char symlink[PATH_MAX + 1] = "?";
      ssize_t size;
      if ((size = readlink(path, symlink, PATH_MAX)) > 0)
        symlink[size] = '\0';
      printf(" target=%s", symlink);
      break;
    }
    default:
      break;
  }
  putchar('\n');

  return 0;
}

static int listdir(const char *path) {
  char newpath[strlen(path) + MAXNAMLEN + 2];

  DIR *dirp = opendir(path);
  if (dirp == NULL)
    return ENOENT;

  struct dirent *dp;
  while ((dp = readdir(dirp))) {
    if (strcmp(dp->d_name, ".") == 0)
      continue;
    if (strcmp(dp->d_name, "..") == 0)
      continue;

    strcpy(newpath, path);
    strcat(newpath, "/");
    strcat(newpath, dp->d_name);
    showfile(newpath);

    if (dp->d_type == DT_DIR)
      listdir(newpath);
  }

  (void)closedir(dirp);
  return 0;
}

int main(int argc, char *argv[]) {
  if (argc == 2) {
    if (chdir(argv[1])) {
      perror("chdir");
      exit(EXIT_FAILURE);
    }
  }

  (void)showfile(".");
  (void)listdir(".");
  exit(EXIT_SUCCESS);
}
