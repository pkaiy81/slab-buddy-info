class Utils:
    def display_slabinfo(self, slab_data):
        print(
            "{:<20} {:>10} {:>10} {:>10}".format("Name", "Active", "Total", "ObjSize")
        )
        for slab in slab_data:
            print(
                "{:<20} {:>10} {:>10} {:>10}".format(
                    slab["name"], slab["active_objs"], slab["num_objs"], slab["objsize"]
                )
            )

    def display_buddyinfo(self, buddy_data):
        for entry in buddy_data:
            print(f"Node {entry['node']}, Zone {entry['zone']}:")
            print("Order | Free Blocks")
            for order, count in enumerate(entry["free_counts"]):
                print(f"{order:>5} | {count}")
            print()

    def text_bar_graph(self, labels, values, max_width=50):
        max_value = max(values) if max(values) > 0 else 1
        for label, value in zip(labels, values):
            bar_length = int((value / max_value) * max_width)
            bar = "#" * bar_length
            print(f"{label:<20} | {bar} ({value})")
