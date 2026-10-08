# BUG-02: End date before start date is accepted with no warning

| | |
|---|---|
| Severity | Low |
| Priority | Low |
| Component | Start date / End date fields |
| Environment | Opera GX 136.0.6008.76, Windows 11 Home, Pacific Time |
| Reproducible | Always |
| Evidence | [screenshot](../evidence/BUG-02-end-date-before-start-date.png), [recording](../evidence/BUG-02-end-date-before-start-date.mp4) |

## Steps to reproduce

1. Open https://codebeautify.org/generate-random-date.
2. Swap the two default dates:
   - Start date `2099-12-31 23:59:59`
   - End date `2020-01-01 00:00:00`
3. Click Generate Random Date.

## Expected result

One of these:
- A message that the end date is before the start date, and no output.
- The range is swapped on purpose, and the user is told about it.

## Actual result

10 dates are generated between 2020 and 2094, with no message. The output looks normal, so the user can't tell that the range they entered was backwards.

![Reversed range output](../evidence/BUG-02-end-date-before-start-date.png)

## Why it happens

The script never compares the two dates. Each date is picked as `start + random * (end - start)`. When the end is earlier than the start, the random offset is negative, so the dates still land between the two values and the output looks fine.

## Why Low

Every generated date is still between the two dates the user typed, so nobody gets wrong data. It's still a bug: the form accepts a backwards range without saying anything, which is exactly the kind of input mistake a form should catch.

## Suggested fix

Check `end >= start` before generating. If it isn't, show "End date must be after start date", or swap the dates and tell the user.
