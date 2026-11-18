#!/usr/bin/env python3
"""Repository structure and Markdown checks (run locally and by GitHub Actions)."""
import pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent.parent
required = ["README.md", "AUTHORSHIP.md", "documentation/first_responder_SOP.md",
 "documentation/chain_of_custody.csv", "documentation/tool_summary_workflow.md",
 "evidence/OMEGA-E01.dd", "evidence/OMEGA-E01.dd.sha256", "logs/auth_events.csv",
 "analysis/attack_timeline.csv", "analysis/sandbox_behaviour_report.json",
 "images", "scripts", "report"]
errors = []
for p in required:
    ok = (R / p).exists()
    print(f"[{'PASS' if ok else 'FAIL'}] exists: {p}")
    if not ok: errors.append(p)
for md in sorted(R.rglob("*.md")):
    t = md.read_text()
    rel = md.relative_to(R)
    h1 = len(re.findall(r"^# ", t, re.M))
    ok = h1 == 1 and t.endswith("\n") and "\t" not in t and not re.search(r"[ ]+$", t, re.M)
    print(f"[{'PASS' if ok else 'FAIL'}] markdown format: {rel}")
    if not ok: errors.append(str(rel))
print("\nRESULT:", "FAILED" if errors else "ALL CHECKS PASSED")
sys.exit(1 if errors else 0)
