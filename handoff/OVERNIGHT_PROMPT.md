# Paste everything below the line into Claude Code (started in this folder)

---

You are working unattended overnight on my VLSI lab project. I am asleep and cannot answer questions. Read `CLAUDE.md` and `ProjectState.md` in this folder first and follow CLAUDE.md strictly (no invented numbers, write only in `output/`, log progress in `output/PROGRESS_LOG.md`, mark doubts with `[CHECK]`).

You have NO access to my lab PC (Cadence runs there; I reach it through AnyDesk only). Do the document work below, which needs only this folder. Work through the tasks in order; if one gets stuck, log why and move to the next.

## Task 1: Full report draft (most important)
Create `output/Report_Draft.docx` following the faculty template in CLAUDE.md (Times New Roman 12 pt, headings 14 pt, sections in the template order, cover page with placeholders for names/register numbers/batch). Use python-docx (install it if needed).
- Fill every section that can be written from ProjectState.md, the netlists and the paper (if the PDF is available, read it for the theory section and for accurate citation).
- Theory and working principle: explain Fig. 2 as built (NMOS input pair M9/M10, diode-connected PMOS loads, current mirrors to the output, cascode output stage M12/M15 and M6/M5, cascode bias devices, Ibias = 2 uA, C0 = 1 pF), weak/moderate inversion, the gain expression the paper gives (eq. 3 / eq. 4), and why sizing (input pair width -> gm, longer L on output devices -> r_o) changes gain, GBW, delay and power. Use the device mapping table in ProjectState.md (Virtuoso names vs paper names).
- Tool and technology: Cadence Virtuoso 6.1.8 (Schematic, ADE L, Spectre), Layout Suite XL with Virtuoso Space-based Router, Assura DRC/LVS, Quantus (PEX), gpdk045 45 nm generic PDK, thick-oxide devices g45n2svt/g45p2svt, VDD = 2.0 V.
- Tables: (a) without vs with sizing (power, delay, PDP, plus gain, GBW, phase margin); (b) PVT table. Recompute percentages with Python and keep the values from ProjectState.md.
- Every screenshot slot gets a clear placeholder box: `[SCREENSHOT: <exactly what to capture, which cell/window, which markers visible>]`.
- Post-layout results, LVS outcome and final DRC status: placeholders (`[TO FILL ...]`).
- "Any other relevant information": include the "Deviations from the paper" notes from ProjectState.md.
- Problems faced / problems resolved: use the debugging histories in ProjectState.md (schematic and layout), written as a numbered list of problem -> cause -> solution.
- Conclusion: honest summary (what improved with sizing, what still misses the spec and why, PVT spread, layout status).
- References: the paper (full IEEE-style citation), Cadence documentation for Virtuoso/Spectre/Assura (generic), gpdk045 PDK, plus at most 2 standard analog textbooks (Allen & Holberg; Razavi) only if you actually reference a concept from them, marked [CHECK].
Also save the same content as `output/Report_Draft.md` for quick review.

## Task 2: Screenshot checklist
Create `output/Screenshot_Checklist.md`: a numbered list of every screenshot the report needs, mapped to its report section, with exact instructions for capturing each in Virtuoso (which cell, which analysis, which markers to place, what values should be visible, e.g. "AC gain/phase of sized circuit with markers at DC gain 46.66 dB, 0 dB at 1.726 MHz, phase -90.0 deg"). Include both the baseline (cell `Low_AmpSd_base`, swap it into the test benches temporarily) and the sized versions, the PVT runs, the layout, DRC/LVS result windows, and post-layout waveforms. Order them so I can capture them efficiently in one sitting (group by test bench / analysis).

## Task 3: Morning guide for the remaining lab work
Create `output/Morning_Guide.md`: a step-by-step guide (one step per numbered block, exact menus and keys, what to send/check after each) for:
1. Fixing the 13 remaining Assura DRC errors listed in ProjectState.md section 6c: for each rule, what it means physically, how to locate it (Error Layer Window, right-arrow), and the usual fix (move/shorten a Metal1 segment, nudge a device, move a router gate contact, etc.). Mark guesses with [CHECK].
2. LVS with Assura (Assura -> Run LVS; schematic = Sld_80/Low_AmpSd/schematic, layout = Sld_80/Low_AmpSd/layout, Extract rules `/home/install/FOUNDRY/analog/45nm/assura/extract.rul`, Compare rules `/home/install/FOUNDRY/analog/45nm/assura/compare.rul`). Include how to handle the ideal I0 (idc) and C0 (pcapacitor) that exist only in the schematic: option A (instance property such as `lvsIgnore`, mark [CHECK] since it depends on the Assura version), option B (move them into the test benches and add an `ibias` pin to the b1 net; then update test benches). Include how to read the LVS result (match / mismatch, the "Open Tool" / LVS Debug windows) and common mismatches to expect (body terminals, ideal parts, pin names).
3. PEX with Quantus (Quantus -> Run Quantus / Assura -> Run RCX depending on menu; output an `av_extracted` or `extracted` view), then post-layout simulation by making the test benches use the extracted view (config view or "Setup -> Environment -> Switch View List" with the extracted view name first), rerunning AC on `low_amp1` and transient on `low_amp1_tran`, and comparing with the schematic results. Give a small table template for pre- vs post-layout.
Keep it practical; I am a beginner in Virtuoso.

## Task 4: Update the state file copy
Create `output/ProjectState_updated.md`: a copy of ProjectState.md with a short "Overnight work done" section added at the top listing the new files. Do not edit the original.

## Finish
At the end, append a summary to `output/PROGRESS_LOG.md` with: files created, anything I must verify, and the very first thing I should do in the morning.
