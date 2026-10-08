# BUG-01: Page freezes at a count of 10,000 and never recovers

| | |
|---|---|
| Severity | High |
| Priority | High |
| Component | "How many dates to generate?" field |
| Environment | Opera GX 136.0.6008.76, Windows 11 Home, Pacific Time. Hardware: i7-12700KF, 16 GB RAM |
| Reproducible | Yes, at 10,000 on the test machine (see recording). In offline timing runs, larger counts like 1,000,000 block the page every time. |
| Evidence | [BUG-01-page-freezes-on-large-count.mp4](../evidence/BUG-01-page-freezes-on-large-count.mp4) |

## Steps to reproduce

1. Open https://codebeautify.org/generate-random-date.
2. In "How many dates to generate?", enter `10`, then `100`, then `1000`. The output updates each time.
3. Change the count to `10000`.

## Expected result

One of these:
- 10,000 dates are generated and the page stays usable.
- The tool shows a clear maximum and doesn't accept counts above it.

## Actual result

- 10, 100 and 1,000 work. 2,000 and 5,000 were tested separately and also worked.
- At 10,000 the page slows down and then freezes. Nothing can be clicked, and the dates that were already in the output box disappear.
- Refreshing doesn't help. The page never recovered.

## Why it happens

- The count has no limit. The field is `<input type="number" id="count">` with no `min` or `max` (visible in DevTools > Elements), and the script loops as many times as the number says.
- All the dates are built and written into the output box in one go, on the page's main thread. Until that finishes, the browser can't respond to clicks, scrolling or refresh.
- The field has `oninput="generateRandomDate();"`, so the tool regenerates on every keystroke. Typing `10000` runs it 5 times: for 1, 10, 100, 1,000 and 10,000.

I timed the site's own script in headless Chrome on the same machine, without ads or extensions:

| Count | Time to generate and lay out (headless, no ads) |
|---|---|
| 10,000 | about 45 ms |
| 100,000 | about 0.5 s |
| 1,000,000 | about 5 to 8 s |
| `1e7` (10 million) | still running after 4 minutes |

So the script alone doesn't explain the freeze I saw at 10,000. The cause on the live page is still open. It could be the ads, a browser extension or something in Opera GX. Next step: repeat in a private window with extensions off and record a DevTools Performance trace. Either way the core problem holds: with no limit and all the work on the main thread, a big enough number always hangs the page. With BUG-04 that takes three characters: `1e7`.

## Suggested fix

- Set a maximum count (for example 5,000, the largest count that worked for me, until the freeze is understood) in both the input (`max`) and the script, and show a message when it's exceeded.
- Build the output in chunks or in a Web Worker so the page stays responsive.
- Generate only when the button is clicked, not on every keystroke.

## Related

[BUG-04](BUG-04-count-field-accepts-e.md): exponent values like `1e7` make huge counts easy to enter by accident.
