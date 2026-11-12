# Authentication Log Analyzer

Detect bursts of failed logins and successful logins after a failure burst in offline JSONL logs.

Educational cybersecurity portfolio project. Built with AI assistance and supplied with synthetic fixtures and automated tests. It is a learning implementation, not a production security product.

## Quick start

Requires Python 3.11 or newer. Uses only the Python standard library; no pip installation or network access is needed.

From this repository's directory:

```console
python main.py samples/events.jsonl --threshold 3 --window 60
```

On Windows, use `py` in place of `python` if that is your installed launcher. Output is JSON on stdout. To save it, append `> report.json` in your terminal. Paths are relative to your current working directory.

## How it works

Group failures by (IP, user), maintain a sliding deque, emit one burst alert when the threshold is crossed, then flag a success while the burst is still in the time window. Sorting costs O(n log n); the scan is O(n).

## Input and example

The `samples/` directory contains the complete minimal input schema and fictional data. The checked `samples/expected-output.json` records the output of the quick-start command (for the integrity monitor, the final check command).

## Tests

```console
python -m unittest discover -s tests -v
```

Tests cover core behavior, boundary cases and invalid input. GitHub Actions is configured to run them on Windows and Ubuntu with Python 3.11–3.13; see the Actions tab for actual remote results.

## Limitations

Synthetic JSONL schema only; no syslog parser, distributed password-spray detection, or account lockout. A burst is a lead for investigation, not proof of compromise.

Successful analysis exits 0 unless stated otherwise above; command/input errors exit 2. Findings are not automatically remediated. Only use data you are authorized to analyze. Do not commit real credentials, customer logs or personal data.

## Learning notes

See [LEARNING_RU.md](LEARNING_RU.md) for an exercise and interview questions. Explain the algorithm, run the demo and implement an extension before presenting this as a skill you can use independently.
