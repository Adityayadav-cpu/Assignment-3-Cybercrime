#!/usr/bin/env python3
"""Build the synthetic 'compromised server' volume contents (all data is fictional).
No executable or malicious code is produced: 'locked' files are just random bytes
used to demonstrate entropy analysis."""
import os, random, pathlib
root = pathlib.Path("/tmp/omega_src")
if root.exists():
    import shutil; shutil.rmtree(root)
clin = root / "Shares" / "Clinical"
clin.mkdir(parents=True)
(root / "Windows" / "System32" / "winevt").mkdir(parents=True)
(root / "Users" / "svc_backup").mkdir(parents=True)
random.seed(11)
# intact files (synthetic text)
for i in range(1, 6):
    (clin / f"ward_roster_{i:02d}.txt").write_text(
        f"SYNTHETIC ROSTER {i}\n" + "\n".join(f"PATIENT-{i}{j:03d} (synthetic) bed {j}" for j in range(1, 40)) + "\n")
# 'locked' files: random bytes standing in for high-entropy (encrypted-looking) content
for i in range(1, 6):
    (clin / f"lab_results_{i:02d}.txt.omega_locked").write_bytes(os.urandom(48_000))
(clin / "README_RESTORE_FILES.txt").write_text(
"""*** CASE OMEGA TRAINING ARTIFACT - FICTIONAL RANSOM NOTE ***
Your files have been locked. (Simulated text for a classroom exercise.)
Contact: restore@casomega-attacker.example   Wallet: SIMULATED-WALLET-0000
This note is not real. No payment is requested. No real system was affected.
""")
(root / "Windows/System32/winevt/Security_export.txt").write_text(
    "SIMULATED EVENT LOG EXPORT - see logs/ directory for structured data\n")
(root / "Users/svc_backup/NOTE.txt").write_text("Service account profile (synthetic).\n")
print("fixture tree built:", sum(1 for _ in root.rglob('*') if _.is_file()), "files")
