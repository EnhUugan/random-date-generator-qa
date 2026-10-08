# BUG-04: Count box accepts `e` and clears the output with no message

| | |
|---|---|
| Severity | Low |
| Priority | Medium (it makes BUG-01 easy to trigger) |
| Component | "How many dates to generate?" field |
| Environment | Opera GX 136.0.6008.76, Windows 11 Home, Pacific Time |
| Reproducible | Always |
| Evidence | None recorded yet |

## Steps to reproduce

1. Open https://codebeautify.org/generate-random-date.
2. Clear "How many dates to generate?" and type `e` (or `E`).

## Expected result

The value is rejected, or a message says what's allowed, for example "Enter a whole number from 1 to 5,000".

## Actual result

The output box goes empty and nothing explains why.

## Why it happens

The field is `<input type="number">` with no `min`, `max` or `step`. Chromium browsers block other letters in a number field but allow `e`, `E`, `+`, `-` and `.`, because exponents like `1e2` are valid number syntax. So that part is normal browser behaviour. What's wrong is that the site never checks the value it gets:

- While the box holds something that isn't a complete number, such as `e` on its own, the browser reports the value as empty. The script turns that into 0, generates zero dates and clears the output without a message.
- When the box holds a complete exponent, the script just uses it. `1e2` gives 100 dates. `1e7` asks for 10 million. In my offline run of the site's script, that was still running after 4 minutes (BUG-01). I haven't tried `1e7` on the live page.

## Suggested fix

- Add `min="1"`, `step="1"` and a `max` (whatever limit BUG-01 settles on) to the input.
- In the script, check that the value is a whole number in range. If it isn't, show a message instead of clearing the output.

## Related

[BUG-01](BUG-01-page-freezes-on-large-count.md): page freezes on large counts.
