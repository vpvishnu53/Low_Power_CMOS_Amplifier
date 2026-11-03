# PROGRESS LOG (overnight run, started 2026-11-03)

## Setup (done)
- Read CLAUDE.md, ProjectState.md, OVERNIGHT_PROMPT.md, both netlists, the paper PDF and the faculty template (template text matches the section list in CLAUDE.md).
- Installed python-docx 1.2.0, pypdf, pdfplumber, pywin32 (pip, user site). Word COM is available on this laptop but is NOT needed for the build.
- Working folder changed by the student to `...\VLSI_Lab\SystemLevel`; this handoff folder is `...\SystemLevel\handoff`. All outputs are written to `handoff\output\`.
- Git: repo initialised in `...\SystemLevel` (branch main) with `origin` = https://github.com/vpvishnu53/Low_Power_CMOS_Amplifier.git. NOTHING committed or pushed. (An empty `.git` I first created inside `handoff` was removed.) STM32_BMS was not touched.
- Helper files `_paper_text.txt` and `_template_text.txt` in this folder are scratch extracts (safe to delete).

## Checks on ProjectState.md numbers (recomputed in Python)
- Baseline power 2 V x 12.3356 uA = 24.671 uW; tp = (171.2+254.9)/2 = 213.05 ns; PDP = 5.255 pJ (state: 5.26). OK.
- Sized (mc) power 2 V x 16.354 uA = 32.708 uW; tp = 118.3 ns; PDP = 3.869 pJ (state: 3.87). OK.
- tt: 32.454 uW, PDP 3.275 pJ (state 3.27). ss at 1.8 V: 1.8 x 9.065 = 16.32 uW, PDP 3.17 pJ. ff at 2.2 V: 2.2 x 35.23 = 77.51 uW. All consistent with the state file (power uses the case VDD).
- Changes with sizing: power +32.6 %, tp -44.5 %, PDP -26.4 %, gain +2.06 dB, GBW about 2.4-2.5x. State file rounds these to +33 %, -44 %, -26 %.
- Spec gap: gain short by 13.34 dB (46.66 vs 60), GBW short by 0.27 MHz (1.726 vs 2.0), transient power 32.71 vs <20 uW.
- Paper inconsistency noticed: phase margin is 57.78 deg in Sec. III-A but 68 deg in the Conclusion.

## Task log
- **Task 1 done:** `Report_Draft.docx` (about 20 pages, Times New Roman 12, headings 14, all template sections in order, cover page placeholders) and `Report_Draft.md` (same content; the docx is generated from the md). Device connectivity table is generated from the two netlists. Tables: without/with sizing, spec comparison, PVT, post-layout template. Percentages recomputed in Python (see Setup section). Rendered through Word to PDF and checked visually (cover page, table pages).
- **Task 2 done:** `Screenshot_Checklist.md`, shots S01-S43 in capture order (G0 prep, G1 schematics, G2 low_amp1 baseline then sized, G3 low_amp1_tran, G4 PVT, G5 layout, G6 DRC, G7 LVS, G8 PEX, G9 post-layout) plus a section -> screenshot table. Every ID in the report is in the checklist.
- **Task 3 done:** `Morning_Guide.md` (Step 0 backups; Part 1 DRC rule by rule; Part 2 LVS with Option A and Option B; Part 3 Quantus, extracted view, post-layout runs, pre/post table, troubleshooting table).
- **Task 4 done:** `ProjectState_updated.md` (original `ProjectState.md` verified unchanged by checksum).
- No task got stuck.

## Summary for the morning
**Files created (all in handoff\output):** Report_Draft.docx, Report_Draft.md, Screenshot_Checklist.md, Morning_Guide.md, ProjectState_updated.md, PROGRESS_LOG.md. Nothing outside `output/` was edited. Git: repo initialised in `...\SystemLevel`, remote `origin` = github.com/vpvishnu53/Low_Power_CMOS_Amplifier, nothing committed or pushed (do not push the paper PDF to a public repo). STM32_BMS untouched.

**What I could not verify and you must check:**
1. Every `[CHECK]` (16 in the report, more in the guide) and every `[TO FILL]` (51 in the report). Yellow highlight in the docx. Remove them before submitting.
2. All Virtuoso / Assura / Quantus menu names and the DRC rule interpretations in Morning_Guide.md are from general knowledge, not tested on your install.
3. The baseline transient and power numbers: I assumed they were measured with model section mc like the sized one (ProjectState says "use the mc runs"). Confirm. **Resolved 2026-11-03: the student confirmed every non-PVT run (baseline and sized) was mc.**
4. Theory text: eq. (4) of the paper is garbled in the PDF text extraction; I described it in words and marked it [CHECK] for you to retype. Why power went UP after sizing was not isolated; marked [CHECK].
5. Report title wording, delay definition (tp between 1.0 V crossings of a follower) and the spec items not measured (slew rate, ICMR, output swing, PSRR, CMRR) should be agreed with the faculty.
6. Paper inconsistency: PM 57.78 deg (Sec. III-A) vs 68 deg (Conclusion).

**Important finding:** the extracted (PEX) view will contain neither I0 (2 uA bias) nor C0 (1 pF). Ignoring them only for LVS (Option A) would leave post-layout simulation dead. Recommended: Option B (move both into the test benches, add pin `ibias` on net b1 in schematic, symbol and layout). Details in Morning_Guide.md, top and Step 2.2. After Option B re-run the schematic simulations: you must get exactly the old numbers (46.66 dB, 1.726 MHz, trip 1.016089 V).

**First thing to do in the morning:**
1. Open `output\PROGRESS_LOG.md` (this), then skim `Morning_Guide.md` top section.
2. On the lab PC (Step 0 of the guide): back up the layout and the schematic in the Library Manager, then run Assura DRC and take screenshot S31 (the 13 errors before any fix).
3. Then fix DRC (Part 1), LVS (Part 2, Option B), PEX (Part 3). Capture screenshots as you go using Screenshot_Checklist.md.

## Update 2026-11-03: model section decision applied to the docs
- Student confirmed: **every DC, AC and transient run uses model section mc** (baseline, sized and post-layout). tt, ss and ff are only for the PVT runs. So the Table 2 comparison (44.6 -> 46.66 dB etc.) is mc vs mc and is valid.
- Changed: `ProjectState.md` and `ProjectState_updated.md` (8b reset now says mc; 6b notes), `Screenshot_Checklist.md` (G0.2 and the post-G4 reset now mc, G3 [CHECK] removed, G9 says mc), `Morning_Guide.md` (Option B regression test, Step 3.3 conditions, 3.3.3 restore, and the pre/post table now uses the mc schematic values: tp 118.3 ns, 16.354 uA, 32.71 uW, 3.87 pJ), `Report_Draft.md` and `Report_Draft.docx` (tool section states mc for all non-PVT results, Table 2 [CHECK] removed, post-layout table shows mc values only), `CADENCE_LOG.md` (open items marked resolved).

## Update 2026-11-03 evening: report v2 and hand-off sync
- Real Cadence screenshots (cropped) now in `report/Report_Final_Draft_v2.docx`: Fig 4 test bench, Fig 16 DC sweep (trip 1.016094 V, out 1.000859 V), Fig 17 AC (46.636 dB, 1.72485 MHz, -90.0024 deg), Fig 18 transient (tPLH 79.5, tPHL 118.1, tp 98.8 ns), S20 calculator reading average(IT("/V0/PLUS")) = -16.35E-6 A.
- AC numbers changed in the report: 46.66 -> 46.64 dB, 1.726 -> 1.725 MHz, +2.06 -> +2.04 dB, shortfalls 13.34 -> 13.36 dB and 0.27 -> 0.28 MHz.
- The shallow 1.0637 V DC sweep was a wrong run (not reproduced, removed from the report). See ProjectState section 11.
- Open: PVT screenshots S21, S22, Fig 19, case B; cover page; layout DRC/LVS/PEX.
- Hand-off files refreshed: ProjectState.md, NEW_CHAT_PROMPT.md, README.md, .gitignore, COMMIT_MESSAGE.txt. build_report.py must NOT be run (it would overwrite v2).
- Delay numbers updated in the report (text, Table 2, conclusion): tPLH 79.5, tPHL 118.1, tp 98.8 ns, PDP 3.23 pJ, delay -53.6 %, PDP -38.6 %. Model section of that run not confirmed.

