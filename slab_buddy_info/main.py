# main.py

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
    # Initialize curses
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # White on black

    stdscr.nodelay(True)  # Non-blocking input
    interval = args.interval
    top_n = args.top

    # Initialize time series data
    time_series_data = {
        "timestamps": [],
        "slab_usage": {},  # key: slab name, value: list of usage over time
    }

    while True:
        start_time = time.time()

        # Slab and buddy allocator information
        slab_data = slabinfo.parse_slabinfo()
        buddy_data = buddyinfo.parse_buddyinfo()

        if not slab_data:
            stdscr.addstr(
                0, 0, "Error: Unable to read /proc/slabinfo.", curses.color_pair(1)
            )
            stdscr.refresh()
            time.sleep(interval)
            continue

        # Calculate summary information
        sum_active_objs = sum(slab["active_objs"] for slab in slab_data)
        sum_total_objs = sum(slab["num_objs"] for slab in slab_data)
        sum_active_slabs = sum(slab["active_slabs"] for slab in slab_data)
        sum_total_slabs = sum(slab["num_slabs"] for slab in slab_data)
        sum_active_caches = sum(1 for slab in slab_data if slab["active_slabs"] > 0)
        sum_total_caches = len(slab_data)
        sum_active_size = sum(
            slab["active_objs"] * slab["objsize"] for slab in slab_data
        )
        sum_total_size = sum(slab["num_objs"] * slab["objsize"] for slab in slab_data)
        min_obj_size = min(slab["objsize"] for slab in slab_data) if slab_data else 0
        avg_obj_size = (
            (sum(slab["objsize"] for slab in slab_data) / len(slab_data))
            if slab_data
            else 0
        )
        max_obj_size = max(slab["objsize"] for slab in slab_data) if slab_data else 0

        # Calculate percentage used
        percent_objs = (
            (sum_active_objs / sum_total_objs * 100) if sum_total_objs > 0 else 0
        )
        percent_slabs = (
            (sum_active_slabs / sum_total_slabs * 100) if sum_total_slabs > 0 else 0
        )
        percent_caches = (
            (sum_active_caches / sum_total_caches * 100) if sum_total_caches > 0 else 0
        )
        percent_size = (
            (sum_active_size / sum_total_size * 100) if sum_total_size > 0 else 0
        )

        # Format size in bytes to human-readable format
        def format_size(size_bytes):
            if size_bytes >= 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.2f}M"
            elif size_bytes >= 1024:
                return f"{size_bytes / 1024:.2f}K"
            else:
                return f"{size_bytes}B"

        # Format size information
        min_obj_size_fmt = format_size(min_obj_size)
        avg_obj_size_fmt = format_size(avg_obj_size)
        max_obj_size_fmt = format_size(max_obj_size)

        summary_lines = [
            f"Active / Total Objects (% used)    : {sum_active_objs} / {sum_total_objs} ({percent_objs:.1f}%)",
            f"Active / Total Slabs (% used)      : {sum_active_slabs} / {sum_total_slabs} ({percent_slabs:.1f}%)",
            f"Active / Total Caches (% used)     : {sum_active_caches} / {sum_total_caches} ({percent_caches:.1f}%)",
            f"Active / Total Size (% used)       : {format_size(sum_active_size)} / {format_size(sum_total_size)} ({percent_size:.1f}%)",
            f"Minimum / Average / Maximum Object : {min_obj_size_fmt} / {avg_obj_size_fmt} / {max_obj_size_fmt}",
        ]

        # Sort slab data by usage (active objects * object size)
        slab_data_sorted = sorted(
            slab_data,
            key=lambda x: x["active_objs"] * x["objsize"],
            reverse=True,
        )[:top_n]

        # Update time series data
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

        # Get screen dimensions
        max_y, max_x = stdscr.getmaxyx()
        half_x = max_x // 2  # Divide screen into two columns
        current_line_left = 0
        current_line_right = 0

        try:
            # ----------- Left: Summary Information -----------
            for line in summary_lines:
                if current_line_left >= max_y - 2:
                    break  # Stop if we reach the bottom of the screen
                stdscr.addstr(current_line_left, 0, line[: half_x - 1])
                current_line_left += 1

            slab_header = "{:<10} {:>10} {:>5} {:>10} {:>10} {:>10} {:>15} {:>30}"
            header_text = slab_header.format(
                "OBJS",
                "ACTIVE",
                "USE",
                "OBJ SIZE",
                "SLABS",
                "OBJ/SLAB",
                "CACHE SIZE",
                "NAME",
            )
            if current_line_left < max_y - 2:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(current_line_left, 0, header_text[: half_x - 1])
                stdscr.attroff(curses.color_pair(1))
                current_line_left += 1

            # Slab information display (no background color)
            for slab in slab_data_sorted:
                if current_line_left >= max_y - 2:
                    break  # Stop if we reach the bottom of the screen
                row = "{:<10} {:>10} {:>4}% {:>9} {:>10} {:>10} {:>14} {:>30}"
                row_text = row.format(
                    slab["active_objs"],
                    slab["active_objs"],
                    (
                        (slab["active_objs"] / slab["num_objs"] * 100)
                        if slab["num_objs"] > 0
                        else 0
                    ),
                    format_size(slab["objsize"]),
                    slab["pagesperslab"],
                    slab["objperslab"],
                    format_size(slab["active_objs"] * slab["objsize"]),
                    slab["name"],
                )
                stdscr.addstr(current_line_left, 0, row_text[: half_x - 1])
                current_line_left += 1

            # ----------- Right: Buddy Allocator Information -----------
            buddy_header = "{:<20} {:>10} {:>15}"
            buddy_header_text = buddy_header.format("Node/Zone", "Order", "Free Blocks")
            if current_line_right < max_y - 2:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(
                    current_line_right, half_x, buddy_header_text[: max_x - half_x - 1]
                )
                stdscr.attroff(curses.color_pair(1))
                current_line_right += 1

            for entry in buddy_data:
                if current_line_right >= max_y - 2:
                    break  # Stop if we reach the bottom of the screen
                node_zone = f"Node {entry['node']}/Zone {entry['zone']}"
                stdscr.addstr(
                    current_line_right, half_x, node_zone[: max_x - half_x - 1]
                )
                current_line_right += 1

                # Display free block counts for each order
                for order, count in enumerate(entry["free_counts"]):
                    if current_line_right >= max_y - 2:
                        break
                    buddy_row = "{:<20} {:>10} {:>15}".format("", order, count)
                    stdscr.addstr(
                        current_line_right, half_x, buddy_row[: max_x - half_x - 1]
                    )
                    current_line_right += 1

                # Add an empty line between entries
                if current_line_right < max_y - 2:
                    stdscr.addstr(current_line_right, half_x, "")
                    current_line_right += 1

            if max_y - 1 > 0:
                instruction = "Press 'q' to quit."
                stdscr.attron(curses.color_pair(1))
                # stdscr.addstr(max_y - 1, (max_x - len(instruction)) // 2, instruction)
                stdscr.addstr(max_y - 1, 0, instruction)
                stdscr.attroff(curses.color_pair(1))

            stdscr.refresh()

        except curses.error:
            pass

        # Sleep for the remaining time to maintain the interval
        elapsed_time = time.time() - start_time
        time_to_wait = max(0, interval - elapsed_time)
        try:
            time.sleep(time_to_wait)
        except KeyboardInterrupt:
            break

        # Check for user input
        key = stdscr.getch()
        if key == ord("q"):
            break

    # Generate time series graph
    if args.graph:
        utils.generate_time_series_graph(
            time_series_data, filename=args.filename, top_n=top_n
        )
        print(f"Graph saved to {args.filename}.html")


if __name__ == "__main__":
    main()
