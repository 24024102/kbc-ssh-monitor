import re
import time
import json
import os
import requests
from collections import defaultdict

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)


failed_attempts = defaultdict(list)

def send_telegram_alert(message):
    config = load_config()
   
    if not config.get('telegram_enabled', True):
        return
        
    token = config.get('bot-token')
    chat_id = config.get('chat-id')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": f"SECURITY ALERT:\n{message}"
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f" Failed to send via telegram : {e}")

def monitor():
    send_telegram_alert("System is okay! ")
    config = load_config()
    log_path = config.get('log-file', 'auth-log')
    limit = config.get('attempts_limit', 5)
    window = config.get('time_window_second', 60)
    
    print(f"[{time.ctime()}]  SIEM-lite з. : Spectating for the file{log_path}")

    
    if not os.path.exists(log_path):
        open(log_path, 'a').close()

    with open(log_path, 'r', encoding='utf-8') as f:
        f.seek(0, 2) 
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            if "Failed password" in line:
                match = re.search(r"from (\d{1,3}(?:\.\d{1,3}){3})", line)
                if match:
                    ip = match.group(1)
                    now = time.time()
                    
                    failed_attempts[ip].append(now)
                   
                    failed_attempts[ip] = [t for t in failed_attempts[ip] if now - t < window]
                    
                    print(f"Failled attemtp с IP: {ip}. Tries in a minute: {len(failed_attempts[ip])}")

                    if len(failed_attempts[ip]) >= limit:
                        alert_msg = f"Brute-force detected! IP {ip} blacklisted {len(failed_attempts[ip])} tries."
                        print(f" {alert_msg}")
                        send_telegram_alert(alert_msg)
                        failed_attempts[ip] = [] 

if __name__ == "__main__":
    monitor()