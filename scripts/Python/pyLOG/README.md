# 🔍 pyLOG - Log Parser & Analyzer

A Python utility designed for log analysis and system auditing. The script accepts a target file and a search keyword via the command line, securely parses massive text files to extract matching lines, and optionally generates a structured `.json` report with audit metadata.

This project is part of the **Automation, Networking, and Python Scripting** module of my Cybersecurity Roadmap.

---

## ⚡ Features

- **Memory Management:** Utilizes `with open` context managers to process extensive log files sequentially, optimizing system RAM usage.
- **Precise Search (Regex):** Implements automatic string escaping via `re.escape`, allowing exact searches for IP addresses, directory paths, and URLs without breaking regular expressions.
- **Interactive JSON Export:** Prompts the user to optionally export results into a structured `.json` artifact containing audit metadata, keeping the directory clean during quick reconnaissance.
- **System Exception Handling:** Manages common OS exceptions like missing files (`FileNotFoundError`) and permission denials (`PermissionError`), preventing abrupt script crashes.

---

## ⚙️ Prerequisites

- Python 3.8+
- No external dependencies required (uses built-in `re`, `os`, `sys`, `json`, `datetime`).

Make the script executable:

```bash
chmod +x pyLOG.py
./pyLOG.py <file_path> '<keyword>'
