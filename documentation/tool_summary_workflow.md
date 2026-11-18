# Tool Summary and Workflow

| Tool | Use in this project | Executed here |
| --- | --- | --- |
| dd | Bit-stream acquisition of the source volume | Yes (on a 16 MiB ext4 fixture) |
| sha256sum / cmp | Hash generation and verification | Yes |
| debugfs | Read-only review and extraction from the image | Yes |
| Python 3 scripts | Fixture creation, log correlation, entropy and IOC extraction, figures | Yes |
| matplotlib | Timeline visualisations and scene sketch | Yes |
| FTK Imager | Equivalent GUI acquisition on Windows (procedure documented) | No |
| Autopsy, Plaso/log2timeline, Wireshark | Recommended for real cases | No |

## Workflow

1. `scripts/01_build_fixture.py` builds the fictional server volume contents.
2. `dd` images the volume to `evidence/OMEGA-E01.dd`; SHA-256 is computed before and after.
3. `scripts/02_generate_logs.py` writes the synthetic logs.
4. `scripts/03_build_timeline.py` correlates all logs into `analysis/attack_timeline.csv`.
5. `scripts/04_entropy_analysis.py` and `scripts/05_extract_iocs.py` analyse the recovered files and logs.
6. `scripts/06_make_figures.py` draws the sketch, tags and timelines.
7. `scripts/check_repo.py` and the GitHub Actions workflow verify structure and Markdown.
