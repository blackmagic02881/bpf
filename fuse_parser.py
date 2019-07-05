#!/usr/bin/env python
import sys
import json
from enum import Enum

# see FUSE OP code definition at https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/include/uapi/linux/fuse.h?h=v5.1.16#n358


class FUSEOPCode(Enum):
    FUSE_LOOKUP = 1
    FUSE_FORGET = 2
    FUSE_GETATTR = 3
    FUSE_SETATTR = 4
    FUSE_READLINK = 5
    FUSE_SYMLINK = 6
    FUSE_MKNOD = 8
    FUSE_MKDIR = 9
    FUSE_UNLINK = 10
    FUSE_RMDIR = 11
    FUSE_RENAME = 12
    FUSE_LINK = 13
    FUSE_OPEN = 14
    FUSE_READ = 15
    FUSE_WRITE = 16
    FUSE_STATFS = 17
    FUSE_RELEASE = 18
    FUSE_FSYNC = 20
    FUSE_SETXATTR = 21
    FUSE_GETXATTR = 22
    FUSE_LISTXATTR = 23
    FUSE_REMOVEXATTR = 24
    FUSE_FLUSH = 25
    FUSE_INIT = 26
    FUSE_OPENDIR = 27
    FUSE_READDIR = 28
    FUSE_RELEASEDIR = 29
    FUSE_FSYNCDIR = 30
    FUSE_GETLK = 31
    FUSE_SETLK = 32
    FUSE_SETLKW = 33
    FUSE_ACCESS = 34
    FUSE_CREATE = 35
    FUSE_INTERRUPT = 36
    FUSE_BMAP = 37
    FUSE_DESTROY = 38
    FUSE_IOCTL = 39
    FUSE_POLL = 40
    FUSE_NOTIFY_REPLY = 41
    FUSE_BATCH_FORGET = 42
    FUSE_FALLOCATE = 43
    FUSE_READDIRPLUS = 44
    FUSE_RENAME2 = 45
    FUSE_LSEEK = 46
    FUSE_COPY_FILE_RANGE = 47
    CUSE_INIT = 4096


result = {
    'PID_COMM': {},
    'FUSE_OP': {},
    'COMM': {},
    'PID_OP': {},
}


def k_v_parser(line):
    k, v = line.split('[')[1].split(']:')
    return k.strip(), v.strip()


def parse_pid_comm(line):
    k, v = k_v_parser(line)
    result['PID_COMM'][k] = v


def parse_req_by_op(line):
    k, v = k_v_parser(line)
    result['FUSE_OP'][str(FUSEOPCode(int(k)))] = int(v)


def parse_req_by_pid_op(line):
    k, v = k_v_parser(line)
    # this 256 need to match the value in the bpftrace script
    pid, op = divmod(int(k), 256)
    if pid not in result['PID_OP']:
        result['PID_OP'][pid] = dict()
    result['PID_OP'][pid][str(FUSEOPCode(op))] = int(v)


def parse_req_by_comm(line):
    k, v = k_v_parser(line)
    result['COMM'][k] = int(v)


parsers = {
    '@pid_comm': parse_pid_comm,
    '@fusereq_by_op': parse_req_by_op,
    '@fusereq_by_pid_op': parse_req_by_pid_op,
    '@fusereq_comm': parse_req_by_comm,
}


def process(line):
    for k, v in parsers.items():
        if line.startswith(k):
            v(line)
            break


def save_result():
    print(json.dumps(result, indent=2))


def main():
    with open(sys.argv[1], 'r') as f:
        for line in f:
            process(line)
    save_result()


if __name__ == "__main__":
    main()
