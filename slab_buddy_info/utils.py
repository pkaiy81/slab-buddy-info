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
        print(
            f"{'Name':<20} {'Active Objs':>10} {'Num Objs':>10} {'Objsize':>10} {'Objperslab':>10} {'Pagesperslab':>10} {'Limit':>10} {'Batchcount':>10} {'Sharedfactor':>10} {'Active Slabs':>10} {'Num Slabs':>10} {'Sharedavail':>10}"
        )
        for slab in slab_data:
            print(
                f"{slab['name']:<20} {slab['active_objs']:>10} {slab['num_objs']:>10} {slab['objsize']:>10} {slab['objperslab']:>10} {slab['pagesperslab']:>10} {slab['limit']:>10} {slab['batchcount']:>10} {slab['sharedfactor']:>10} {slab['active_slabs']:>10} {slab['num_slabs']:>10} {slab['sharedavail']:>10}"
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
