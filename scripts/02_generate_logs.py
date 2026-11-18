#!/usr/bin/env python3
"""Generate the synthetic log set for Case Omega (all values fictional)."""
import csv, json, pathlib
L = pathlib.Path(__file__).resolve().parent.parent / "logs"
L.mkdir(exist_ok=True)
D = "2026-11-15"
def w(name, header, rows):
    with open(L / name, "w", newline="") as f:
        c = csv.writer(f); c.writerow(header); c.writerows(rows)

w("auth_events.csv", ["timestamp","host","account","event","source"], [
 (f"{D} 07:42:11","HOSP-WS-14","nurse.priya","Interactive logon (4624 type 2)","console"),
 (f"{D} 07:56:40","HOSP-SRV-01","svc_backup","Network logon (4624 type 3)","HOSP-WS-14 10.20.5.14"),
 (f"{D} 07:56:44","HOSP-SRV-01","svc_backup","Special privileges assigned (4672)","HOSP-WS-14 10.20.5.14"),
])
w("usb_events.csv", ["timestamp","host","event","device_id","serial"], [
 (f"{D} 07:44:30","HOSP-WS-14","USB mass storage inserted","VID_0951&PID_1666 (fictional)","OMEGA-USB-0001"),
 (f"{D} 07:47:05","HOSP-WS-14","USB mass storage removed","VID_0951&PID_1666 (fictional)","OMEGA-USB-0001"),
])
w("browser_history.csv", ["timestamp","host","user","url","note"], [
 (f"{D} 07:46:52","HOSP-WS-14","nurse.priya","https://mail.casomega-hospital.test/inbox","webmail opened"),
 (f"{D} 07:47:30","HOSP-WS-14","nurse.priya","https://mail.casomega-hospital.test/attach/invoice_Q4.zip","attachment downloaded"),
 (f"{D} 07:51:10","HOSP-WS-14","nurse.priya","https://198.51.100.24/update/check","redirect/beacon page (TEST-NET)"),
])
w("process_events.csv", ["timestamp","host","process","parent","command_line"], [
 (f"{D} 07:48:03","HOSP-WS-14","explorer.exe","userinit.exe","open C:\\Users\\nurse.priya\\Downloads\\invoice_Q4.zip"),
 (f"{D} 07:49:18","HOSP-WS-14","invoice_viewer.exe","explorer.exe","C:\\Users\\nurse.priya\\Downloads\\invoice_viewer.exe"),
 (f"{D} 07:49:55","HOSP-WS-14","schtasks.exe","invoice_viewer.exe","/create /tn OmegaSync /sc onlogon (simulated)"),
 (f"{D} 07:49:58","HOSP-WS-14","reg.exe","invoice_viewer.exe","add HKCU\\...\\Run /v InvoiceViewer (simulated)"),
])
w("network_firewall.csv", ["timestamp","src_host","src_ip","dst_ip","dst_port","proto","action","bytes_out"], [
 (f"{D} 07:51:02","HOSP-WS-14","10.20.5.14","198.51.100.24",443,"TCP","ALLOW",18234),
 (f"{D} 07:53:40","HOSP-WS-14","10.20.5.14","198.51.100.24",443,"TCP","ALLOW",9120),
 (f"{D} 07:56:39","HOSP-WS-14","10.20.5.14","10.20.8.2",445,"TCP","ALLOW",4410),
])
# file activity: per-minute modify/rename counts on the clinical share
counts = {"08:02":120,"08:03":410,"08:04":690,"08:05":880,"08:06":1010}
w("file_activity.csv", ["timestamp","host","path","files_modified_or_renamed"],
  [(f"{D} {t}:00","HOSP-SRV-01","D:\\Shares\\Clinical",n) for t,n in counts.items()] +
  [(f"{D} 08:04:27","HOSP-SRV-01","D:\\Shares\\Clinical\\README_RESTORE_FILES.txt","1 (new file)")])
alerts = [
 {"timestamp": f"{D} 08:06:10","host":"HOSP-SRV-01","source":"EDR","rule":"Mass file modification / rename","severity":"HIGH"},
 {"timestamp": f"{D} 08:08:52","host":"NETWORK","source":"SOC action","rule":"Server VLAN isolated by incident commander","severity":"INFO"},
]
(L / "edr_alerts.json").write_text(json.dumps(alerts, indent=2))
print("logs written:", sorted(p.name for p in L.iterdir()))
