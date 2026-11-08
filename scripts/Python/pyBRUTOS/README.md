# 🔓 pyBRUTOS - SSH Authentication Auditor

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Roadmap-Cybersecurity-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A Python utility designed for auditing SSH service security through dictionary-based brute-force attacks. Built with the `paramiko` library, this script automates the process of testing credentials against a target SSH server to identify weak or compromised passwords.

This project is part of the **Automation, Networking, and Python Scripting** module of my Cybersecurity Roadmap.

---

## ⚡ Features

- **Automated Protocol Handling:** Utilizes `paramiko` to seamlessly manage SSH connection negotiation, host key acceptance (`AutoAddPolicy`), and authentication routines without interactive prompts.
- **CLI Argument Parsing:** Implements `argparse` for structured and intuitive command-line inputs, validating required parameters before execution.
- **Exception Management:** Natively handles network exceptions such as `socket.timeout`, `socket.error`, and `AuthenticationException` to ensure the script does not crash abruptly during unreachable host scenarios.
- **Rate Limiting / Evasion:** Incorporates a programmed delay (`time.sleep`) between connection attempts to mitigate the risk of triggering immediate IP blocks from basic defense mechanisms like Fail2Ban.

---

## ⚙️ Prerequisites

- Python 3.8+
- `paramiko` library

Install dependencies:

```bash
pip3 install paramiko --break-system-packages

## 🚀 Usage
python3 pyBRUTOS.py <HOST> <PORT> <USERNAME> <WORDLIST_PATH>

⚠️ Disclaimer
This tool was developed strictly for educational purposes and authorized penetration testing within the scope of my cybersecurity studies.
Always ensure you have explicit permission before auditing or testing any network infrastructure.
