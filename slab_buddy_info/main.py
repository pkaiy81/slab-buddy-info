import argparse
import time
import curses
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
        default=3,
        help="Set the update interval in seconds for real-time monitoring.",
    )
    parser.add_argument(
        "--graph",
        action="store_true",
        help="Generate time-series line graphs after execution.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Specify the top N slabs to display.",
    )
    parser.add_argument(
        "--output",
        choices=["html"],
        default="html",
        help="Set the output format for the graph ('html').",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="slab_buddy_graph",
        help="Filename to save the graph (without extension).",
    )
    args = parser.parse_args()

    slabinfo = SlabInfo()
    buddyinfo = BuddyInfo()
    utils = Utils()

    try:
        curses.wrapper(run_top_interface, slabinfo, buddyinfo, utils, args)
    except KeyboardInterrupt:
        print("Exiting...")


def run_top_interface(stdscr, slabinfo, buddyinfo, utils, args):
    curses.use_default_colors()
    stdscr.nodelay(True)  # Set getch() non-blocking
    interval = args.interval
    top_n = args.top

    # Initialize data storage for time-series graphs
    time_series_data = {
        "timestamps": [],
        "slab_usage": {},  # key: slab name, value: list of usage over time
    }

    while True:
        # Capture start time
        start_time = time.time()

        # Get slab and buddy data
        slab_data = slabinfo.parse_slabinfo()
        buddy_data = buddyinfo.parse_buddyinfo()

        # Sort slab data by usage
        slab_data_sorted = sorted(
            slab_data,
            key=lambda x: x["active_objs"] * x["objsize"],
            reverse=True,
        )[:top_n]

        # Update time-series data
        timestamp = time.strftime("%H:%M:%S")
        time_series_data["timestamps"].append(timestamp)
        for slab in slab_data_sorted:
            name = slab["name"]
            usage = slab["active_objs"] * slab["objsize"]
            if name not in time_series_data["slab_usage"]:
                time_series_data["slab_usage"][name] = []
            time_series_data["slab_usage"][name].append(usage)

        # Clear the screen
        stdscr.clear()

        # Get terminal size
        max_y, max_x = stdscr.getmaxyx()
        half_x = max_x // 2  # Divide the screen width by 2
        current_line_left = 0
        current_line_right = 0

        try:
            # Display slab info on the left side
            stdscr.addstr(current_line_left, 0, "=== Slab Allocator Top Usage ===")
            current_line_left += 1
            slab_header = "{:<20} {:>15} {:>15}"
            stdscr.addstr(
                current_line_left,
                0,
                slab_header.format("Name", "Active Objects", "Usage (Bytes)"),
            )
            current_line_left += 1

            for idx, slab in enumerate(slab_data_sorted):
                if current_line_left >= max_y - 1:
                    break  # Stop if we reach the bottom of the screen
                row = "{:<20} {:>15} {:>15}"
                stdscr.addstr(
                    current_line_left,
                    0,
                    row.format(
                        slab["name"],
                        slab["active_objs"],
                        slab["active_objs"] * slab["objsize"],
                    ),
                )
                current_line_left += 1

            # Display buddy info on the right side
            stdscr.addstr(
                current_line_right, half_x, "=== Buddy Allocator Information ==="
            )
            current_line_right += 1

            for entry in buddy_data:
                if current_line_right >= max_y - 1:
                    break  # Stop if we reach the bottom of the screen
                stdscr.addstr(
                    current_line_right,
                    half_x,
                    f"Node {entry['node']}, Zone {entry['zone']}:",
                )
                current_line_right += 1
                if current_line_right >= max_y - 1:
                    break
                stdscr.addstr(current_line_right, half_x, "Order | Free Blocks")
                current_line_right += 1

                for order, count in enumerate(entry["free_counts"]):
                    if current_line_right >= max_y - 1:
                        break  # Stop if we reach the bottom of the screen
                    stdscr.addstr(current_line_right, half_x, f"{order:>5} | {count}")
                    current_line_right += 1

                current_line_right += 1  # Add extra line between zones

            # Add instruction at the bottom
            if max_y - 1 > 0:
                stdscr.addstr(max_y - 1, 0, "Press 'q' to quit.")

            stdscr.refresh()

        except curses.error:
            # Ignore curses errors when trying to write outside the screen
            pass

        # Wait for the interval, adjust for processing time
        elapsed_time = time.time() - start_time
        time_to_wait = max(0, interval - elapsed_time)
        try:
            time.sleep(time_to_wait)
        except KeyboardInterrupt:
            break

        # Check for user input to exit
        key = stdscr.getch()
        if key == ord("q"):
            break

    # After exiting the loop, generate graphs if requested
    if args.graph:
        utils.generate_time_series_graph(
            time_series_data, filename=args.filename, top_n=top_n
        )
        print(f"Graph saved to {args.filename}.html")


if __name__ == "__main__":
    main()
