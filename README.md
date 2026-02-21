# SSH Brute-Force Detector (SIEM-lite)

### Description
A lightweight security monitor designed for practice. It parses system logs in real-time to detect and respond to SSH brute-force attacks.

### Features
- **Real-time Log Parsing**: Monitors `auth.log` for failed login attempts.
- **Sliding Window Logic**: Detects threats based on a configurable time window (e.g., 5 attempts in 60s).
- **Instant Alerts**: Integrated with Telegram API for immediate security notifications.
- **Automated Blacklisting**: Logs malicious IPs for further action.

### Tech Stack
- **Python 3.14**
- **Requests Library** (API Integration)
- **JSON Configuration**
