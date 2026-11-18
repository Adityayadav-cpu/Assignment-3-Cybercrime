#!/usr/bin/env python3
"""Correlate the synthetic logs into one ordered timeline (CSV) and print it.
Plaso/log2timeline would be used on real artefacts; this script normalises the
fixture CSV/JSON records the same way (timestamp, host, source, event)."""
import csv, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
L = R / "logs"
ev = []
def rows(n): return list(csv.DictReader(open(L / n)))
for r in rows("auth_events.csv"):    ev.append((r["timestamp"], r["host"], "AUTH",    f'{r["account"]}: {r["event"]} from {r["source"]}'))
for r in rows("usb_events.csv"):     ev.append((r["timestamp"], r["host"], "USB",     f'{r["event"]} (serial {r["serial"]})'))
for r in rows("browser_history.csv"):ev.append((r["timestamp"], r["host"], "BROWSER", f'{r["url"]} - {r["note"]}'))
for r in rows("process_events.csv"): ev.append((r["timestamp"], r["host"], "PROCESS", f'{r["process"]} <- {r["parent"]}'))
for r in rows("network_firewall.csv"):ev.append((r["timestamp"], r["src_host"], "NETWORK", f'{r["src_ip"]} -> {r["dst_ip"]}:{r["dst_port"]} {r["action"]} ({r["bytes_out"]} B out)'))
for r in rows("file_activity.csv"):  ev.append((r["timestamp"], r["host"], "FILE",    f'{r["path"]} : {r["files_modified_or_renamed"]}'))
for a in json.load(open(L / "edr_alerts.json")): ev.append((a["timestamp"], a["host"], a["source"], a["rule"]))
ev.append(("2026-11-15 08:14:06","HOSP-SRV-01","IR","Forensic acquisition authorised/started (scenario)"))
ev.sort()
out = R / "analysis" / "attack_timeline.csv"
with open(out, "w", newline="") as f:
    c = csv.writer(f); c.writerow(["timestamp","host","source","event"]); c.writerows(ev)
print(f"{'TIMESTAMP (IST)':<20} {'HOST':<12} {'SRC':<8} EVENT")
for t,h,s,e in ev: print(f"{t:<20} {h:<12} {s:<8} {e[:50]}")
print(f"\n{len(ev)} events correlated -> analysis/attack_timeline.csv")
