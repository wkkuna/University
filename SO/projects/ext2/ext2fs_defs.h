#pragma once

/* Based on NetBSD's header files from /sys/ufs/ext2fs,
 * namely: ext2fs.h, ext2fs_dinode.h, ext2fs_dir.h */

#include <sys/cdefs.h>
#include <stdint.h>

/*
 * The first super block and block group descriptors offsets are given in
 * absolute disk addresses.
 */
#define EXT2_SBOFF ((off_t)1024)
#define EXT2_GDOFF ((off_t)2048)

/*
 * Filesystem identification
 */
#define EXT2_MAGIC 0xEF53 /* the ext2fs magic number */
#define EXT2_REV0 0       /* GOOD_OLD revision */
#define EXT2_REV1 1       /* Support compat/incompat features */

/*
 * File system super block.
 */
typedef struct ext2_superblock {
  uint32_t sb_icount;        /* Inode count */
  uint32_t sb_bcount;        /* blocks count */
  uint32_t sb_rbcount;       /* reserved blocks count */
  uint32_t sb_fbcount;       /* free blocks count */
  uint32_t sb_ficount;       /* free inodes count */
  uint32_t sb_first_dblock;  /* first data block */
  uint32_t sb_log_bsize;     /* bsize = 1024*(2^sb_log_bsize) */
  uint32_t sb_fsize;         /* fragment size */
  uint32_t sb_bpg;           /* blocks per group */
  uint32_t sb_fpg;           /* frags per group */
  uint32_t sb_ipg;           /* inodes per group */
  uint32_t sb_mtime;         /* mount time */
  uint32_t sb_wtime;         /* write time */
  uint16_t sb_mnt_count;     /* mount count */
  uint16_t sb_max_mnt_count; /* max mount count */
  uint16_t sb_magic;         /* magic number */
  uint16_t sb_state;         /* file system state */
  uint16_t sb_beh;           /* behavior on errors */
  uint16_t sb_minrev;        /* minor revision level */
  uint32_t sb_lastfsck;      /* time of last fsck */
  uint32_t sb_fsckintv;      /* max time between fscks */
  uint32_t sb_creator;       /* creator OS */
  uint32_t sb_rev;           /* revision level */
  uint16_t sb_ruid;          /* default uid for reserved blocks */
  uint16_t sb_rgid;          /* default gid for reserved blocks */
  /* EXT2_DYNAMIC_REV superblocks */
  uint32_t sb_first_ino;         /* first non-reserved inode */
  uint16_t sb_inode_size;        /* size of inode structure */
  uint16_t sb_block_group_nr;    /* block grp number of this sblk */
  uint32_t sb_features_compat;   /*  compatible feature set */
  uint32_t sb_features_incompat; /* incompatible feature set */
  uint32_t sb_features_rocompat; /* RO-compatible feature set */
  uint8_t sb_uuid[16];           /* 128-bit uuid for volume */
  char sb_vname[16];             /* volume name */
  char sb_fsmnt[64];             /* name mounted on */
  uint32_t sb_algo;              /* For compression */
  uint8_t sb_prealloc;           /* # of blocks to preallocate */
  uint8_t sb_dir_prealloc;       /* # of blocks to preallocate for dir */
  uint16_t sb_reserved_ngdb;     /* # of reserved gd blocks for resize */
} ext2_superblock_t;

#define ext2_blksize(sb) (1024UL << (sb)->sb_log_bsize)

/*
 * File system block group descriptor.
 */
typedef struct ext2_groupdesc {
  uint32_t gd_b_bitmap; /* blocks bitmap block */
  uint32_t gd_i_bitmap; /* inodes bitmap block */
  uint32_t gd_i_tables; /* first inodes table block */
  uint16_t gd_nbfree;   /* number of free blocks */
  uint16_t gd_nifree;   /* number of free inodes */
  uint16_t gd_ndirs;    /* number of directories */

  /*
   * Following only valid when either GDT_CSUM or METADATA_CKSUM feature is on.
   */
  uint16_t gd_flags;                /* ext4 bg flags (INODE_UNINIT, ...)*/
  uint32_t gd_exclude_bitmap_lo;    /* snapshot exclude bitmap */
  uint16_t gd_block_bitmap_csum_lo; /* Low block bitmap checksum */
  uint16_t gd_inode_bitmap_csum_lo; /* Low inode bitmap checksum */
  uint16_t gd_itable_unused_lo;     /* Low unused inode offset */
  uint16_t gd_checksum;             /* Group desc checksum */
} ext2_groupdesc_t;

/*
 * A block group has backup copy of the superblock and block group descriptors
 * only if it's 1, a power of 3, 5 or 7
 */
static inline int ext2_gd_has_backup(int i) {
  int a3, a5, a7;

  if (i == 0 || i == 1)
    return 1;
  for (a3 = 3, a5 = 5, a7 = 7; a3 <= i || a5 <= i || a7 <= i;
       a3 *= 3, a5 *= 5, a7 *= 7)
    if (i == a3 || i == a5 || i == a7)
      return 1;
  return 0;
}

/*
 * A dinode contains all the meta-data associated with a file. This structure
 * defines the on-disk format of a dinode. Since this structure describes an
 * on-disk structure, all its fields are defined by types with precise widths.
 */

#define EXT2_NDADDR 12 /* Direct addresses in inode. */
#define EXT2_NIADDR 3  /* Indirect addresses in inode. */
#define EXT2_NADDR (EXT2_NDADDR + EXT2_NIADDR)

#define EXT2_MAXSYMLINKLEN ((EXT2_NDADDR + EXT2_NIADDR) * sizeof(uint32_t))

/*
 * The root inode is the root of the file system.  Inode 0 can't be used for
 * normal purposes and bad blocks are normally linked to inode 1, thus
 * the root inode is 2.
 * Inode 3 to 10 are reserved in ext2fs.
 */
#define EXT2_BADBLKINO ((ino_t)1)
#define EXT2_ROOTINO ((ino_t)2)
#define EXT2_ACLIDXINO ((ino_t)3)
#define EXT2_ACLDATAINO ((ino_t)4)
#define EXT2_BOOTLOADERINO ((ino_t)5)
#define EXT2_UNDELDIRINO ((ino_t)6)
#define EXT2_RESIZEINO ((ino_t)7)
#define EXT2_JOURNALINO ((ino_t)8)
#define EXT2_FIRSTINO ((ino_t)11)

/*
 * Structure of an inode on the disk.
 */
typedef struct ext2_inode {
  uint16_t i_mode;               /*   0: IFMT, permissions; see below. */
  uint16_t i_uid;                /*   2: Owner UID */
  uint32_t i_size;               /*   4: Size (in bytes) */
  uint32_t i_atime;              /*   8: Access time */
  uint32_t i_ctime;              /*  12: Change time */
  uint32_t i_mtime;              /*  16: Modification time */
  uint32_t i_dtime;              /*  20: Deletion time */
  uint16_t i_gid;                /*  24: Owner GID */
  uint16_t i_nlink;              /*  26: File link count */
  uint32_t i_nblock;             /*  28: Blocks count */
  uint32_t i_flags;              /*  32: Status flags (chflags) */
  uint32_t i_version;            /*  36: Low 32 bits inode version */
  uint32_t i_blocks[EXT2_NADDR]; /*  40: disk blocks */
  uint32_t i_gen;                /* 100: generation number */
  uint32_t i_facl;               /* 104: Low EA block */
  uint32_t i_size_high;          /* 108: Upper bits of file size */
  uint32_t i_faddr;              /* 112: Fragment address (obsolete) */
  uint16_t i_nblock_high;        /* 116: Blocks count bits 47:32 */
  uint16_t i_facl_high;          /* 118: File EA bits 47:32 */
  uint16_t i_uid_high;           /* 120: Owner UID top 16 bits */
  uint16_t i_gid_high;           /* 122: Owner GID top 16 bits */
  uint16_t i_chksum_lo;          /* 124: Lower inode checksum */
  uint16_t i_lx_reserved;        /* 126: Unused */
} ext2_inode_t;

_Static_assert(sizeof(ext2_inode_t) == 128,
               "size of ext2 i-node must be 128 bytes");

/* File permissions. */
#define EXT2_IEXEC 0000100  /* Executable. */
#define EXT2_IWRITE 0000200 /* Writable. */
#define EXT2_IREAD 0000400  /* Readable. */
#define EXT2_ISVTX 0001000  /* Sticky bit. */
#define EXT2_ISGID 0002000  /* Set-gid. */
#define EXT2_ISUID 0004000  /* Set-uid. */

/* File types. */
#define EXT2_IFMT 0170000   /* Mask of file type. */
#define EXT2_IFIFO 0010000  /* Named pipe (fifo). */
#define EXT2_IFCHR 0020000  /* Character device. */
#define EXT2_IFDIR 0040000  /* Directory file. */
#define EXT2_IFBLK 0060000  /* Block device. */
#define EXT2_IFREG 0100000  /* Regular file. */
#define EXT2_IFLNK 0120000  /* Symbolic link. */
#define EXT2_IFSOCK 0140000 /* UNIX domain socket. */

/*
 * A directory consists of some number of blocks of e2fs_blksize bytes.
 *
 * Each block contains some number of directory entry structures, which are of
 * variable length. Each directory entry has a struct direct at the front of
 * it, containing its inode number, the length of the entry, and the length of
 * the name contained in the entry. These are followed by the name padded to a
 * 4 byte boundary with null bytes. All names are guaranteed null terminated.
 * The maximum length of a name in a directory is EXT2_MAXNAMLEN.
 */

/* Ext2 directory file types. */
enum {
  EXT2_FT_UNKNOWN = 0,
  EXT2_FT_REG = 1,
  EXT2_FT_DIR = 2,
  EXT2_FT_CHRDEV = 3,
  EXT2_FT_BLKDEV = 4,
  EXT2_FT_FIFO = 5,
  EXT2_FT_SOCK = 6,
  EXT2_FT_SYMLINK = 7,
};

/*
 * The EXT2_DIRSIZE macro gives the minimum record length which will hold
 * the directory entry for a name of length `len` (without the terminating null
 * byte). This requires the amount of space in struct direct without the
 * de_name field, plus enough space for the name without a terminating null
 * byte, rounded up to a 4 byte boundary.
 */
#define EXT2_DIRSIZE(len) roundup2(8 + len, 4)

#define EXT2_MAXNAMLEN 255

typedef struct ext2_dirent {
  uint32_t de_ino;                  /* inode number of entry */
  uint16_t de_reclen;               /* length of this record */
  uint8_t de_namelen;               /* length of string in de_name */
  uint8_t de_type;                  /* file type */
  char de_name[EXT2_MAXNAMLEN + 1]; /* name with length <= EXT2_MAXNAMLEN */
} ext2_dirent_t;
