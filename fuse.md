# bpftrace code to track FUSE requests

Example on how to run the command. Feel free to enable or disable certain records

```bash
# BPFTRACE_MAP_KEYS_MAX=65536 sudo bpftrace  fuse.bt -o fuse.res
```

Use fuse_parser as an example on parsing the results

```bash
# ./fuse_parser fuse.res
```
