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
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Split the line into sections separated by ':'
                    sections = line.split(":")
                    if len(sections) < 3:
                        continue  # Malformed line
                    # Parse the first section
                    first_part = sections[0].strip().split()
                    if len(first_part) < 6:
                        continue  # Not enough data
                    name = first_part[0]
                    active_objs = int(first_part[1])
                    num_objs = int(first_part[2])
                    objsize = int(first_part[3])
                    objperslab = int(first_part[4])
                    pagesperslab = int(first_part[5])

                    # Parse the tunables section
                    tunables_part = sections[1].strip().split()
                    # The first element should be 'tunables', skip it
                    if tunables_part and tunables_part[0] == "tunables":
                        tunables_values = tunables_part[1:]
                    else:
                        tunables_values = tunables_part
                    limit = (
                        int(tunables_values[0]) if len(tunables_values) > 0 else None
                    )
                    batchcount = (
                        int(tunables_values[1]) if len(tunables_values) > 1 else None
                    )
                    sharedfactor = (
                        int(tunables_values[2]) if len(tunables_values) > 2 else None
                    )

                    # Parse the slabdata section
                    slabdata_part = sections[2].strip().split()
                    # The first element should be 'slabdata', skip it
                    if slabdata_part and slabdata_part[0] == "slabdata":
                        slabdata_values = slabdata_part[1:]
                    else:
                        slabdata_values = slabdata_part
                    active_slabs = (
                        int(slabdata_values[0]) if len(slabdata_values) > 0 else None
                    )
                    num_slabs = (
                        int(slabdata_values[1]) if len(slabdata_values) > 1 else None
                    )
                    sharedavail = (
                        int(slabdata_values[2]) if len(slabdata_values) > 2 else None
                    )

                    slab = {
                        "name": name,
                        "active_objs": active_objs,
                        "num_objs": num_objs,
                        "objsize": objsize,
                        "objperslab": objperslab,
                        "pagesperslab": pagesperslab,
                        "limit": limit,
                        "batchcount": batchcount,
                        "sharedfactor": sharedfactor,
                        "active_slabs": active_slabs,
                        "num_slabs": num_slabs,
                        "sharedavail": sharedavail,
                    }
                    slab_data.append(slab)
            return slab_data
        except FileNotFoundError:
            print("Error: /proc/slabinfo not found.")
            return []
        except Exception as e:
            print(f"Error parsing /proc/slabinfo: {e}")
            return []
