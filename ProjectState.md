# ProjectState.md — VLSI System Design Project (23ECE302 / 23ECE383)

Last updated: 2026-11-03 night (repo restructure: VLSI_SLD is the project folder). FINAL REPORT = `report/Report_Final.docx` (+ `.pdf`, 36 pages). Everything is done except: cover page names, the ss PVT table decision, and layout (DRC/LVS/PEX). See sections 8b, 10, 11. Update this file after every completed step.

## 1. Assignment
- Circuit assigned (Dr. Kaveri Hatti): **Fig. 2 — Cascade Second Stage Topology for improved gain in weak inversion region**
- Paper: "Low-Power CMOS Operational Amplifier Design in 45nm Technology", D. Chowbey and R. K. Baruah, DevIC 2025 (Kalyani, India), DOI 10.1109/DevIC63749.2025.11012572
- Only Fig. 2 is in scope (16 transistors + Ibias + C1). NOT Fig. 3 (the 29-transistor version).
- Deliverables: report in "System Design Project Report_format.doc" (sections listed in section 8 below).
- Paper spec targets (Table I): VDD 2.0 V, Pdiss < 20 uW, gain >= 60 dB, GBW >= 2 MHz, SR >= 2.5 V/us, PM >= 50 deg.

## 2. Environment
- Machine: Red Hat lab PC (host vlsi150 / user "train"), Virtuoso 6.1.8-64b, Spectre, ADE L.
- PDK: **gpdk045** (45 nm). Devices: `nmos2v` (model g45n2svt) and `pmos2v` (model g45p2svt), thick-oxide, W = 320n, L = 150n, m = 1 for ALL transistors (baseline).
- Library: `Sld_80` (project folder `~/sld_proj`). Cells: `Low_AmpSd` (the op-amp, schematic + symbol), `low_amp1` (DC/AC test bench), `low_amp1_tran` (follower transient test bench, used for delay, power and PVT), `Low_AmpSd_base` (unsized backup).
- Netlist path: `/home/train/simulation/low_amp1/spectre/schematic/netlist/netlist`
- Windows project folder (documents only): `C:\Users\MY PC\Desktop\SEM 5\VLSI_SLD` (see section 10). Older copies (`C:\Users\Admin\Desktop\SEM 5\VLSI_Lab\SystemLevel`, `C:\Users\MY PC\Desktop\SEM 5\VLSI_SystemLevel`) are stale snapshots, do not trust them.

## 3. Test bench (cell low_amp1)
- V0: vdc = 2 V on `vdd`; `vss` to gnd.
- V2 on `vin+`: DC = **1.028 V** (trip-point bias), AC magnitude = 1 (for AC analysis).
- V3 on `vin-`: DC = 1 V.
- Output net labelled `out`. Load capacitor C0 = 1 pF is INSIDE Low_AmpSd (do not add another).
- Ibias: analogLib `idc`, **DC current = 2u** inside Low_AmpSd.

## 4. Device name mapping (inferred, my names in Virtuoso -> paper Fig. 2)
| Virtuoso | Type | Paper | Role |
|---|---|---|---|
| M9 | NMOS | M1 | input pair, vin- |
| M10 | NMOS | M2 | input pair, vin+ |
| M8 | PMOS | M3 | diode load (net b2) |
| M11 | PMOS | M4 | diode load (net b3) |
| M7 | PMOS | M8 | mirror of M3 into M2 diode |
| M12 | PMOS | M6 | output pull-up mirror (mirrors M4) |
| M15 | PMOS | M15 | cascode pull-up |
| M13 | PMOS | M12 | diode (cascode bias) |
| M14 | PMOS | M11 | mirror of M13 (net b4) |
| M3 | NMOS | M14 | sink for M13 diode, gate on bias net b1 |
| M2 | NMOS | M9 | diode (net14) |
| M6 | NMOS | M7 | output pull-down |
| M5 | NMOS | M16 | cascode pull-down |
| M4 | NMOS | M13 | diode (net b4) |
| M0 | NMOS | M10 | bias diode (net b1) |
| M1 | NMOS | M5 | tail (but currently shorted to b1, see Fix 4) |

## 5. Debugging history (use for report sections "Problems faced / resolved")
1. **VSS check-and-save error** — set pin direction to inputOutput, redraw wire onto the pin.
2. **Hanging `out` wire warning** — harmless (test bench), kept for plotting.
3. **Output stuck at 1.9989 V, flat for all vin+ (0 to 2 V)** — root cause found from the Spectre netlist:
   - Ibias had NO DC value (isource with no dc=) -> 0 A. FIXED: idc = 2u.
   - 4 floating gate nets (net4, net10, net44, net33), mirrors not diode-connected. FIXED with wire labels b1, b2, b3, b4.
   - Input pair M9/M10 were PMOS instead of NMOS. FIXED: Q -> Cell Name pmos2v->nmos2v, body to vss.
4. **Stale netlist** (changes not appearing) — a second ADE L session was attached to Low_AmpSd; used ADE only from low_amp1, Simulation -> Netlist -> Recreate.
5. **Fix 4 (tail node = bias node short, copied from a dot in the paper's drawing)** — NOT applied: the circuit works as drawn, kept faithful to the paper.

## 6. Results so far (BASELINE, "without sizing")
- DC sweep of vin+ (vin- = 1 V): sharp transition, trip point vin+ ~ **1.028 V** (read from plot), smooth S-curve, ~1.0 V crossing at 1.028.
- At V2 = 1.028 V: out(DC) = **1.13 V** (mid-rail OK).
- Supply current (V0): **7.943 uA**. Power = 2 V x 7.943 uA = **15.886 uW** (meets < 20 uW).
- Rough estimate of DC gain from sweep slope: ~130-140 V/V (~43 dB), BELOW the 60 dB spec. To be confirmed by AC analysis.
- **AC baseline (done):** DC gain **44.6 dB** (marker at 1.26 Hz), -3 dB point ~4 kHz, GBW (0 dB crossing) ~**0.69-0.71 MHz** (marker 708 kHz, -0.255 dB), phase at 707.9 kHz = -89.74 deg, **phase margin ~90.3 deg**. Spec status: gain short by ~15 dB, GBW short by ~3x, PM and power OK. Method: ADE L -> Outputs -> Setup, expressions `gain_dB = dB20(VF("/out"))` and `phase_deg = phase(VF("/out"))`; ac analysis 1 Hz to 1 GHz, 20 pts/decade, V2 AC magnitude = 1. (Direct Plot gave empty windows in this install; the expression method works.).
- **Transient baseline (done):** test bench `low_amp1_tran` = unity-gain follower (out tied to vin-), vpulse on vin+ (0.8 V to 1.2 V, delay 1u, rise/fall 10n, width 10u, period 20u), tran stop 40u, moderate. Output settles ~28 mV below input (systematic offset, matches DC trip 1.028 V). Rising edge fast, falling edge slow (weak pull-down, Ibias only 2 uA).
  - Markers: out crosses 1.0 V at 1.1762 us (rising) and 11.2699 us (falling). Input crosses 1.0 V at 1.005 us and 11.015 us.
  - tPLH = 171.2 ns, tPHL = 254.9 ns, **tp = 213 ns**.
  - avg supply current (expr `average(IT("/V0/PLUS"))`) = **-12.3356 uA**, transient avg power = 2 V x 12.3356 uA = **24.67 uW** (above 20 uW spec; DC-bias power was 15.886 uW).
  - **PDP = 24.67 uW x 213 ns = 5.26 pJ.**
  - Use the SAME method (transient avg power, tp from the same follower test) for the "with sizing" column.

## 6b. SIZED results (with sizing) and PVT (done 2026-11-02)
**Sizing v1 applied in Low_AmpSd** (backup of unsized circuit = `Low_AmpSd_base`): M9, M10 (input pair) W = 1.6u, L = 150n; M5, M6 (NMOS) and M12, M15 (PMOS) W = 640n, L = 300n; all others unchanged (320n/150n). Ibias still 2u. Verified in the Spectre netlist.
- New trip point: vin+ = **1.016089 V** (out DC = 0.981 V at that bias), offset smaller than baseline (1.028 V).
- **AC (sized):** DC gain **46.66 dB**, GBW **1.726 MHz**, phase margin **~90.0 deg** (phase -90.005 deg at 1.728 MHz) = Nov 2 photo run. **Re-run 2026-11-03 16:50 (real screenshot, V2 = 1.016 V, mc): DC gain 46.636 dB (marker at 9.01 Hz), 0 dB crossing at 1.72485 MHz (920.654 udB), phase -90.0024 deg at 1.72119 MHz, PM about 90.0 deg. The report now uses 46.64 dB / 1.725 MHz.**
- **Transient (sized): 2026-11-03 run (student confirmed correct, used in the report): tPLH = 79.5 ns, tPHL = 118.1 ns, tp = 98.8 ns; avg_I = -16.354 uA (calculator shows -16.35E-6) -> power 32.71 uW; PDP = 3.23 pJ.** (Earlier Nov 2 photo run, no longer used: tPLH 120.0, tPHL 116.6, tp 118.3 ns, PDP 3.87 pJ.) Model section of the 11-03 run not confirmed; report text still says mc.
- PVT nominal row only: same measurement on section **tt**, 27 C, 2.0 V: tPLH 82.1 ns, tPHL 119.7 ns, tp 100.9 ns, avg_I = -16.227 uA, power 32.45 uW, PDP 3.27 pJ.

**With vs without sizing (both columns are mc runs, same method; confirmed by the student 2026-11-03):**
| Parameter | Without | With | Change |
|---|---|---|---|
| DC gain | 44.6 dB | 46.64 dB (46.66 on Nov 2) | +2.04 dB |
| GBW | ~0.7 MHz | 1.725 MHz (1.726 on Nov 2) | 2.4-2.5x |
| Phase margin | ~90.3 deg | ~90.0 deg | same |
| Power (transient avg) | 24.67 uW | 32.71 uW | +33% |
| Delay tp | 213 ns | 98.8 ns | -53.6% |
| PDP | 5.26 pJ | 3.23 pJ | -38.6% |

**PVT (sized circuit, follower test bench low_amp1_tran; model file sections available: tt, ff, ss, fs, sf, mc):**
| Case | Section | Temp | VDD | tp | Power | PDP |
|---|---|---|---|---|---|---|
| Nominal | tt | 27 C | 2.0 V | 100.9 ns | 32.45 uW | 3.27 pJ |
| A slow | ss | 125 C | 1.8 V | 194.0 ns (tPLH 153.8, tPHL 234.3) | 16.32 uW (avg_I -9.065 uA) | 3.17 pJ |
| B fast | ff | -40 C | 2.2 V | 51.9 ns (tPLH 39.4, tPHL 64.4) | 77.51 uW (avg_I -35.23 uA) | 4.02 pJ |
Findings: delay varies ~2x, power ~5x across PVT; power is the weak point (20 uW target met only at the slow corner). Case C (tt, 125 C, 2.0 V) skipped.

**Honest notes for the report ("Deviations from the paper"):** gpdk045 thick-oxide devices, L = 150n baseline; Ibias = 2 uA is our choice; paper Fig. 2 omits some gate connections, we added the mirror diode connections per the paper text and used an NMOS input pair; tail node shorted to bias node as drawn; results are for Fig. 2 only (paper's 66.85 dB / 2.31 MHz / 12.5 uW are for the full Fig. 3 design); gain still below the 60 dB target; no process-corner limitation (corners ss/ff were available).

## 6c. LAYOUT progress (2026-11-03)
- Layout view `Sld_80/Low_AmpSd/layout` created with Layout XL (Launch -> Layout XL -> Create New; Connectivity -> Generate -> All From Source). gpdk045 tech already attached. Menus available: Assura (DRC/LVS), Quantus (PEX), PVS, Route (Virtuoso Space-based Router, VSR).
- Placement (matches the floorplan sketch): top PMOS row M7 M8 M11 M12 M15 M13 M14; middle NMOS row M0 M9 M10 M1 M3 (M9 under M8, M10 under M11); bottom NMOS row M2 M6 M5 M4. Options -> Display -> Show Name Of: instance shows M-numbers. Ctrl+F = boxes only, Shift+F = all levels.
- Pins (Metal1 pin, enlarged to roughly transistor-box size): vdd top, vin- and vin+ on the left, out on the right, vss bottom.
- Rails on **Metal1 drawing**: vdd rail on top (overlaps vdd pin), vss strap between middle and bottom rows (starts right of the vin+ pin), vss rail at bottom (overlaps vss pin), vertical Metal1 link from strap to bottom rail at the right edge.
- Device parameters set on every transistor: Bodytie Type = Detached; PMOS Top Tap, NMOS Bottom Tap (Left Tap unticked); Gate Connection: PMOS Bottom, NMOS Top.
- One Nwell drawing rectangle over the whole PMOS row (merged the separate n-wells).
- Routing: Route -> Automatic Routing -> All Nets routes the 11 signal nets (11/11, 0 opens, 0 shorts); vdd and vss are skipped by All Nets, route them by selecting both in Navigator -> Nets, then Route -> Automatic Routing -> Selected Nets (2/2, 0 opens, 0 shorts). Annotation Browser Connectivity = 0/0 (no incomplete nets, no shorts).
- Backups: student was asked to copy the layout view to `layout_preroute` and `layout_routed` (not confirmed which exist).
- **DRC** (Assura -> Run DRC, Run Name drc1, Run Directory ".", Technology -undefined-, Rules File `/home/install/FOUNDRY/analog/45nm/assura/assuraDRC.rul`). History: ~50 errors -> 14 -> latest **13 remaining**: OXIDETHK.SP.1 (1, thick active to thick active spacing >= 0.16 um), CONT.SE.3 (2, gate contact to active >= 0.06 um), CONT.SE.4 (2, 1.8V gate contact to active >= 0.07 um), METAL1.SP.1.1 (3, >= 0.06 um), METAL1.SP.1.2 (2, >= 0.1 um), METAL1.SP.1.3 (3, wide-metal >= 0.25 um). Route -> Fix Violations removed VIA1.X.1. Remaining ones need hand fixes: jump to each with the right-arrow button in the Error Layer Window.
- **LVS rule files** (Assura): `/home/install/FOUNDRY/analog/45nm/assura/extract.rul` and `/home/install/FOUNDRY/analog/45nm/assura/compare.rul`. Known LVS issue: the schematic has ideal analogLib parts I0 (idc, 2 uA, vdd -> b1) and C0 (pcapacitor 1 pF, out -> vss) with no layout; they must be excluded (e.g. instance property lvsIgnore, to be verified for this Assura version) or moved to the test benches (then b1 needs a pin). Body terminals are tied via Detached taps.
- Lab PC shell is csh/tcsh: `2>/dev/null` does not work; use plain commands. PDK root: `/home/install/FOUNDRY/analog/45nm/` (gpdk045, models/spectre/gpdk045.scs, assura/, pvs/).
- Layout debugging history for the report: (1) rails first drawn on Metal1 *fill* purpose -> 5 router shorts, fixed by changing to Metal1 drawing; (2) body (B) terminals left open (16) -> fixed with Detached body taps; (3) 40 gate-contact spacing errors from router-placed M1_PO contacts -> fixed by pcell Gate Connection Top/Bottom; (4) 6 Nwell spacing errors -> one merged Nwell rectangle.

## 7. Roadmap / checklist
- [x] Schematic of Fig. 2 built, checked, symbol created
- [x] Test bench low_amp1, DC operating point
- [x] Fix bias, gate ties, input pair type; netlist verified
- [x] DC sweep, trip point 1.028 V, out = 1.13 V
- [x] Baseline power 15.886 uW
- [x] AC analysis: gain 44.6 dB, GBW ~0.7 MHz, PM ~90.3 deg (baseline); screenshots still to be taken cleanly for the report
- [x] Transient: tp = 213 ns (baseline); clean screenshots still to be taken for the report
- [x] Baseline table: power 24.67 uW (transient avg), tp 213 ns, PDP 5.26 pJ; gain 44.6 dB, GBW ~0.7 MHz, PM ~90.3 deg
- [x] SIZING DONE (see 6b): Low_AmpSd_base backup, v1 sizing, trip point 1.016089 V, AC and transient re-run
      Ideas: longer L on output/cascode devices and mirrors for gain; larger W/L on input pair M9/M10 for gm; mirror ratio of M12 vs M11 (paper S6/S4); keep power < 20 uW
- [x] Table: Parameter | Value without sizing | Value with sizing (Power, Delay, PDP) (in 6b)
- [x] PVT analysis (nominal, slow, fast; table in 6b). Screenshots of PVT still to be taken cleanly.
- [x] Report screenshots: real Cadence screenshots for Figs 4, 16, 17, 18, S20, S21, S22, 19, 20 and layout Figs 22, 25, 26, 27. Still older images: Figs 23, 24 (layout placement/pins) and the baseline (unsized) figures (phone photos or earlier captures)
- [x] Layout placed and routed (connectivity clean), see 6c
- [ ] DRC: 13 errors left (see 6c), fix by hand
- [ ] LVS (Assura, extract.rul + compare.rul; handle ideal I0 and C0)
- [ ] PEX (Quantus) and post-layout simulation (re-use low_amp1 / low_amp1_tran with the extracted view)
- [ ] Layout and post-layout screenshots
- [ ] Write report

## 8. Report sections required (from System Design Project Report_format.doc)
Font: Times New Roman 12 everywhere, headings 14.
Title of project; title of paper; details of paper; circuit diagram; theory and working principle; tool and technology used; screenshot of simulator circuit; DC and transient waveforms (no sizing); screenshot of circuit with sizing; DC and transient waveforms (with sizing); table (power, delay, PDP, without vs with sizing) with screenshots as proof; PVT analysis screenshot; layout screenshot; layout simulation waveform; other info; conclusion; problems faced; problems resolved; any other comment; references.

## 8b. NEXT ACTION (resume here)
1. **Cover page** of `report/Report_Final.docx`: names, register numbers, batch number are yellow `[TO FILL]` (the student fills these in Word).
2. **ss PVT table decision (ask the student, answer "update pvt"):** the real ss screenshot (Fig 19) gives tPLH 153.7 ns, tPHL 253.7 ns, tp 203.7 ns, avg_I -9.06535 uA, power 16.32 uW, PDP 3.32 pJ. The PVT table, the observations paragraph (delay ratio "1.9 times", "3.7 times", PDP range 3.17 to 4.02 pJ), the PVT conclusion and the bar chart (Fig 21) still use the old photo reading (tPHL 234.3, tp 194.0, PDP 3.17). Update table + text + conclusion; the bar chart image cannot be regenerated here (regenerate with the new values or say so in the caption).
3. **Layout (not progressed since DRC 13 errors):** fix the 13 DRC errors by hand, then LVS (extract.rul/compare.rul, handle ideal I0 and C0, see 6c and docs/Morning_Guide.md), PEX, post-layout simulation. If any of it is done, retake Figs 22-27, update the layout section text and the "not performed" statements in the report.
4. **Before any new simulation reset ADE:** V0 = 2 (the `low_amp1_tran` schematic was last SAVED with V0 = 2.2 from PVT case B), model section mc, temperature 27.
5. Unconfirmed: the model section of the 2026-11-03 sized transient run (report text says mc for the sized circuit; nominal tt gave 82.1/119.7 ns, the sized run gave 79.5/118.1 ns).

## 9. Open questions
- Exact Ibias value to use at sizing stage (2 uA currently).
- Which delay definition the faculty expects (propagation delay vs settling time).

## 10. REPORT STATUS and FILE LOCATIONS (2026-11-03)
- Project folder = git repo root: `C:\Users\MY PC\Desktop\SEM 5\VLSI_SLD` (private GitHub repo https://github.com/vpvishnu53/Low_Power_CMOS_Amplifier, branch main). The old `LATEST/` and `handoff/` folders were merged into it on 2026-11-03; earlier versions are in git history. The cloud sandbox is only scratch.
- **FINAL REPORT: `report/Report_Final.docx` and `report/Report_Final.pdf`** (36 pages). It was edited directly in the docx XML; there is no generator any more. Never regenerate it from a script or template; edit the docx.
- Folder contents:
  - `README.md` (index + resume prompt), `ProjectState.md` (this file), `CLAUDE.md` (working rules)
  - `report/` Report_Final.docx, Report_Final.pdf, `source_images/` (the images the old generator used, kept for reference)
  - `docs/` CADENCE_LOG.md (lab-PC log), PROGRESS_LOG.md (what was done when), Morning_Guide.md (DRC/LVS/PEX how-to, still needed for layout), Screenshot_Checklist.md (shot list S01-S43)
  - `netlist/Low_AmpSd_baseline_netlist.scs` (reference netlist of the corrected baseline) and `netlist/Low_AmpSd_sized_netlist_with_testbench.scs` (sizing v1 op-amp + low_amp1 test bench)
  - `references/` the IEEE paper PDF and "System Design Project Report_format.doc" (both committed; the repo is private)
  - `screenshots/` real Cadence screenshots used in the report: S01 (baseline schematic) and G2_testbench_low_amp1 (older, still used for Figs 2 and 15), S02/S14/S16/S19/S20 (test bench, DC, AC, transient, avg_I), S21a/b, S22/S22b (nominal PVT), S23/S23b (ss), S24/S24b (ff), S26, S30, S31, S32 (layout, DRC form, DRC errors, annotation browser)
- The class report format file is `references/System Design Project Report_format.doc`; the section list is in section 8.

## 11. Final numbers in the report (all mc unless stated)
| Item | Value |
|---|---|
| Baseline (unsized) | gain 44.6 dB, GBW ~0.7 MHz, PM ~90.3 deg, tp 213 ns (tPLH 171.2, tPHL 254.9), power 24.67 uW (avg 12.3356 uA), PDP 5.26 pJ, DC-bias power 15.886 uW |
| Sized | gain 46.64 dB, GBW 1.725 MHz, PM ~90.0 deg, trip/bias V2 = 1.016 V (DC sweep marker 1.016094 V, out 1.000859 V) |
| Sized transient | tPLH 79.5 ns, tPHL 118.1 ns, tp 98.8 ns, avg_I -16.354 uA (calculator -16.35E-6), power 32.71 uW, PDP 3.23 pJ |
| Change vs baseline | gain +2.04 dB, GBW 2.4-2.5x, power +32.6 %, tp -53.6 %, PDP -38.6 % |
| Spec gaps | gain 13.36 dB below 60 dB, GBW 0.28 MHz below 2 MHz, transient power above 20 uW |
| PVT nominal tt 27 C 2.0 V | table 82.1/119.7/100.9 ns, avg -16.227 uA (screenshot: 82.0/119.2/100.6 ns, avg -16.2274 uA), power 32.45 uW, PDP 3.27 pJ |
| PVT A ss 125 C 1.8 V | table 153.8/234.3/194.0 ns, 16.32 uW, 3.17 pJ. **Screenshot (Fig 19): 153.7/253.7/203.7 ns, avg -9.06535 uA, PDP 3.32 pJ (table not yet updated)** |
| PVT B ff -40 C 2.2 V | 39.4/64.4/51.9 ns (screenshot 39.3/64.4), avg -35.2335 uA, 77.51 uW, PDP 4.02 pJ |
| Layout | DRC 13 errors (OXIDETHK.SP.1 1, CONT.SE.3 2, CONT.SE.4 2, METAL1.SP.1.1 3, METAL1.SP.1.2 2, METAL1.SP.1.3 3, run drc4), Annotation Browser Connectivity 0/0; LVS, PEX, post-layout NOT done |

## 12. The 1.0637 V DC sweep (resolved as a wrong run)
- A sweep on 2026-11-03 (0.8 to 1.2 V, shallow curve, marker 1.0637 V) disagreed with the Nov 2 result and was removed from the report. The re-run (0.9 to 1.125 V, only /out plotted) gave a sharp transition at 1.016094 V, out 1.000859 V, reproducing 1.016089 V. Cause of the shallow curve unknown (suspect leftover ADE conditions).

## 13. ADE / Virtuoso tips learned
- DC sweep: only /out should have Plot ticked (untick gain_dB, phase_deg). V2 `dc` swept 0.9 to 1.125 V, step 0.0005.
- An expression output (e.g. `avg_I = average(IT("/V0/PLUS"))`) is evaluated only when "Plotted/Evaluated" is ticked in Setting Outputs; `/V0/PLUS` needs Save ticked. If the Value stays empty, use Tools -> Calculator, type `average(IT("/V0/PLUS"))` (not with `?result "tran"`), Enter, then the Evaluate icon.
- Transient plot: show only /in and /out, place four markers at the 1.0 V crossings; keep the mouse off the toolbar so no tooltip covers it.
- If the run fails with "cellview has been modified since the last extraction": press X (check and save) in the schematic, then Netlist and Run.
- Plot not opening: Results -> Plot Outputs -> Transient; Plot after simulation = Auto. The check-and-save warning about the hanging `out` wire is harmless.
- Annotation Browser: Window -> Assistants (shows Connectivity (0/0)); Error Layer Window lists DRC rule groups.
- PVT recipe (same ADE window): V0 value in the schematic + X, Setup -> Model Libraries section (tt/ss/ff), Setup -> Temperature, Netlist and Run.
