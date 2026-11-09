# 🐍 Python Security & Automation Tools

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Module-Offensive_&_Defensive-red?style=for-the-badge)

Welcome to the **Python Security Tools** directory of my 12-Month Cybersecurity Roadmap. 

This module contains a collection of custom Python scripts developed to automate routine security tasks, parse system logs, and perform network auditing. The focus here is on building lightweight, portable tools that rely heavily on native Python libraries, optimizing execution for environments like Linux, Kali, and Termux.

---

## 🧰 Tools Index

Below is the current list of utilities available in this module. *(Refer to each script's individual README or source code for detailed usage instructions and specific dependencies).*

### 1. [🔍 pyLOG (Log Parser & Analyzer)](/pyLOG)
A command-line utility designed to securely parse massive text files (e.g., `auth.log`, `access.log`). It leverages Regular Expressions (Regex) to find exact keyword matches (like IPs or system errors) and optionally exports structured `.json` audit reports.

### 2. [🔓 pyBRUTOS (SSH Authentication Auditor)](/pyBRUTOS)
A dictionary-based SSH auditing script built with the `paramiko` library. Designed to automate credential testing against target servers, featuring automated protocol handling, network exception management, and rate-limiting evasion delays.

### 3. [📥 pyDOWN (Python File Downloader)](/pyDOWN)
A web request automation script that validates target URLs and sanitizes file extensions via Regex. It downloads specific files (such as `.pdf` and `.txt`) using optimized memory streaming chunks via the `requests` library.

---

## ⚠️ Warning / Safe Harbor

**For Educational and Authorized Testing Purposes Only.**

The scripts contained in this directory are developed strictly for academic research, malware analysis studies, and authorized penetration testing. 
You must have explicit, written permission from the system owner before running any auditing or enumeration tools against a network infrastructure. 
The author is not responsible for any misuse, damage, or legal consequences caused by these scripts.
