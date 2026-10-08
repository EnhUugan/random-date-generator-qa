# Test Report: Random Date Generator

| | |
|---|---|
| Product | https://codebeautify.org/generate-random-date |
| Tester | Enkh-Uugan |
| Date | 7 October 2026 |

## 1. Summary

With normal input, the generator works. Dates come out inside the chosen range, leap days are handled, and a sample of 100 dates was spread evenly.

The problems are all about input. The tool barely checks what you type: invalid dates, a reversed range or a letter in the count box all give wrong or empty results, and no error message ever appears. A large count freezes the page completely.

| | |
|---|---|
| Test cases run | 12 |
| Passed | 6 |
| Failed | 6 |
| Bugs found | 4 (1 High, 1 Medium, 2 Low) |

**Recommendation:** fix BUG-01 (the freeze) and BUG-03 (invalid dates) first, since those either break the page or give the user wrong data without warning. BUG-02 and BUG-04 are small input checks that can be fixed at the same time.

## 2. What I tested

**In scope:** the random date generator only:
- the "How many dates to generate?" box;
- the start date and end date boxes;
- the default output format (MM-DD-YYYY);
- the Generate Random Date button;
- how random the generated dates are.

**Out of scope:** the rest of the codebeautify.org website.

## 3. Types of testing

| Type | What it means | What I did |
|---|---|---|
| Functional testing | Does the tool do its main job? | Generated dates with the default settings and checked they were valid and inside the range. |
| Boundary testing | What happens at the edges? | Raised the count step by step (10, 100, 1,000, 2,000, 5,000, 10,000). Checked the leap day, 29 February 2020. |
| Negative testing | What happens with wrong input? | Typed things that shouldn't be accepted: `-1` and `1` as dates, 30 February, an end date before the start date, and the letter `e` as a count. |
| Performance testing | Does it cope with a heavy load? | Kept raising the count until the page broke at 10,000. |
| Randomness testing | Are the dates really random and evenly spread? | Saved 100 generated dates and checked them with a Python script I wrote (see section 6). |
| Exploratory testing | Free testing, following anything that looks odd | When a result looked strange, I tried more inputs around it to understand the pattern. |

I recorded the screen for each bug and took screenshots. They're in the `evidence` folder, named after the bug they show.

## 4. Test environment

| | |
|---|---|
| Browser | Opera GX 136.0.6008.76 |
| Operating system | Windows 11 Home |
| Device | Desktop PC (Intel i7-12700KF, 16 GB RAM) |
| Time zone | Pacific Time |

## 5. Test cases

| ID | Test | Input | Expected | Actual | Result |
|---|---|---|---|---|---|
| TC-01 | Default settings | Count 10, range 2020-01-01 to 2099-12-31 | 10 valid dates in range | 10 valid dates in range | Pass |
| TC-02 | 100 dates | Count `100` | 100 valid dates in range | 100 valid dates in range, no duplicates | Pass |
| TC-03 | Bigger counts | Count `1000`, `2000`, `5000` | That many dates, page keeps working | Worked | Pass |
| TC-04 | Very big count | Count `10000` | 10,000 dates, or a message with the limit | Page froze and never recovered | **Fail: BUG-01** |
| TC-05 | Leap day | Range that includes 29 Feb 2020 | 02-29-2020 can be generated | 02-29-2020 was generated | Pass |
| TC-06 | Even spread | The 100 dates from TC-02 | No obvious bias | Evenly spread (see section 6) | Pass |
| TC-07 | End date before start date | Start `2099-12-31 23:59:59`, end `2020-01-01 00:00:00` | Error message | Dates generated, no message | **Fail: BUG-02** |
| TC-08 | Numbers as dates | Start `-1`, end `-2` | Error message | 10 dates from January 2001 | **Fail: BUG-03** |
| TC-09 | Same number in both date boxes | Start and end `1` (also `-1`) | Error message | `01-01-2001` on every line | **Fail: BUG-03** |
| TC-10 | Date that doesn't exist | Start and end `2020-02-30 00:00:00` | Error message | `03-01-2020` on every line | **Fail: BUG-03** |
| TC-11 | Letter in count | Count `e` (also `E`) | Blocked, or a message | Empty output, no message | **Fail: BUG-04** |
| TC-12 | Exponent number in count | Count `1e2` | 100 dates (`1e2` means 100) | 100 dates | Pass |

## 6. Randomness check

I saved 100 dates the tool generated (default range, 2020 to 2099). I wrote a small Python script that counts them by decade, month and day of the week.

If the tool is fair, every group should get roughly its share, and no decade, month or weekday should get far more or far fewer than the others. That's what I found. To be sure the differences were just normal randomness, I also ran a chi-square test, a standard statistics test for exactly this question. All three groupings passed.

| Grouped by | Test score | Pass limit | Result |
|---|---|---|---|
| Decade | 8.16 | 14.07 | Pass |
| Month | 16.70 | 19.68 | Pass |
| Weekday | 2.76 | 12.59 | Pass |

A lower score means a more even spread. 100 dates is a small sample, so this can only catch obvious problems. The scripts and the sample are in the `scripts` folder, and the README explains how to run them.

## 7. Bugs found

| ID | Title | Severity |
|---|---|---|
| [BUG-01](bugs/BUG-01-page-freezes-on-large-count.md) | Page freezes when count is set to 10,000 | High |
| [BUG-02](bugs/BUG-02-end-date-before-start-date.md) | End date earlier than start date is accepted without a warning | Low |
| [BUG-03](bugs/BUG-03-invalid-dates-accepted.md) | Date boxes accept invalid dates and generate wrong results without an error | Medium |
| [BUG-04](bugs/BUG-04-count-field-accepts-e.md) | Count box accepts the letter "e" and shows an empty result with no message | Low |

**How I rated severity:**
- **High:** the page becomes unusable or data is lost.
- **Medium:** the tool gives wrong results without any warning.
- **Low:** an input check is missing, but the result is still usable.

Smaller observation: the empty output box shows "Generated Random Integer" as its placeholder text, which looks like it was copied from another tool.

## 8. Not tested, and next steps

I left these out, mainly for time. They'd be next:
- **The other output formats and the custom date format.** I only used MM-DD-YYYY.
- **The Copy and Download buttons.**
- **Other browsers.** I only tested Opera GX, and the page says it supports Chrome, Firefox, Edge and Safari. Browsers can read dates differently, so BUG-03 might behave differently in them.
- **Phones and tablets.**
- **Accessibility:** using the page with only a keyboard, or with a screen reader.
- **The exact count where BUG-01 starts.** It's somewhere between 5,000 and 10,000.
- **A larger randomness sample**, for example 10,000 dates.
