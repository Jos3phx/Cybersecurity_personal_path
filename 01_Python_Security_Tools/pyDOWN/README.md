# 📥 Python File Downloader (PDF & TXT)

A Python utility designed for input validation and web request automation. The script accepts a URL via the command line, validates the syntax and file extension using **Regular Expressions (Regex)**, and downloads `.pdf` and `.txt` files using memory streaming.

This project is part of the **Automation, Networking, and Python Scripting** module of my Cybersecurity Roadmap.

---

## ⚡ Features

- **Syntax Validation (Regex):** Validates URL structure (supports `http`, `https`, `ftp`, `ftps`, domain names, IP addresses, and `localhost`).
- **Extension Sanitization:** Filters requests to strictly allow files with `.pdf` or `.txt` extensions.
- **Streamed Download:** Utilizes `stream=True` from the `requests` library to download files in 8 KB chunks, optimizing RAM usage.
- **Network Exception Handling:** Manages connection failures, timeouts, missing schemes, and HTTP status errors (`4xx` and `5xx`).

---

## ⚙️ Prerequisites

- Python 3.8+
- `requests` library

Install dependencies:

```bash
pip install requests
