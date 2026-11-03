# CLAUDE.md — Instructions for this project

## Who and what
Student doing the VLSI System Design project (23ECE302 VLSI Design / 23ECE383 VLSI Design Lab, Amrita School of Engineering, Bengaluru). Circuit: **Fig. 2** (cascode second stage op-amp) from the paper "Low-Power CMOS Operational Amplifier Design in 45nm Technology". Read ProjectState.md first for the current status, numbers and checklist. Update it after every completed step.

## How to work with the student
- Guide step by step in Cadence Virtuoso. Give ONE step (or one small group) at a time and wait for the student to confirm it is done before moving on.
- Assume the student does not know Virtuoso. Give exact menu paths, key presses and what they should see after each step. Keep it readable: detailed enough to follow, not a wall of text.
- Use plain language. Explain WHY briefly when a step is not obvious.
- Always end a step by saying exactly what to send back (value, screenshot, CIW message).
- Never invent values. Ask for readings or netlist text. The Spectre netlist is the most reliable evidence of what the schematic really contains.
- Be honest about uncertainty (for example inferred device mapping, values read off a plot).

## Environment facts
- Red Hat lab PC, Virtuoso 6.1.8-64b, Spectre, ADE L, PDK **gpdk045**, devices nmos2v / pmos2v (g45n2svt / g45p2svt), baseline W = 320n, L = 150n, m = 1.
- Library `Sld_80`, cells `Low_AmpSd` (op-amp), `low_amp1` (DC/AC test bench) and `low_amp1_tran` (transient test bench: unity-gain follower with vpulse on vin+). Simulate only from the test benches, never from `Low_AmpSd` itself. `Low_AmpSd_base` (to be created in Step 7) is the unsized backup.
- The Windows folder is for documents (reports, notes, netlists, screenshots). Cadence files live on the Red Hat PC. The bridge to the student's Windows computer may be disconnected; then deliver files with SendUserFile.

## Virtuoso tips learned (use these, they are correct for this install)
- Undo is **u**, redo is **Shift+U** (not Ctrl+Z).
- **X** = Check and Save (preferred). Ctrl+S is a plain save.
- Edit instance: select, press **Q**. To change PMOS to NMOS, change **Cell Name** in the Q form (Edit -> Replace is the wrong dialog in this version).
- Wire = **W**, wire name/label = **L** (same label on two wires connects them), instance = **I**, fit = **F**, descend = Design -> Hierarchy -> Descend Edit, return = Shift+B.
- ADE: Outputs -> To Be Plotted -> **Select On Design** (not "On Schematic"). Sweep a source with Analyses -> Choose -> dc -> Component Parameter -> Select Component -> pick source -> parameter `dc`.
- Keep ONE ADE L session, launched from `low_amp1`. A second session on the same design causes warning ADE-1009 and stale netlists. If results look stale: Simulation -> Netlist -> Recreate.
- Get the netlist: `cat /home/train/simulation/low_amp1/spectre/schematic/netlist/netlist`. Check timestamp with `ls -l --time-style=full-iso` and `date`.
- Never press Ctrl+C or close the terminal that started Virtuoso; never close the CIW.

- AC plots: Results -> Direct Plot produced empty graphs in this install. Use ADE L -> Outputs -> Setup and add expressions `gain_dB` = `dB20(VF("/out"))` and `phase_deg` = `phase(VF("/out"))` (Plot ticked), then run. Read DC gain, 0 dB crossing (GBW) and phase with markers; phase margin = 180 + phase at GBW.

## Circuit notes
- Bias point for AC: V2 (vin+) = 1.028 V DC with AC magnitude 1, V3 (vin-) = 1 V, VDD = 2 V, Ibias = 2u. The open-loop gain is high, so the input must be within about a millivolt of the trip point; re-find it by DC sweep after every sizing change.
- The tail node is shorted to the bias node exactly as drawn in the paper (Fig. 2 dot). Leave it unless the faculty says otherwise.
- Sizing goal: keep power < 20 uW, raise gain toward >= 60 dB, GBW >= 2 MHz, PM >= 50 deg; report Power, Delay, PDP with and without sizing.

## Deliverables and format
Report follows `references/System Design Project Report_format.doc`: Times New Roman 12, headings 14. Sections are listed in ProjectState.md section 8. Collect screenshots for every section as work proceeds, and log problems and solutions as they happen (they feed the "Problems faced / resolved" sections).

## Report editing rules (added 2026-11-03)
- The final report is `report/Report_Final.docx`. It is edited directly (image swaps and text changes in the docx); there is no generator script. Keep a copy before big edits, convert to PDF with LibreOffice to check pages, and show the changed page to the student.
- When a screenshot arrives: check every marker value against the report first (compute delays from the marker times), crop to the Virtuoso window (no taskbar, mail windows or browser tooltips), insert it, fix the caption to match the picture, and flag any number that now disagrees with the rest of the report. Never change a number silently.
- Real screenshots beat older phone photos. If a new run disagrees with an old one, say so and ask before changing tables.
- Keep ProjectState.md up to date after each step and keep `screenshots/` names as S<number>_<what>_real.png.

## More Virtuoso tips (learned 2026-11-03)
- Expression outputs (avg_I) need "Plotted/Evaluated" ticked; else use Tools -> Calculator with `average(IT("/V0/PLUS"))`.
- "cellview has been modified since the last extraction": press X in the schematic, then Netlist and Run.
- For PVT runs in one ADE window change only V0 (then X), the model section and the temperature. Reset to mc, 27 C, V0 = 2 afterwards.
