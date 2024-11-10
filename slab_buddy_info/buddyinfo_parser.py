class BuddyInfo:
    """Parse /proc/buddyinfo to get buddy allocator information.

    Attributes:
        filepath (str): The path to the buddyinfo file.

    Linux buddyinfo example:
    Node 0, zone      DMA      1      0      0      1      2      1      1      0      1      1      3
    Node 0, zone    DMA32   5625   3348    349    130     76     67     16      7      2      3    389
    Node 0, zone   Normal    512     88     14     97      9      0     29     36     20      0      0
    """

    def __init__(self, filepath="/proc/buddyinfo"):
        self.filepath = filepath

    def parse_buddyinfo(self):
        try:
            with open(self.filepath, "r") as f:
                lines = f.readlines()
                buddy_data = []
                for line in lines:
                    fields = line.strip().split()
                    if len(fields) >= 4:
                        node = fields[1].split(",")[0]
                        zone = fields[3]
                        free_counts = list(map(int, fields[4:]))
                        buddy_data.append(
                            {"node": node, "zone": zone, "free_counts": free_counts}
                        )
                return buddy_data
        except FileNotFoundError:
            print("Error: /proc/buddyinfo not found.")
            return []
        except Exception as e:
            print(f"Error parsing /proc/buddyinfo: {e}")
            return []
