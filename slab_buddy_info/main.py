import argparse
import time
from .slabinfo_parser import parse_slabinfo
from .buddyinfo_parser import parse_buddyinfo
from .utils import display_slabinfo, display_buddyinfo, text_bar_graph


def main():
    parser = argparse.ArgumentParser(
        description="Display Linux kernel slab and buddy allocator information."
    )
    parser.add_argument(
        "--interval", type=int, default=0, help="リアルタイム監視の更新間隔（秒）"
    )
    parser.add_argument(
        "--graph", action="store_true", help="テキストベースのグラフ表示を有効にする"
    )
    parser.add_argument(
        "--top", type=int, default=10, help="グラフ表示する上位N件のslabを指定"
    )
    parser.add_argument(
        "--show-slab", action="store_true", help="slabアロケータ情報のみを表示"
    )
    parser.add_argument(
        "--show-buddy", action="store_true", help="buddyアロケータ情報のみを表示"
    )
    args = parser.parse_args()

    if not args.show_slab and not args.show_buddy:
        # どちらも指定されていない場合、両方を表示
        args.show_slab = True
        args.show_buddy = True

    try:
        while True:
            if args.show_slab:
                slab_data = parse_slabinfo()
                print("\n=== Slab Allocator Information ===")
                display_slabinfo(slab_data)

                if args.graph:
                    print("\nSlab Usage Graph:")
                    sorted_slab = sorted(
                        slab_data,
                        key=lambda x: x["active_objs"] * x["objsize"],
                        reverse=True,
                    )[: args.top]
                    labels = [slab["name"] for slab in sorted_slab]
                    values = [
                        slab["active_objs"] * slab["objsize"] for slab in sorted_slab
                    ]
                    text_bar_graph(labels, values)

            if args.show_buddy:
                buddy_data = parse_buddyinfo()
                print("\n=== Buddy Allocator Information ===")
                display_buddyinfo(buddy_data)

            if args.interval <= 0:
                break
            else:
                time.sleep(args.interval)
                print("\033[H\033[J", end="")  # 画面をクリア

    except KeyboardInterrupt:
        print("終了します...")


if __name__ == "__main__":
    main()
