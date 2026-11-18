#!/usr/bin/env python3
"""Extract Indicators of Compromise from the synthetic logs and artefacts."""
import re, pathlib, json
R = pathlib.Path(__file__).resolve().parent.parent
text = "\n".join(p.read_text(errors="ignore") for p in (R/"logs").iterdir())
ips  = sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)))
ext  = sorted(i for i in ips if not i.startswith("10."))
files= sorted(set(re.findall(r"[\w\-]+\.(?:exe|zip|omega_locked)\b|README_RESTORE_FILES\.txt", text)))
doms = sorted(set(re.findall(r"https?://([\w\.\-]+)", text)))
accts= sorted(set(re.findall(r"\b(?:svc_backup|nurse\.priya)\b", text)))
rep  = json.load(open(R/"analysis"/"sandbox_behaviour_report.json"))
print("IOC EXTRACTION - CASE OMEGA")
print("External IPs      :", ", ".join(ext))
print("Domains/hosts     :", ", ".join(doms))
print("File names        :", ", ".join(files))
print("Accounts involved :", ", ".join(accts))
print("Persistence       :", "; ".join(p.get("name") or p.get("value") for p in rep["persistence"]))
print("Attachment SHA-256:", open(R/"evidence/samples/invoice_Q4.zip.sha256").read().split()[0])
