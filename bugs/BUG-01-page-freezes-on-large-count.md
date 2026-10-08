# BUG-01: Page freezes when count is set to 10,000

- **Severity: High.** The page stops responding completely, and the dates already on screen are lost.
- **Priority: High.** Any user can hit this by typing a number that looks perfectly reasonable.

## Environment

- Page: https://codebeautify.org/generate-random-date
- Browser: Opera GX 136.0.6008.76
- OS: Windows 11 Home
- Device: Desktop PC (Intel i7-12700KF, 16 GB RAM)
- Date tested: 7 October 2026

## Preconditions

Page freshly loaded, all settings at default.

## Steps to reproduce

1. Click the "How many dates to generate?" box and change `10` to `100`.
2. Change it to `1000`.
3. Change it to `10000`.
4. Try to click anything on the page.
5. Refresh the page.

## Expected result

The tool generates 10,000 dates and the page stays usable. If 10,000 is too many, the tool should show a message with the maximum it allows.

## Actual result

- With 100 and 1,000, the dates were generated normally.
- With 10,000, the page slowed down and then froze.
- Nothing on the page could be clicked.
- The dates that were already in the output box disappeared.
- Refreshing didn't help, and the page never recovered.

## Evidence

Video: [BUG-01-page-freezes-on-large-count.mp4](../evidence/BUG-01-page-freezes-on-large-count.mp4)

## Reproducibility

Happened in the recorded test (see video).

## Notes

- **Boundary:** 2,000 and 5,000 also worked, in a separate run. The problem appears somewhere between 5,000 and 10,000. I didn't narrow down the exact number.
- **Suspected cause:** the count box has no maximum, and the tool seems to build every date in one go. While it does that, the browser can't respond to anything else.
- **Workaround:** keep the count at 5,000 or below. If the page freezes, close the tab and open the page again.
- **Suggested fix:** set a maximum count and show a message when someone goes over it.
- **Related:** [BUG-04](BUG-04-count-field-accepts-e.md). The count box accepts exponent numbers like `1e2`, which makes a huge count easy to type by accident.
