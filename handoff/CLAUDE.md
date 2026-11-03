# CLAUDE.md: instructions for Claude Code working on this folder

## What this project is
A VLSI System Design lab project (23ECE302 VLSI Design / 23ECE383 VLSI Design Lab, Amrita School of Engineering, Bengaluru, B.Tech V sem, AY 2026-27). The student recreates **Fig. 2 ("Cascade Second Stage Topology for improved gain in weak inversion region")** of the paper "Low-Power CMOS Operational Amplifier Design in 45nm Technology" (D. Chowbey, R. K. Baruah, DevIC 2025, Kalyani, India, DOI 10.1109/DevIC63749.2025.11012572) in Cadence Virtuoso with the gpdk045 PDK, sizes it, runs PVT, draws the layout, and writes a report.

**Read `ProjectState.md` first.** It is the single source of truth for every number, setting, file path and decision. Never contradict it; if something there looks wrong, flag it in `output/PROGRESS_LOG.md`, do not silently change it.

## Where things are
- Cadence work (schematics, layout, simulations) lives ONLY on the student's Red Hat lab PC (user `train`, project dir `~/sld_proj`, library `Sld_80`). The student reaches it from this laptop through AnyDesk, which is a remote screen only. **From this laptop you have no shell or file access to the lab PC.** Do not pretend otherwise and do not try to drive AnyDesk.
- This folder (on the laptop) holds documents: `ProjectState.md`, netlists in `netlists/`, and your outputs in `output/`.
- The paper PDF and the report template (`System Design Project Report_format.doc`) may be in the parent folder or nearby (look for them, e.g. `..\Low-Power_CMOS_Operational_Amplifier_Design_in_45nm_Technology.pdf`). Read them if present; if not, rely on ProjectState.md and say so.

## Rules
1. **Never invent results.** Every number in anything you write must come from ProjectState.md or the netlists. If a value is missing (for example post-layout results, LVS outcome), write a clearly marked placeholder like `[TO FILL: post-layout tp]`.
2. **Do the arithmetic in code** (Python) when you compute or re-check power, PDP, percentages; do not do it in your head.
3. **Be honest about limitations** in anything written for the report: Fig. 2 only (paper's headline 66.85 dB / 2.31 MHz / 12.5 uW are for the full Fig. 3 design), gain below the 60 dB target, power above 20 uW in transient, the wiring interpretations listed in ProjectState.md ("Deviations from the paper").
4. **Write only inside `output/`** (plus appending to `output/PROGRESS_LOG.md`). Never delete or overwrite the student's other files.
5. **Log as you go:** after each finished task, append a short entry to `output/PROGRESS_LOG.md` (what you did, which files, anything the student must check).
6. **This is graded student work.** Produce drafts and guides the student will review, edit and own. Mark anything you are unsure about with `[CHECK]`.
7. If something is ambiguous, pick the most reasonable reading, note it in the log, and carry on. Do not stop to ask; the student is asleep.

## How the student likes to be guided (for any step-by-step guide you write)
- One step at a time, numbered, with exact Virtuoso menu paths and key presses, what they should see, and what to check.
- Plain language, short WHY lines, no walls of text.
- Proven Virtuoso facts for this install (use them): undo = `u`; Check and Save = `X`; Q = properties; R = rectangle; M = move; S = stretch; Shift+F all levels, Ctrl+F top level; ADE "Select On Design"; one ADE L session per design; Netlist -> Recreate if results look stale; lab shell is csh/tcsh (no `2>/dev/null`).

## Report format (from the faculty template)
Times New Roman 12 pt everywhere, headings 14 pt. Sections, in order:
Title of the system design project; Title of the paper; Details of the paper (source of the title); Circuit diagram; Theory and working principle; Tool and technology used; Screenshot of the simulator based circuit implementation; Screenshot of the output waveform obtained from the simulator (DC and transient); Screenshot of the circuit based on sizing concept; Screenshot of the output waveform for the circuit with sizing concept (DC and transient); Table: Parameter | Value without sizing | Value with sizing for Power calculation, Delay calculation, Power Delay Product (with screenshots as proof); Screenshot of the PVT analysis; Screenshot of the layout; Screenshot of the output waveform obtained from the simulator for the layout; Any other relevant information; Conclusion; Problems faced during the implementation; Problems resolved using solutions; Any other comment; References.
The cover page has: Amrita School of Engineering, Bengaluru; Department of Electronics & Communication Engineering; B.Tech V Semester (ECE and EAC) AY 2026-2027; Assignment for 23ECE302 VLSI Design; System Design for 23ECE383 VLSI Design Laboratory; Report; July to November 2026; title; table for register numbers, names, signatures; batch number; faculty examiner signature with evaluation date. Leave student details as placeholders.
