class BuddyInfo:
    def __inti__(self, filepath="/proc/buddyinfo"):
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
