# Case Omega - Ransomware Investigation on a Healthcare Network (Simulation)

Assignment 3, Unit 3: Investigation of Cyber Crimes. Everything here is fictional.

## Repository layout

| Path | Contents |
| --- | --- |
| `report/` | Final legal-technical report (DOCX) |
| `evidence/` | Disk image `OMEGA-E01.dd`, SHA-256 file, benign attachment placeholder |
| `logs/` | Synthetic auth, USB, browser, process, firewall, file-activity and EDR logs |
| `analysis/` | Correlated timeline CSV and simulated behaviour report |
| `documentation/` | First responder SOP, chain of custody, tool summary |
| `images/` | Scene sketch, evidence tags, screenshots, timeline charts |
| `scripts/` | Reproducible Python scripts and the repository check |

## Reproduce

```bash
python3 scripts/01_build_fixture.py
python3 scripts/02_generate_logs.py
python3 scripts/03_build_timeline.py
python3 scripts/04_entropy_analysis.py
python3 scripts/05_extract_iocs.py
python3 scripts/check_repo.py
```

## Safety note

No functional malware is included. Files ending in `.omega_locked` contain random bytes only.
