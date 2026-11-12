# Cybersecurity_personal_path

My personal repository for studies and research in cybersecurity, focusing on networks (physical & wireless), infrastructure, SDR, telecommunications, and everything related to security testing within these environments.

# 🛡️ Personal Cybersecurity & Infrastructure Path (12 Months)

![Status](https://img.shields.io/badge/Status-In_Progress-brightgreen)
![Focus](https://img.shields.io/badge/Focus-Offensive_Sec_%7C_Networks_%7C_RF_%7C_Low_Level-red)
![License](https://img.shields.io/badge/License-MIT-blue)

Personal repository dedicated to documenting practical research, automation scripts, exploit development, spectrum analysis, and hands-on labs for a 12-month study roadmap focused on **Network Security (physical & wireless), Infrastructure, Telecom, and Low-Level Engineering**, with IoT/OT-ICS covered as a complementary module.

This path is self-directed and shaped by prior formal training (see below), so several months are framed as **hands-on validation** of concepts already studied, not first-time learning. Months are organizational, not fixed deadlines.

---

## 🎓 Prior Training

- **Pentester Jr / Pentest Professional Training (Desec Security)** — full methodology track: security fundamentals, networking & protocols, scripting, end-to-end pentest process (recon → exploitation → professional reporting).
- **Cisco Networking Academy:** CCNA 1, Network Security, CyberOps Associate, Ethical Hacker.

---

## 📅 12-Month Roadmap & Milestones

### 1st Quarter: Programming & Practical Validation (Networks, SecOps, Pentest Methodology)

| Month | Topics & Technologies | Practical Milestone |
|---|---|---|
| **Month 01** | **Programming & Automation:** Python (Sockets, raw packet parsing, Scapy, Impacket), Bash (Pipes, Grep, Awk, Sed, Xargs), SQL fundamentals. | Automated network recon script + packet sniffer built from raw sockets. |
| **Month 02** | **Networks & SecOps — Practical Validation:** TCP/IP, Wireshark, Scapy, pfSense, Suricata, Wazuh, VLAN segmentation. *(Builds on CCNA 1 / Network Security / CyberOps Associate.)* | Self-built lab topology with working firewall, IDS/IPS and SIEM, documented from scratch. |
| **Month 03** | **Pentest Methodology — Practical Validation:** Recon, enumeration, privilege escalation (Linux/Windows), professional reporting. *(Builds on Desec Pentest Professional.)* | 3-5 HTB/THM machines with full reports, published as write-ups. |

### 2nd Quarter: Active Directory, Network Services & Wireless

| Month | Topics & Technologies | Practical Milestone |
|---|---|---|
| **Month 04** | **Active Directory & Offensive PowerShell:** Win32 API, In-Memory execution, Kerberos, Pass-the-Hash, DCSync, BloodHound, PowerView, Mimikatz. | AD Attack & Defense lab. |
| **Month 05** | **Network Services & Device Hardening:** SNMP v1-v3, TR-069, router management interfaces, Linux hardening (nftables, auditd), Windows Sysmon/Event Forwarding. | RCE / gateway bypass + hardening checklist. |
| **Month 06** | **Wireless Security:** Wi-Fi 802.11 (WPA2/WPA3 Enterprise), Evil Twin, Bluetooth Classic/BLE (ATT/GATT), Aircrack-ng, Ubertooth, Crackle. | WPA2/WPA3 audit on own network + BLE analysis. |

### 3rd Quarter: Exploit Development, Firmware & RF Fundamentals

| Month | Topics & Technologies | Practical Milestone |
|---|---|---|
| **Month 07** | **C Language, Assembly & Exploit Dev:** Memory management (stack/heap), x86/x64 Assembly, buffer overflow, shellcode, ROP chains. | Buffer overflow exploit written in C. |
| **Month 08** | **Firmware & Embedded Reversing:** MIPS/ARM/PowerPC architectures, Binwalk, Ghidra, UART/SPI/JTAG. | Firmware extraction + analysis of a router/gateway device. |
| **Month 09** | **Radio Frequency & SDR:** RTL-SDR, HackRF One, GQRX, SDR++, GNU Radio — signal analysis and decoding. | Signal decoding + replay restricted to own transmitters. |

### 4th Quarter: Physical Security, Telecom & Industrial OT/ICS

| Month | Topics & Technologies | Practical Milestone |
|---|---|---|
| **Month 10** | **Physical Security & Access Control:** RFID/NFC (125 kHz & 13.56 MHz, MIFARE), Proxmark3/Flipper Zero, VLAN hopping via exposed ports, physical intrusion testing methodology. | Badge cloning in a controlled environment + physical pentest report. |
| **Month 11** | **Telecom & Mobile Networks:** 2G-5G NR architecture, SS7/Diameter signaling, Open5GS, 3GPP TS 33.501. | Private, isolated 5G core (Open5GS) + passive signaling analysis. |
| **Month 12** | **IoT & Industrial OT/ICS:** ESP32/FreeRTOS/MQTT, Modbus, S7comm, DNP3, OPC UA, Purdue Model, IEC 62443, NIST SP 800-82. | Modbus/S7 lab with traffic analysis/injection + introductory OT audit report. |

---

## ⚠️ Legal & Ethical Notes

All testing involving RF transmission, signal replay, physical access control, or telecom signaling is restricted to equipment and environments I own, or performed under explicit written authorization. Active jamming and interception of third-party communications are not part of this roadmap; radio transmission in Brazil is regulated by Anatel. This repository documents study and lab work, not attacks on systems I don't own or have authorization to test.

---

## 📌 Disclaimer

All technical documentation, code snippets, and material published in this repository are intended solely for educational, research, and defensive/offensive security validation purposes within authorized laboratory environments.
