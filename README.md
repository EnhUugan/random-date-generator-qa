# Random Date Generator: QA

I tested the random date generator at https://codebeautify.org/generate-random-date. Only the generator was in scope, not the rest of the site. I tested in Opera GX on Windows 11 on 7 October 2026.

I found 4 bugs. The two most important:
- the page freezes when you ask for 10,000 dates;
- invalid dates like `-1` or `2020-02-30` give wrong results with no error message.

| ID | Title | Severity |
|---|---|---|
| [BUG-01](bugs/BUG-01-page-freezes-on-large-count.md) | Page freezes when count is set to 10,000 | High |
| [BUG-02](bugs/BUG-02-end-date-before-start-date.md) | End date earlier than start date is accepted without a warning | Low |
| [BUG-03](bugs/BUG-03-invalid-dates-accepted.md) | Date boxes accept invalid dates and generate wrong results without an error | Medium |
| [BUG-04](bugs/BUG-04-count-field-accepts-e.md) | Count box accepts the letter "e" and shows an empty result with no message | Low |

The full [test report](test-report.md) covers:
- the types of testing I did;
- all 12 test cases and their results;
- the randomness check;
- what I didn't test.

## What's in this repo

```
README.md          this page
test-report.md     the test report
bugs/              one file per bug
evidence/          screen recordings and screenshots, named after each bug
scripts/           Python scripts for the randomness check, and the 100 dates I tested
```

## Running the randomness check

You only need Python 3. On Mac or Linux, type `python3` instead of `python`.

```
cd scripts
python date_distribution.py sample-100-dates.txt
python uniformity_check.py sample-100-dates.txt
```

- `date_distribution.py` shows how many dates fall in each decade, month and day of the week, with a simple bar chart.
- `uniformity_check.py` runs a chi-square test to check that the spread is even.

To check your own dates, generate them in the default MM-DD-YYYY format and save them with the tool's download button. Then pass the saved file to the scripts. If you changed the date range, add the start and end dates after the file name:

```
python uniformity_check.py my-dates.txt 2000-01-01 2039-12-31
```
