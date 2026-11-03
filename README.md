# VLSI System Design Project: Fig. 2 cascade op-amp, 45 nm gpdk045 (23ECE302 / 23ECE383)

**Final report:** [`report/Report_Final.docx`](report/Report_Final.docx) (Word, edit this one) and [`report/Report_Final.pdf`](report/Report_Final.pdf) (36 pages).

| Path | What it is |
|---|---|
| `report/Report_Final.docx`, `.pdf` | the final report (edit the docx directly; there is no generator) |
| `report/source_images/` | earlier images (phone photos, first captures) used for the baseline and older figures |
| `ProjectState.md` | **hand-off**: full project context, results, numbers, layout status, next actions |
| `CLAUDE.md` | working rules for an AI assistant (one step at a time, Virtuoso tips) |
| `docs/` | CADENCE_LOG (lab-PC log), PROGRESS_LOG, Morning_Guide (DRC/LVS/PEX how-to), Screenshot_Checklist |
| `netlist/` | Spectre netlists: corrected baseline, and the sized op-amp with test bench |
| `references/` | the paper (Chowbey and Baruah, IEEE DevIC 2025) and the faculty report format (.doc) |
| `screenshots/` | Cadence screenshots used in the report (`S<number>_<what>_real.png`) |

## Status (2026-11-03)
Done: schematic, sizing, DC/AC/transient, PVT (tt, ss, ff) with real screenshots, final report.
Open: cover-page names/register numbers/batch; ss PVT table update (ProjectState 8b item 2); layout (13 DRC errors, LVS, PEX, post-layout not done).

## Resume with an AI assistant
Open this folder (`C:\Users\MY PC\Desktop\SEM 5\VLSI_SLD`), then paste:

> Continue my VLSI System Design project (23ECE302/383, Fig. 2 op-amp, Cadence Virtuoso 6.1.8, gpdk045). Read ProjectState.md first (sections 8b, 10, 11), then CLAUDE.md, then report/Report_Final.docx. Working folder: C:\Users\MY PC\Desktop\SEM 5\VLSI_SLD (the git repo root). Edit the docx directly; there is no generator. Do not invent numbers. One step at a time, detailed numbered steps starting from the Library Manager. I send screenshots, you crop them and put them into the report and show me the page.
