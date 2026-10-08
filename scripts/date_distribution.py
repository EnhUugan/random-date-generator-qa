import sys
from collections import Counter
from datetime import datetime

path = sys.argv[1] if len(sys.argv) > 1 else input("Path to .txt file: ").strip('" ')
with open(path) as f:
    dates = [datetime.strptime(line.strip(), "%m-%d-%Y") for line in f if line.strip()]


def show(title, counts):
    print(f"\n{title}")
    top = max(counts.values())
    for label, n in counts.items():
        print(f"  {label:<6} {'#' * round(20 * n / top):<20} {n} ({n / len(dates):.0%})")


print(f"Total: {len(dates)}  |  {min(dates):%m-%d-%Y} to {max(dates):%m-%d-%Y}")
show("By decade", Counter(f"{d.year // 10 * 10}s" for d in sorted(dates)))
show("By month", Counter(d.strftime("%b") for d in sorted(dates, key=lambda d: d.month)))
show("By weekday", Counter(d.strftime("%a") for d in sorted(dates, key=lambda d: d.weekday())))
