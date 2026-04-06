# AUTOMATED SECURITY PROXY AND VULNERABILITY MONITOR

An interactive Inter-Process Communication (IPC) wrapper written in Python that acts as a real-time security monitor for vulnerable C/C++ applications.

This project demonstrates how to intercept user input, scan it for malicious patterns (Buffer Overflows, Format Strings, Integer Wraps, Trapdoor/Backdoor Logins, Cache Poisoning), and log attacks in real time — before they can exploit the underlying executable.

## Core Features

1. **Real-Time Interception** — Utilizes `pexpect` to create a live proxy between the user's keyboard and the target C++ binary.
2. **Buffer Overflow Detection** — Dynamically compares the actual length of an inputted string against the user's declared allocation size before passing it to memory.
3. **Format String Prevention** — Scans inputs for malicious memory-leak format specifiers (e.g., `%p`, `%x`, `%n`, `%s`).
4. **Integer Wrap Detection** — Monitors mathematical inputs (like quantity/price multipliers) to prevent maximum integer boundary bypassing.
5. **Trapdoor / Backdoor Detection** — Checks login credentials against a known list of hardcoded backdoor passwords and flags suspicious keywords.
6. **Cache Poisoning Detection** — Validates promo codes against a legitimate registry and detects value-tampering attempts where attackers inject forged discount values.
7. **Automated Forensic Logging** — Silently appends all triggered security alerts to a background `.log` file with precise timestamps.

## Prerequisites

To run this MasterMonitor, you need a Linux environment with the following installed:

- `python3`
- `g++`
- `pexpect`

```bash
sudo apt update && sudo apt install python3-pexpect
# For installing the required Python library
```

## Compilation

```bash
g++ -o victim MasterVictim.cpp
g++ -o format_victim format_victim.cpp
```

## Usage

### MasterMonitor2.py (Real-Time / Telephone Mode)

Works like a telephone — takes one input, sends it to the C++ binary, waits for it to process, then asks for the next input.

```bash
python3 MasterMonitor2.py
# Or with custom paths:
python3 MasterMonitor2.py --victim ./victim --log ./security_alerts.log
```

### MasterMonitor.py (Batch / Mail Mode)

Works like mail — takes all the inputs at once and then sends them all to `MasterVictim.cpp` in a single batch.

```bash
python3 MasterMonitor.py
```

## Attack Types Demonstrated

| Attack | How It Works | Detection Method |
|--------|-------------|-----------------|
| Buffer Overflow | Input longer than declared buffer size | Compare declared length vs actual input length |
| Format String | Injecting `%p`, `%x`, `%n` in name field | Scan input for dangerous format specifiers |
| Integer Wrap | Large quantity causing unsigned int wrap | Threshold check on quantity values |
| Trapdoor/Backdoor | Hardcoded password `MASTER_28` in binary | Match against known backdoor credential list |
| Cache Poisoning | Injecting fake promo codes or tampering discount values | Validate against legitimate promo registry |
