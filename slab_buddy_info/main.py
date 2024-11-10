import argparse
import time
from .slabinfo_parser import SlabInfo
from .buddyinfo_parser import BuddyInfo
from .utils import Utils


def main():
    parser = argparse.ArgumentParser(
        description="Display Linux kernel slab and buddy allocator information."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Set the update interval in seconds for real-time monitoring.",
    )
    parser.add_argument(
        "--graph",
        action="store_true",
        help="Enable graph display after execution.",
    )
    parser.add_argument(
        "--output",
        choices=["text", "html"],
        default="text",
        help="Set the output format for the graph ('text' or 'html').",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the graph to a file instead of displaying it.",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="slab_buddy_graph",
        help="Filename to save the graph (without extension).",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Specify the top N slabs to display in the graph.",
    )
    parser.add_argument(
        "--show-slab",
        action="store_true",
        help="Display only slab allocator information.",
    )
    parser.add_argument(
        "--show-buddy",
        action="store_true",
        help="Display only buddy allocator information.",
    )
    args = parser.parse_args()

    if not args.show_slab and not args.show_buddy:
        # If neither is specified, display both
        args.show_slab = True
        args.show_buddy = True

    slabinfo = SlabInfo()
    buddyinfo = BuddyInfo()
    utils = Utils()

    try:
        while True:
            if args.show_slab:
                slab_data = slabinfo.parse_slabinfo()
                print("\n=== Slab Allocator Information ===")
                utils.display_slabinfo(slab_data)

            if args.show_buddy:
                buddy_data = buddyinfo.parse_buddyinfo()
                print("\n=== Buddy Allocator Information ===")
                utils.display_buddyinfo(buddy_data)

            if args.interval <= 0:
                break
            else:
                time.sleep(args.interval)
                print("\033[H\033[J", end="")  # Clear the screen

        # After execution, generate graphs if requested
        if args.graph:
            if args.show_slab:
                # Generate slab graph
                slab_data = slabinfo.parse_slabinfo()
                sorted_slab = sorted(
                    slab_data,
                    key=lambda x: x["active_objs"] * x["objsize"],
                    reverse=True,
                )[: args.top]
                labels = [slab["name"] for slab in sorted_slab]
                values = [slab["active_objs"] * slab["objsize"] for slab in sorted_slab]
                if args.output == "text":
                    utils.text_bar_graph(labels, values)
                elif args.output == "html":
                    html_content = utils.generate_html_bar_graph(
                        labels, values, title="Slab Usage Graph"
                    )
                    if args.save:
                        filename = f"{args.filename}_slab.html"
                        with open(filename, "w") as f:
                            f.write(html_content)
                        print(f"Slab graph saved to {filename}")
                    else:
                        utils.display_html_in_terminal(html_content)

            if args.show_buddy:
                # Generate buddy graph
                buddy_data = buddyinfo.parse_buddyinfo()
                labels, values = utils.prepare_buddy_graph_data(buddy_data)
                if args.output == "text":
                    utils.text_bar_graph(labels, values)
                elif args.output == "html":
                    html_content = utils.generate_html_bar_graph(
                        labels, values, title="Buddy Allocator Free Blocks"
                    )
                    if args.save:
                        filename = f"{args.filename}_buddy.html"
                        with open(filename, "w") as f:
                            f.write(html_content)
                        print(f"Buddy graph saved to {filename}")
                    else:
                        utils.display_html_in_terminal(html_content)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
