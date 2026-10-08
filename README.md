# Random Date Generator: QA

I tested the random date generator at https://codebeautify.org/generate-random-date, and only the generator, not the rest of the site. Testing was done in Opera GX 136 on Windows 11 on 7 October 2026.

I found 4 bugs. The two that matter most:
- a count of 10,000 froze the page, and it never recovered, even after a refresh;
- invalid dates like `-1` or `2020-02-30` give wrong output with no error.

| ID | Title | Severity |
|---|---|---|
| [BUG-01](bugs/BUG-01-page-freezes-on-large-count.md) | Page freezes at a count of 10,000 and never recovers | High |
| [BUG-02](bugs/BUG-02-end-date-before-start-date.md) | End date before start date is accepted with no warning | Low |
| [BUG-03](bugs/BUG-03-invalid-dates-accepted.md) | Date boxes accept invalid values and output wrong dates silently | Medium |
| [BUG-04](bugs/BUG-04-count-field-accepts-e.md) | Count box accepts `e` and clears the output with no message | Low |

The full report is in [test-report.md](test-report.md). It has every test case, the distribution check, a few issues found by reading the page's code, and what I didn't test.

## Repo layout

```
README.md              this file
test-report.md         test report
bugs/                  one file per bug
evidence/              screen recordings and screenshots, named after the bug they belong to
scripts/               two distribution check scripts + the 100-date sample they were run on
```

## Running the distribution check

You need Python 3 and nothing else. On macOS or Linux, use `python3` instead of `python`.

```
cd scripts
python date_distribution.py sample-100-dates.txt
python uniformity_check.py sample-100-dates.txt
```

`date_distribution.py` prints counts and bars by decade, month and weekday. `uniformity_check.py` runs a chi-square test to see whether those counts are what a fair generator would produce.

To check your own output, keep the tool's default MM-DD-YYYY format and save the dates with its download button. If you changed the date range, put the start and end after the file name:

```
python uniformity_check.py my-dates.txt 2000-01-01 2039-12-31
```
