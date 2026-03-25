from flask import Flask, render_template, request, send_file
import re
from collections import defaultdict
import csv

app = Flask(__name__)

log_data = []
failed_logins = defaultdict(int)
suspicious_ips = set()

def analyze_logs(file):
    global log_data
    log_data.clear()
    failed_logins.clear()
    suspicious_ips.clear()

    for line in file:
        line = line.decode("utf-8")
        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
        ip = ip_match.group(1) if ip_match else "Unknown"

        event = "Normal"
        severity = "Low"

        if "Failed password" in line:
            failed_logins[ip] += 1
            event = "Failed Login"
            severity = "Medium"

        if "error" in line.lower() or "invalid" in line.lower():
            suspicious_ips.add(ip)
            event = "Suspicious Activity"
            severity = "High"

        log_data.append((ip, event, severity))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        analyze_logs(file)

    return render_template("index.html",
                           logs=log_data,
                           failed=dict(failed_logins),
                           suspicious=list(suspicious_ips))

@app.route("/export")
def export():
    filename = "report.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Event", "Severity"])
        writer.writerows(log_data)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)