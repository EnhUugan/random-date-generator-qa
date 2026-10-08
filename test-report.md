# Test Report: Random Date Generator

| | |
|---|---|
| Product | https://codebeautify.org/generate-random-date |
| Tester | Enkh-Uugan |
| Date | 7 October 2026 |
| Build | Live site. Tool script `random-date-generator.js`, last modified 20 April 2026 |

## 1. Summary

With valid dates and the default format, the generator works. Dates land in the chosen range, leap days work, and a 100-date sample showed no sign of bias in a chi-square test.

Input handling is the weak spot. The tool barely validates anything, so bad input gives wrong output (or none), and the user never sees an error. A large count freezes the tab completely.

| Result | Count |
|---|---|
| Test cases run | 12 |
| Passed | 6 |
| Failed | 6 |
| Bugs filed | 4 (1 High, 1 Medium, 2 Low) |

**Recommendation:** fix BUG-01 and BUG-03 before relying on this tool for test data. BUG-02 and BUG-04 are small validation fixes that can ship with them.

## 2. Scope

In scope: the random date generator only. That covers the count field, the start and end date fields, the default output format (MM-DD-YYYY), the Generate button and the randomness of the output.

Out of scope: the rest of codebeautify.org, ads, login and other tools.

## 3. Approach

I tested each input by hand, aiming at the places date tools usually break: invalid dates, leap years, reversed ranges and very large counts. For each field I tried normal values, edge values and things that shouldn't be accepted at all, like `-1` as a date or `e` as a count.

To check randomness, I saved 100 generated dates and wrote two small Python scripts (in `scripts/`). One charts the dates by decade, month and weekday. The other runs a chi-square test to see whether the spread is what a fair generator would give.

The tool runs entirely in the browser, so I also looked at why each bug happens:
- the input attributes in DevTools;
- errors in the Console;
- how the browser reads the values (for example, typing `new Date("-1")` in the Console);
- the page's script itself.

The script is obfuscated, so I resolved its string table to read it. Then I loaded an offline copy of the page (the site's HTML and its own two scripts, with no ads and no network) in headless Chrome 154, and drove the inputs with a small harness to time large counts and to confirm a few things I hadn't hit by hand (section 6). The harness isn't included in this repo.

Evidence (screen recordings and screenshots) is in `evidence/`, named after the bug it shows.

## 4. Environment

| | |
|---|---|
| Browser | Opera GX 136.0.6008.76 (Chromium) |
| OS | Windows 11 Home, build 26200 |
| Hardware | Intel i7-12700KF, 16 GB RAM |
| Time zone | Pacific Time (UTC-7 on the test date) |
| Timing runs | Headless Chrome 154, same machine |

## 5. Test cases

| ID | Test | Input | Expected | Actual | Result |
|---|---|---|---|---|---|
| TC-01 | Default generation | Defaults (10 dates, 2020-01-01 to 2099-12-31) | 10 dates in range | 10 dates in range | Pass |
| TC-02 | Count 100 | Count `100` | 100 valid dates in range | 100 valid dates, 2020-02-08 to 2099-07-12, no duplicates | Pass |
| TC-03 | Count 1,000 / 2,000 / 5,000 | Count `1000`, `2000`, `5000` | That many dates, page stays usable | Works | Pass |
| TC-04 | Count 10,000 | Count `10000` | 10,000 dates, or a clear limit | Page freezes, output disappears, refresh doesn't help, never recovers | **Fail: BUG-01** |
| TC-05 | Leap day | Range covering 29 Feb 2020 | 02-29-2020 generated as a valid date | 02-29-2020 generated correctly | Pass |
| TC-06 | Even distribution | The 100 dates from TC-02 | No bias by decade, month or weekday | Chi-square passes on all three (see 5.1) | Pass |
| TC-07 | Reversed range | Start `2099-12-31 23:59:59`, end `2020-01-01 00:00:00` | Error message | Dates generated, no warning | **Fail: BUG-02** |
| TC-08 | Number as a date | Start `-1`, end `-2` | Error message | 10 dates in January 2001 | **Fail: BUG-03** |
| TC-09 | Same number in both boxes | Start and end `1` (also `-1`) | Error message | `01-01-2001` on every line | **Fail: BUG-03** |
| TC-10 | Impossible date | Start and end `2020-02-30 00:00:00` | Error message | `03-01-2020` on every line | **Fail: BUG-03** |
| TC-11 | Letters in count | Count `e` / `E` | Rejected, or a message | Output cleared, no message | **Fail: BUG-04** |
| TC-12 | Exponent in count | Count `1e2` | 100 dates (`1e2` is valid number syntax) | 100 dates | Pass |

### 5.1 Distribution check (TC-06)

I took 100 dates over the default range (2020 to 2099). For each group, the expected count is based on how many days that group has in the range, so it isn't simply an equal split.

| Grouping | Chi-square | 5% limit | Result |
|---|---|---|---|
| Decade | 8.16 | 14.07 | Pass |
| Month | 16.70 | 19.68 | Pass |
| Weekday | 2.76 | 12.59 | Pass |

100 dates is a small sample, so this only rules out obvious bias. To rerun it, see the README.

## 6. Other issues found in code review

I found these by reading the page's script, and confirmed them by running that script in headless Chrome. I haven't checked them by hand on the live page yet, so they aren't filed as bugs. They're the next things to test.

| # | Issue | How to see it |
|---|---|---|
| 1 | An invalid date leaves the old output on screen. The tool's own error handling crashes with a `TypeError`, so no message appears and the previous results stay as if they matched the new input. | Generate once, then select all the text in the start date box and type `abc`. The old dates stay, and the Console shows the error. |
| 2 | Custom format garbles month names. Each token is replaced once in a fixed order, so letters inside month names get replaced too. | Set start and end to `2020-03-05 13:07:09` and use the custom format `month DD, YYYY`. You get `Marc13 05, 2020` instead of `March 05, 2020`. With random dates, other months break too, for example `Augu45t` or `Dece19ber`. |
| 3 | "Year Date Month" prints Year Month Date. Both options run the same code. | Same start and end, format Year Date Month. You get `2020 March 05 13:07:09` instead of `2020 05 March 13:07:09`. |
| 4 | A count of 0, a negative count or a decimal is accepted with no message. | `0` and `-5` clear the output. `2.5` gives 3 dates and a blank line. |
| 5 | The output box placeholder says "Generated Random Integer", and the field labels aren't linked to their inputs, so screen readers can't name the fields. | Inspect the page. |

## 7. Not tested

Roughly in priority order:

- **Other output formats and the custom format tokens.** I only used MM-DD-YYYY. ISO 8601 prints in UTC while every other format uses local time. That's technically correct, but users may not expect it.
- **Copy and Download:** the contents, the line count and the file name.
- **Other browsers.** Date parsing differs between browsers. The page says it supports Firefox and Safari, but I only tested Chromium-based browsers.
- **Time zones and daylight saving.** Date-only input like `2020-02-30` is read as UTC, so the result can shift by a day depending on where you are.
- **Mobile layout, keyboard-only use and screen readers.**
- **Larger samples** for the distribution check (10,000+ dates, including hours and minutes).

## 8. Bugs

| ID | Title | Severity |
|---|---|---|
| [BUG-01](bugs/BUG-01-page-freezes-on-large-count.md) | Page freezes at a count of 10,000 and never recovers | High |
| [BUG-02](bugs/BUG-02-end-date-before-start-date.md) | End date before start date is accepted with no warning | Low |
| [BUG-03](bugs/BUG-03-invalid-dates-accepted.md) | Date boxes accept invalid values and output wrong dates silently | Medium |
| [BUG-04](bugs/BUG-04-count-field-accepts-e.md) | Count box accepts `e` and clears the output with no message | Low |

Severity:
- **High:** the page becomes unusable or data is lost.
- **Medium:** wrong output with no warning.
- **Low:** a validation or usability gap where the output is still usable.
