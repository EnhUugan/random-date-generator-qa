import sys
from collections import Counter
from datetime import date, datetime, timedelta

if len(sys.argv) < 2:
    sys.exit("usage: python uniformity_check.py dates.txt [start end]")

# Tool default range. Pass start/end (YYYY-MM-DD) as extra arguments if you changed it.
start = date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else date(2020, 1, 1)
end = date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else date(2099, 12, 31)

# Chi-square critical values at 5%, by degrees of freedom
CRITICAL = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07, 6: 12.59, 7: 14.07, 8: 15.51, 9: 16.92, 10: 18.31, 11: 19.68}

with open(sys.argv[1]) as f:
    dates = [datetime.strptime(line.strip(), "%m-%d-%Y").date() for line in f if line.strip()]
every_day = [start + timedelta(n) for n in range((end - start).days + 1)]


def check(title, key):
    observed = Counter(key(d) for d in dates)
    days = Counter(key(d) for d in every_day)
    chi2 = sum((observed[k] - len(dates) * n / len(every_day)) ** 2 / (len(dates) * n / len(every_day)) for k, n in days.items())
    df = len(days) - 1
    if df not in CRITICAL:
        print(f"{title:<8} skipped ({len(days)} groups, need 2 to 12)")
        return
    verdict = "PASS" if chi2 < CRITICAL[df] else "FAIL"
    print(f"{title:<8} chi2 = {chi2:5.2f}  (5% limit {CRITICAL[df]}, df {df})  {verdict}")


print(f"{len(dates)} dates, expected range {start} to {end}")
check("Decade", lambda d: d.year // 10)
check("Month", lambda d: d.month)
check("Weekday", lambda d: d.weekday())
