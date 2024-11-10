class Utils:
    def display_slabinfo(self, slab_data):
        """Display slab allocator information.

        Args:
            slab_data (list): List of dictionaries containing slab information.

        Linux slabinfo example:
        # name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
        ufs_inode_cache        0      0    808   20    4 : tunables    0    0    0 : slabdata      0      0      0
        qnx4_inode_cache       0      0    680   24    4 : tunables    0    0    0 : slabdata      0      0      0
        """
        header = "{:<20} {:>12} {:>10} {:>8} {:>12} {:>14} {:>10} {:>12} {:>14} {:>14} {:>14} {:>12} {:>12}"
        print(
            header.format(
                "Name",
                "ActiveObjs",
                "NumObjs",
                "ObjSize",
                "ObjPerSlab",
                "PagesPerSlab",
                "Limit",
                "BatchCount",
                "SharedFactor",
                "ActiveSlabs",
                "NumSlabs",
                "SharedAvail",
            )
        )
        for slab in slab_data:
            row = "{:<20} {:>12} {:>10} {:>8} {:>12} {:>14} {:>10} {:>12} {:>14} {:>14} {:>14} {:>12} {:>12}"
            print(
                row.format(
                    slab["name"],
                    slab["active_objs"],
                    slab["num_objs"],
                    slab["objsize"],
                    slab["objperslab"],
                    slab["pagesperslab"],
                    slab["limit"] if slab["limit"] is not None else "",
                    slab["batchcount"] if slab["batchcount"] is not None else "",
                    slab["sharedfactor"] if slab["sharedfactor"] is not None else "",
                    slab["active_slabs"] if slab["active_slabs"] is not None else "",
                    slab["num_slabs"] if slab["num_slabs"] is not None else "",
                    slab["sharedavail"] if slab["sharedavail"] is not None else "",
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
