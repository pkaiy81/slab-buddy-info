class SlabInfo:
    """Parse /proc/slabinfo for slab allocator information.

    Attributes:
        filepath (str): The path to the slabinfo file.

    Linux slabinfo example:
    # name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
    ufs_inode_cache        0      0    808   20    4 : tunables    0    0    0 : slabdata      0      0      0
    qnx4_inode_cache       0      0    680   24    4 : tunables    0    0    0 : slabdata      0      0      0

    """

    def __init__(self, filepath="/proc/slabinfo"):
        self.filepath = filepath

    def parse_slabinfo(self):
        try:
            with open(self.filepath, "r") as f:
                lines = f.readlines()[2:]  # Skip the first two lines of headers
                slab_data = []
                for line in lines:
                    fields = line.strip().split()
                    if len(fields) >= 7:
                        slab = {
                            "name": fields[0],
                            "active_objs": int(fields[1]),
                            "num_objs": int(fields[2]),
                            "objsize": int(fields[3]),
                            "objperslab": int(fields[4]),
                            "pagesperslab": int(fields[5]),
                            # tunables
                            # Optional fields (may not be present in all kernels)
                            "limit": int(fields[7]) if len(fields) > 7 else None,
                            "batchcount": int(fields[8]) if len(fields) > 8 else None,
                            "sharedfactor": int(fields[9]) if len(fields) > 9 else None,
                            # slabdata
                            "active_slabs": (
                                int(fields[11]) if len(fields) > 11 else None
                            ),
                            "num_slabs": int(fields[12]) if len(fields) > 12 else None,
                            "sharedavail": (
                                int(fields[13]) if len(fields) > 13 else None
                            ),
                        }
                        slab_data.append(slab)
            return slab_data
        except FileNotFoundError:
            print("Error: /proc/slabinfo not found.")
            return []
        except Exception as e:
            print(f"Error parsing /proc/slabinfo: {e}")
            return []
