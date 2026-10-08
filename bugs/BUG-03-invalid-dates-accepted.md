# BUG-03: Date boxes accept invalid values and output wrong dates silently

| | |
|---|---|
| Severity | Medium |
| Priority | Medium |
| Component | Start date / End date fields |
| Environment | Opera GX 136.0.6008.76, Windows 11 Home, Pacific Time |
| Reproducible | Always |
| Evidence | [screenshot](../evidence/BUG-03-invalid-dates-accepted.png), [recording](../evidence/BUG-03-invalid-dates-accepted.mp4) |

## Steps to reproduce

Open https://codebeautify.org/generate-random-date. Keep the count at 10 and the format at MM-DD-YYYY, then try each row:

| # | Start date | End date | What you get |
|---|---|---|---|
| A | `-1` | `-2` | 10 dates in January 2001 |
| B | `1` (or `-1`) | `1` (or `-1`) | `01-01-2001` on every line |
| C | `2020-02-30 00:00:00` | `2020-02-30 00:00:00` | `03-01-2020` on every line |

## Expected result

A validation error such as "Please enter a valid date (YYYY-MM-DD hh:mm:ss)", and no output. `-1` and `1` aren't dates, and February has no 30th.

## Actual result

Dates are generated every time, and no message appears.

![Start -1, end -2 gives January 2001](../evidence/BUG-03-invalid-dates-accepted.png)

The output looks believable. Someone who made a typo gets a full list of "random" dates from the wrong year and never finds out.

## Why it happens

The date boxes are plain text fields with no format check. The script passes the text straight to `new Date(text)` and takes whatever the browser makes of it. You can see what the browser does by typing `new Date("-1")` in the DevTools Console. I tested in Opera GX and confirmed the same results in Chrome; Edge uses the same engine.

The browser's rules explain each case:
- A lone number from 1 to 12 is read as a month in 2001, and the minus sign is dropped. `1` and `-1` both become 1 January 2001, and `-2` becomes 1 February 2001. That's case A: the range runs from 1 January to 1 February 2001.
- When both boxes hold the same value, the range is a single instant, so case B prints the same date 10 times.
- Any day from 1 to 31 is accepted for any month, and the extra days roll over. 30 February becomes 1 March, and 31 April becomes 1 May. Day 0, day 32+, month 0 and month 13+ are rejected.
- A date typed without a time is read as UTC. On its own, `2020-02-30` becomes 1 March 00:00 UTC, which is 29 February at 4 PM in Pacific Time. The same input gives a different day depending on where you are.

The script does try to handle dates it can't read, but that code is broken too. It calls `this.output.showWarningBadge(...)`, but `this.output` doesn't exist on this page, so it throws `TypeError: Cannot read properties of undefined (reading 'showWarningBadge')` before writing anything. In my offline run of the site's script, no message appeared and the previous output stayed on screen. I haven't confirmed that on the live page yet. See section 6 of the [test report](../test-report.md#6-other-issues-found-in-code-review).

## Suggested fix

- Check both boxes against one format, for example `YYYY-MM-DD hh:mm:ss`, and reject dates that don't exist. One way to do that: build the date, then check that the day and month didn't change.
- Or use `<input type="datetime-local">`, which only lets the user pick real dates.
- Fix the error handling so bad input shows a message and clears the output.
