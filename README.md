# 🕵️ AI Log Hunter (Sherlock)

**Automated Threat Intelligence for Linux Logs using GPT-4.**

## 🚀 Overview
This tool automates the "Tier 1" work of a Security Operations Center (SOC) Analyst. It ingests raw Linux authentication logs (`auth.log`), applies statistical analysis to identify anomalies (brute force patterns), and uses the OpenAI API to generate a natural-language incident report.

## ⚡ Features
- **Statistical Anomaly Detection:** Mathematically scans logs to identify the "noisiest" attacker IP (Brute Force detection).
- **AI Contextual Analysis:** Extracts specific evidence of successful compromise (SSH sessions, accepted passwords) using GPT-4o.
- **Automated Reporting:** Outputs a clear Verdict, Attacker IP, and Risk Assessment.

## 🛠️ Tech Stack
- **Python 3.10+** (Core Logic)
- **OpenAI API** (Intelligence Engine)
- **Regex & Counter** (Data Parsing)

## 💻 How to Run
1. **Clone the repo:**
   ```bash
   git clone https://github.com/nikos/AI-Log-Hunter.git
2. Install Dependencies 
   ```bash 
   pip install openai
3. Run the script 
   ```bash
   python sherlock.py
## 🔍 Use Case
Tested against HackTheBox "Brutus" scenario. Successfully identified the attacker IP (65.2.161.68) and confirmed successful root compromise amidst 20,000+ failed login attempts.