import os
import re
from collections import Counter
from openai import OpenAI

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "API_KEY = os.getenv("OPENAI_API_KEY") # Or paste your key here for local testing" 

client = OpenAI(api_key=API_KEY)

def count_failed_attempts(filename):
    """
    Scans the ENTIRE file for 'Failed password' and counts IPs.
    Returns the IP with the most failures.
    """
    ip_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    failed_ips = []
    
    print(f"[*] Scanning {filename} for brute force patterns...")
    
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "Failed password" in line:
                # Find the IP in this line
                match = re.search(ip_pattern, line)
                if match:
                    failed_ips.append(match.group(1))
    
    if not failed_ips:
        return None, 0
    
    # Count frequency of each IP
    most_common = Counter(failed_ips).most_common(1)
    return most_common[0] # Returns ('1.2.3.4', 5000)

def analyze_target(ip, filename):
    """
    Greps the logs for the specific suspicious IP to see if they ever succeeded.
    """
    relevant_logs = []
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if ip in line:
                relevant_logs.append(line.strip())
    
    # Take the last 20 logs (usually where the success happens) and first 5
    evidence_chunk = "\n".join(relevant_logs[:5] + ["..."] + relevant_logs[-20:])
    
    prompt = f"""
    Analyze these logs for IP: {ip}
    The User detected {len(relevant_logs)} events involving this IP.
    
    LOGS:
    {evidence_chunk}
    
    Question:
    1. Is this a brute force attack?
    2. Did they eventually succeed? (Look for 'Accepted password')
    
    Format:
    - ATTACKER IP: {ip}
    - ATTACK TYPE: [Brute Force / Credential Stuffing]
    - OUTCOME: [Failed / SUCCESSFUL COMPROMISE]
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    print("\n--- Sherlock Assistant V3 (Statistical Hunter) ---\n")
    filename = "auth.log"
    
    if not os.path.exists(filename):
        print("[-] Error: auth.log not found.")
        return

    # STEP 1: STATISTICS (The "Machine" part)
    top_ip, count = count_failed_attempts(filename)
    
    if not top_ip:
        print("[-] No failed passwords found. Safe file?")
        return
        
    print(f"[!] ALERT: IP {top_ip} failed {count} times! Sending to AI...")
    
    # STEP 2: INTELLIGENCE (The "AI" part)
    verdict = analyze_target(top_ip, filename)
    
    print("\n------------------------------------------------")
    print(verdict)
    print("------------------------------------------------\n")

if __name__ == "__main__":
    main()