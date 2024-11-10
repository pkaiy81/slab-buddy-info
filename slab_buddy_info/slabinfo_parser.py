class SlabInfo:
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
                            # Convert to bytes
                            # "size": int(fields[6]) * 1024,
                            # # Optional fields (may not be present in all kernels)
                            # "limit": (
                            #     int(fields[7]) * 1024 if len(fields) >= 8 else None
                            # ),
                            # "batchcount": int(fields[8]) if len(fields) >= 9 else None,
                            # "sharedfactor": (
                            #     int(fields[9]) if len(fields) >= 10 else None
                            # ),
                        }
                        slab_data.append(slab)
            return slab_data
        except FileNotFoundError:
            print("Error: /proc/slabinfo not found.")
            return []
        except Exception as e:
            print(f"Error parsing /proc/slabinfo: {e}")
            return []
