CC = gcc -fsanitize=address -g
CFLAGS = -Og -Wall -Wextra -Werror

all: ext2fuse ext2test ext2list listfs

ext2fs.o: ext2fs.c ext2fs.h ext2fs_defs.h
md5c.o: md5c.c md5.h

ext2fuse: ext2fuse.o ext2fs.o
ext2fuse: LDLIBS += $(shell pkg-config --libs fuse)
ext2fuse.o: ext2fuse.c ext2fs.h ext2fs_defs.h
ext2fuse.o: CFLAGS += $(shell pkg-config --cflags fuse)

ext2test: ext2test.o ext2fs.o
ext2test: LDLIBS += -lreadline
ext2test.o: ext2test.c ext2fs.h ext2fs_defs.h

ext2list: ext2list.o ext2fs.o md5c.o
ext2list.o: ext2test.c ext2fs.h ext2fs_defs.h md5.h

listfs: listfs.o md5c.o
listfs.o: listfs.c md5.h

grade:
	./grade.sh

format:
	clang-format -i *.c *.h

clean:
	rm -f *~ *.o ext2fuse ext2test ext2list listfs

# vim: ts=8 sw=8 noet
