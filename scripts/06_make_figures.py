#!/usr/bin/env python3
"""Create scene sketch, evidence tags, and timeline visualisations (matplotlib)."""
import csv, pathlib, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
R = pathlib.Path(__file__).resolve().parent.parent
I = R / "images"

# ---------- Fig 2: scene sketch ----------
fig, ax = plt.subplots(figsize=(10, 6.2)); ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off")
def box(x, y, w, h, label, fc="#e8f0fe", ec="#1a3d7c", fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=1.6))
    ax.text(x + w/2, y + h/2, label, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal")
ax.add_patch(Rectangle((1, 1), 98, 60, fill=False, ec="#444", lw=2))
ax.text(50, 58, "CASE OMEGA - SCENE SKETCH (not to scale)  |  Hospital IT room & nurse station, Ward 4", ha="center", fontsize=11, weight="bold")
ax.add_patch(Rectangle((3, 30), 40, 24, fill=True, fc="#fafafa", ec="#777", ls="--"))
ax.text(5, 51.5, "Ward 4 - Nurse Station", fontsize=9, style="italic")
box(5, 36, 18, 9, "HOSP-WS-14\n(nurse workstation)\nTags: E05, E04", fc="#fde8e8", ec="#a32020", bold=True)
box(28, 36, 14, 9, "USB device\nOMEGA-USB-0001\n(Tag E04)", fc="#fff4d6", ec="#9a6b00")
ax.add_patch(Rectangle((50, 30), 47, 24, fill=True, fc="#fafafa", ec="#777", ls="--"))
ax.text(52, 51.5, "Server Room (rack R2)", fontsize=9, style="italic")
box(54, 36, 16, 9, "HOSP-SRV-01\n(file server)\nTags: E01, E03", fc="#fde8e8", ec="#a32020", bold=True)
box(75, 36, 17, 9, "Firewall / SIEM / EDR\nconsole\nTag: E02", fc="#e6f6ea", ec="#1c6b36")
box(30, 14, 16, 8, "Core network switch\n(VLAN 20/30)", fc="#eeeeee", ec="#555")
box(8, 14, 16, 8, "Email gateway\n(attachment source)", fc="#eeeeee", ec="#555")
box(54, 14, 21, 8, "ISOLATION POINT\nServer VLAN cut 08:08:52", fc="#fff4d6", ec="#9a6b00", bold=True)
box(79, 14, 17, 8, "Evidence table\n(write blocker,\nlaptop, sealed bags)", fc="#e8f0fe", ec="#1a3d7c")
for (x1, y1, x2, y2) in [(15, 36, 15, 22), (24, 18, 30, 18), (46.4, 18, 53.6, 18), (38, 22, 58, 36), (23.4, 40.5, 27.6, 40.5), (70, 40.5, 75, 40.5)]:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.4, color="#333"))
ax.text(40, 6, "Photograph points: P1 screens/alerts  P2 rack & cabling  P3 labels/serials  P4 evidence table", fontsize=8, ha="center")
ax.text(97, 3.5, "N ^", fontsize=10, ha="right", weight="bold")
fig.savefig(I / "fig02_scene_sketch.png", dpi=170, bbox_inches="tight"); plt.close(fig)

# ---------- Fig 3: evidence tags ----------
tags = [("E01", "Server image OMEGA-E01.dd", "HOSP-SRV-01", "SHA-256 eab3c7f3...37b3"),
        ("E02", "SIEM / log export", "Firewall-SIEM", "CSV + JSON logs"),
        ("E03", "Ransom note README_RESTORE_FILES.txt", "HOSP-SRV-01 D:\\Shares\\Clinical", "Recovered from image"),
        ("E04", "USB drive OMEGA-USB-0001", "HOSP-WS-14 USB port", "Seized (simulated)"),
        ("E05", "Email attachment metadata invoice_Q4.zip", "Mail gateway", "SHA-256 571e9da1...c60e")]
fig, axs = plt.subplots(1, 5, figsize=(13, 3.0))
for a, (eid, desc, src, note) in zip(axs, tags):
    a.set_xlim(0, 10); a.set_ylim(0, 14); a.axis("off")
    a.add_patch(Rectangle((0.2, 0.2), 9.6, 13.4, fc="#fffbe6", ec="#b8860b", lw=2))
    a.add_patch(Rectangle((0.2, 11), 9.6, 2.6, fc="#b8860b"))
    a.text(5, 12.3, f"EVIDENCE TAG {eid}", ha="center", va="center", color="white", weight="bold", fontsize=9)
    import textwrap
    a.text(0.7, 10, "Item:\n" + textwrap.fill(desc, 24), va="top", fontsize=7.2)
    a.text(0.7, 6.4, "Source:\n" + textwrap.fill(src, 26), va="top", fontsize=7.2)
    a.text(0.7, 3.4, "Note: " + note, va="top", fontsize=7)
    a.text(0.7, 1.0, "Case OMEGA-2026-11 | 15-Nov-2026", fontsize=6.5, color="#555")
fig.savefig(I / "fig03_evidence_tags.png", dpi=170, bbox_inches="tight"); plt.close(fig)

# ---------- Timeline data ----------
rows = list(csv.DictReader(open(R / "analysis" / "attack_timeline.csv")))
t = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
lanes = ["AUTH", "USB", "BROWSER", "PROCESS", "NETWORK", "FILE", "EDR", "IR"]
lane_of = {"SOC action": "IR", "IR": "IR"}
col = {"AUTH": "#1f77b4", "USB": "#9467bd", "BROWSER": "#2ca02c", "PROCESS": "#d62728", "NETWORK": "#ff7f0e", "FILE": "#8c564b", "EDR": "#e377c2", "IR": "#17becf"}

# ---------- Fig 10: swimlane ----------
fig, ax = plt.subplots(figsize=(8.6, 4.8))
for r in rows:
    lane = lane_of.get(r["source"], r["source"])
    ax.scatter(t(r["timestamp"]), lanes.index(lane), s=70, color=col[lane], zorder=3, edgecolor="k", lw=0.5)
ax.set_yticks(range(len(lanes))); ax.set_yticklabels(lanes); ax.set_ylim(len(lanes) - 0.4, -0.6)
ax.grid(axis="x", alpha=0.3)
key = [("07:44:30", "USB", "USB inserted"), ("07:48:03", "PROCESS", "attachment\nopened", 12), ("07:49:18", "PROCESS", "invoice_viewer.exe\n+ persistence", -22),
       ("07:51:02", "NETWORK", "outbound HTTPS"), ("07:56:40", "AUTH", "svc_backup logon"), ("08:04:27", "FILE", "ransom note"),
       ("08:06:10", "EDR", "EDR alert"), ("08:08:52", "IR", "VLAN isolated", 10)]
for k in key:
    tm, ln, lab = k[:3]; off = k[3] if len(k) > 3 else -14
    ax.annotate(lab, (t("2026-11-15 " + tm), lanes.index(ln)), xytext=(0, off), textcoords="offset points", fontsize=8.5, ha="center", rotation=0)
import matplotlib.dates as md
ax.xaxis.set_major_formatter(md.DateFormatter("%H:%M")); ax.xaxis.set_major_locator(md.MinuteLocator(byminute=range(0, 60, 5)))
ax.set_title("Case Omega - correlated attack timeline, 15 Nov 2026 (IST)", weight="bold"); ax.set_xlabel("Time (IST)")
fig.tight_layout(); fig.savefig(I / "fig10_timeline_swimlane.png", dpi=170); plt.close(fig)

# ---------- Fig 11: file activity rate ----------
fa = [r for r in rows if r["source"] == "FILE" and "README" not in r["event"]]
x = [t(r["timestamp"]) for r in fa]; y = [int(r["event"].split(":")[-1]) for r in fa]
fig, ax = plt.subplots(figsize=(8.5, 3.8))
ax.bar(x, y, width=0.0006, color="#8c564b"); ax.plot(x, y, "o-", color="#8c564b")
ax.axvline(t("2026-11-15 08:04:27"), color="red", ls="--"); ax.text(t("2026-11-15 08:04:20"), max(y) * 1.02, "ransom note 08:04:27", color="red", fontsize=8, ha="right")
ax.axvline(t("2026-11-15 08:06:10"), color="purple", ls=":"); ax.text(t("2026-11-15 08:06:05"), max(y) * 1.02, "EDR alert 08:06:10", color="purple", fontsize=8, ha="right")
ax.xaxis.set_major_formatter(md.DateFormatter("%H:%M")); ax.set_ylim(0, max(y) * 1.15); ax.set_ylabel("Files modified/renamed per minute"); ax.set_xlabel("Time (IST)")
ax.set_title("HOSP-SRV-01 D:\\Shares\\Clinical - file-modification rate", weight="bold"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(I / "fig11_file_activity.png", dpi=170); plt.close(fig)

# ---------- Fig 06: attack chain ----------
fig, ax = plt.subplots(figsize=(8.2, 4.0)); ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
steps = ["1  Phishing email\ninvoice_Q4.zip\n07:47", "2  invoice_viewer.exe\nexecuted\n07:49", "3  Persistence\ntask + Run key\n07:49", "4  C2 beacon\n198.51.100.24:443\n07:51",
         "5  Privileged logon\nsvc_backup\n07:56", "6  Mass file rename\n.omega_locked\n08:02", "7  Ransom note 08:04\nEDR alert 08:06\nVLAN cut 08:08"]
pos = [(2, 28), (27, 28), (52, 28), (77, 28), (2, 4), (27, 4), (52, 4)]
for i, (s_, (x0, y0)) in enumerate(zip(steps, pos)):
    ax.add_patch(FancyBboxPatch((x0, y0), 21, 16, boxstyle="round,pad=0.3,rounding_size=1", fc="#e8f0fe" if i < 6 else "#fde8e8", ec="#1a3d7c"))
    ax.text(x0 + 10.5, y0 + 8, s_, ha="center", va="center", fontsize=9)
for i in range(3): ax.annotate("", xy=(pos[i+1][0] - 0.6, 36), xytext=(pos[i][0] + 21.6, 36), arrowprops=dict(arrowstyle="->", lw=1.5))
ax.annotate("", xy=(12.5, 20.6), xytext=(87.5, 27.4), arrowprops=dict(arrowstyle="->", lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=0"))
for i in (4, 5): ax.annotate("", xy=(pos[i+1][0] - 0.6, 12), xytext=(pos[i][0] + 21.6, 12), arrowprops=dict(arrowstyle="->", lw=1.5))
fig.savefig(I / "fig06_attack_chain.png", dpi=170, bbox_inches="tight"); plt.close(fig)
print("figures done")
