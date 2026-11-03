# Screenshot checklist for the report

How to use: capture in the order of the groups below (G0 to G9). Each shot has an ID (S01 ... S43). The same ID appears in the boxed placeholder `[SCREENSHOT Sxx: ...]` in `Report_Draft.docx`, so you only have to paste the picture into the matching box. Save every picture as `Sxx_short-name.png` in one folder (for example `shots\`), so you can find it later.

Values in "must be visible" come from ProjectState.md. If your reading differs a little (for example 46.65 instead of 46.66), keep what the tool shows and fix the report number to match the picture. If it differs a lot, stop and tell me, because something in the setup is different from the recorded run.

Items marked [CHECK] are menu names or key presses I am not 100% sure of on your Virtuoso 6.1.8. If a menu is not where I say, look in the neighbouring menu and tell me what you saw.

## G0. Before you start (5 minutes)

1. **How to take the pictures.** You see the lab PC only through AnyDesk, so take the screenshots on the computer where AnyDesk is open: Windows key + Shift + S, drag a rectangle around the Virtuoso window, then paste into Paint or save from the Snipping Tool. Make the AnyDesk window full screen first so that text is sharp. Zoom the Virtuoso window (not the picture) so that text is readable at report size.
2. **Reset ADE** (ProjectState.md section 8b): in `low_amp1` and `low_amp1_tran`, ADE L -> Setup -> Model Libraries: gpdk045.scs section `mc` (mc for everything except the PVT runs); Setup -> Temperature: 27; V0 = 2.0 V. You will change the section and temperature again in group G4 (PVT), so reset them at the start and after G4.
3. **Make a backup first:** in the Library Manager copy `low_amp1` and `low_amp1_tran` to `low_amp1_bak` and `low_amp1_tran_bak` (right-click the cell -> Copy [CHECK], all views). If the swap in G1 goes wrong you can go back.
4. **Waveform window tips:** each marker should show its X and Y values in the marker readout; zoom (press `f` in the waveform window to fit) so that the marker numbers do not overlap the curve; set a plot title or keep the legend so that the signal names (`vin+`, `out`, `gain_dB`, `phase_deg`) are readable.

## G1. Schematics, nothing simulated yet

**S01** -- report section: *Circuit diagram* and *Screenshot of the simulator based circuit implementation*.
- Open `Sld_80 / Low_AmpSd_base / schematic` (the unsized backup). Press `f` to fit.
- Must be visible: the whole circuit, all 16 transistors M0-M15, I0 (2 µA), C0 (1 pF), the pins out, vdd, vin+, vin-, vss, and the net labels b1-b4. Name labels must be readable; if not, zoom in on two halves and take two pictures (S01a, S01b).

**S10** -- *Screenshot of the circuit based on sizing concept*.
- Open `Sld_80 / Low_AmpSd / schematic` (sized). Same view as S01.
- Must be visible: as S01. Optional: show W and L labels of the resized devices (Edit -> Properties, or the CDF display options) so that 1.6u and 640n/300n can be seen.

**S11** -- *Screenshot of the circuit based on sizing concept*.
- In the sized schematic, click M10 (or M9) and press `q`.
- Must be visible: the Edit Object Properties form with Cell Name nmos2v, Width 1.6u, Length 150n. Do NOT click OK; Cancel the form.

**S12** -- same section.
- Click M5 (or M6 / M12 / M15) and press `q`.
- Must be visible: Width 640n, Length 300n (for example M5: nmos2v). Cancel the form.

**S43** -- *Circuit diagram*.
- On your own computer open the paper PDF (page 2) and crop only Fig. 2 with its caption. This is the "source circuit"; the report cites it as Fig. 2 of [1].

## G2. Test bench `low_amp1` (DC and AC): baseline first, then sized

Do the baseline and the sized version in one sitting on this bench so that you open ADE only once.

### G2a. Baseline (swap `Low_AmpSd_base` into the bench)
Swap: open `low_amp1` schematic, click the Low_AmpSd instance, press `q`, change Cell Name to `Low_AmpSd_base` (View stays `symbol`), OK. Set V2 DC = `1.028` (keep AC magnitude 1). Press `X` (check and save) -> 0 errors. In ADE L: Simulation -> Netlist -> Recreate (so the netlist is not stale). [CHECK: if the instance does not accept the new cell name, delete the instance and place `Low_AmpSd_base` with `i`, reconnect the five pins.]

**S02** -- *Screenshot of the simulator based circuit implementation*.
- The `low_amp1` schematic with the base instance.
- Must be visible: V0 = 2 V (net vdd), V2 on vin+ (DC 1.028 V, AC mag 1), V3 on vin- = 1 V, the instance name label showing Low_AmpSd_base, ground symbols.

**S03** -- *Output waveform, DC (baseline)*.
- ADE L: Analyses -> Choose -> dc; Sweep Variable = Component Parameter; select V2 (Select Component, click V2 in the schematic), parameter `dc`; sweep range about 0.95 to 1.1 V (start 0.95, stop 1.1), Auto. Outputs -> To Be Plotted -> Select On Design, click net `out`. Netlist and Run.
- In the waveform window put a marker on the curve where `out` = 1.0 V (menu Marker -> Create Marker, or key `m` [CHECK], then click the curve or type the Y value).
- Must be visible: curve out vs V2 (S-shaped, sharp), marker readout near X = 1.028 V, Y = 1.0 V (ProjectState: trip point about 1.028 V). Optional second marker at X = 1.028 V showing out = 1.13 V.

**S04** -- *Power calculation (baseline DC power)*.
- Results -> Print -> DC Operating Points [CHECK] or Direct Plot of the V0 current; or use the calculator: Tools -> Calculator -> select `I` of V0 at the operating point (V2 = 1.028 V; set the sweep off or run `dc` with Save DC Operating Point).
- Must be visible: V0 supply current 7.943 µA (magnitude). In the report: 2 V x 7.943 µA = 15.886 µW.

**S05** -- *Output waveform, AC (baseline)*.
- ADE L: Analyses -> ac, sweep frequency 1 Hz to 1 GHz, 20 points per decade (Points Per Decade). V2 AC magnitude = 1. Outputs -> Setup: add expressions `gain_dB = dB20(VF("/out"))` and `phase_deg = phase(VF("/out"))`, tick Plot for both; Run. (Direct Plot gave empty windows in your install, so use the expressions as before.)
- In the gain plot put a marker at the lowest frequency (1.26 Hz).
- Must be visible: marker readout about 1.26 Hz and 44.6 dB.

**S06** -- same section.
- Same simulation; in the gain plot put a marker where the curve crosses 0 dB (about 708 kHz, -0.255 dB in your run); in the phase plot put a marker at the same frequency (about 707.9 kHz).
- Must be visible: 0 dB crossing near 0.7 MHz and the phase near -89.74 deg (so PM about 90.3 deg), both plots in one window or two stacked windows.

### G2b. Sized (swap back `Low_AmpSd`)
Swap: instance cell name back to `Low_AmpSd`; set V2 DC = `1.016089` (keep AC magnitude 1). `X`, Netlist -> Recreate.

**S13** -- *Screenshot of the circuit based on sizing concept (test bench)*.
- `low_amp1` with the sized instance: V2 = 1.016089 V visible, instance label Low_AmpSd.

**S14** -- *Output waveform, DC (sized)*.
- Same DC sweep as S03 (adjust the range to about 0.95-1.1 V).
- Must be visible: marker at the 1.0 V crossing near X = 1.016089 V (ProjectState: trip point 1.016089 V; out = 0.981 V at that bias, so a second marker at X = 1.016089 V should read about 0.981 V). [CHECK: ProjectState defines the trip as the bias value used, so the 1.0 V crossing may be slightly above 1.016 V; write whatever the marker reads and tell me.]

**S15** (value, optional picture) -- *Power calculation, table cell "DC-bias power, sized"*.
- Same as S04 for the sized circuit at V2 = 1.016089 V. Write the V0 current in the report table (the cell marked [TO FILL]). 2 V x that current = DC power.

**S16** -- *Output waveform, AC (sized)*.
- Same AC run as S05. Marker at the lowest frequency.
- Must be visible: about 46.66 dB.

**S17** -- same section.
- Marker at the 0 dB crossing in the gain plot and the same frequency in the phase plot.
- Must be visible: 0 dB at about 1.726 MHz, phase about -90.005 deg at about 1.728 MHz (PM about 90.0 deg).

## G3. Test bench `low_amp1_tran` (follower, transient): baseline, sized

ADE L settings for this bench: tran, stop 40u, accuracy moderate. Input: vpulse on vin+ (0.8 V to 1.2 V, delay 1u, rise/fall 10n, width 10u, period 20u), output tied to vin-. Model section **mc** for both versions (confirmed by the student: every non-PVT run is mc).

### G3a. Baseline
Swap the instance to `Low_AmpSd_base`. `X`. Netlist -> Recreate. Run.

**S07** -- *Screenshot of the simulator based circuit implementation*.
- Schematic of `low_amp1_tran` with the base instance: out tied to vin-, vpulse parameters readable (Voltage 1 0.8, Voltage 2 1.2, Delay 1u, Rise 10n, Fall 10n, Pulse width 10u, Period 20u) and V0 = 2 V. If the vpulse values are not readable, add a second picture of the vpulse properties (press `q` on the source, then Cancel).

**S08** -- *Output waveform, transient (baseline)*.
- Plot `vin+` and `out` (Outputs -> To Be Plotted -> Select On Design: the vin+ net and out net). Put four markers on the 1.0 V crossings: input rising near 1.005 µs, output rising near 1.1762 µs, input falling near 11.015 µs, output falling near 11.2699 µs.
- Must be visible: the full pulse (0 to 40 µs) and the zoom in two details if needed (one at the rising edge, one at the falling edge, as S08a, S08b). Marker times must be legible. These give tPLH = 171.2 ns, tPHL = 254.9 ns, tp = 213 ns. Also visible: the output settling about 28 mV below the input.

**S09** -- *Power calculation (baseline)*.
- Calculator (Tools -> Calculator) with the expression `average(IT("/V0/PLUS"))` evaluated, or the Results -> Print table.
- Must be visible: the value -12.3356 µA (sign: current leaves the + terminal of V0). Power in the report: 2 V x 12.3356 µA = 24.67 µW.

### G3b. Sized, section mc
Swap back to `Low_AmpSd`. `X`. Netlist -> Recreate. Run with section mc.

**S18** -- *Screenshot of the circuit based on sizing concept (test bench)*.
- `low_amp1_tran` with the sized instance.

**S19** -- *Output waveform, transient (sized)*.
- Same markers as S08.
- Must be visible: tPLH = 120.0 ns, tPHL = 116.6 ns (input crossings at 1.005 µs / 11.015 µs, outputs about 120 ns and 116.6 ns later). The rise and fall delays are almost equal.

**S20** -- *Power calculation (sized)*.
- Same expression as S09.
- Must be visible: -16.354 µA (power 32.71 µW, PDP 3.87 pJ in the report).

## G4. PVT runs (sized circuit in `low_amp1_tran`)

Do all three runs in one sitting. The model section is changed in ADE L -> Setup -> Model Libraries (select the gpdk045.scs line and change the Section column: tt, ss, ff); temperature in Setup -> Temperature; VDD by editing V0 (DC voltage) in the schematic. After each change: `X` if you edited the schematic, Netlist -> Recreate, Run.

**S21** -- *Screenshot of the PVT analysis*.
- One picture of the ADE L Model Library Setup form with the section visible, plus the ADE main window with the temperature visible (take it once while you run case A or B).

**S22** -- Nominal: tt, 27 C, V0 = 2.0 V.
- Waveform with the delay markers and the average-current value in one window if possible.
- Must be visible: tPLH 82.1 ns, tPHL 119.7 ns (tp 100.9 ns), avg current -16.227 µA (power 32.45 µW).

**S23** -- Case A slow: ss, 125 C, V0 = 1.8 V.
- Must be visible: tPLH 153.8 ns, tPHL 234.3 ns (tp 194.0 ns), avg current -9.065 µA (power 1.8 V x 9.065 µA = 16.32 µW). Make sure the plot title or the ADE window shows ss, 125 and 1.8 V.

**S24** -- Case B fast: ff, -40 C, V0 = 2.2 V.
- Must be visible: avg current -35.23 µA (power 2.2 V x 35.23 µA = 77.51 µW).
- Delay was not measured before; if you have time place the four 1.0 V markers and write the delay in the PVT table (cell marked [TO FILL]).

**S25** -- one summary picture.
- Either the three waveforms overlaid in one window (use "Overlay"/keep previous results, [CHECK]) or a Windows Paint collage of S22-S24 with the case names. Optional: Case C (tt, 125 C, 2.0 V) if you want to fill that row.

After G4: reset to mc, 27 C, V0 = 2.0 V.

## G5. Layout (Sld_80/Low_AmpSd/layout)

**S26** -- *Screenshot of the layout*.
- Open the layout, press `f` to fit, then Shift+F (show all levels) so that the device shapes are visible. Keep the LSW (layer window) visible if you can.
- Must be visible: the whole layout: three rows of devices, the pins vdd, vin-, vin+, out, vss, and the rails.

**S27** -- *Screenshot of the layout*.
- Options -> Display -> Show Name Of: instances (so the labels M0 to M15 are drawn). `f`.
- Must be visible: instance names in the placement (top PMOS row M7 M8 M11 M12 M15 M13 M14; middle row M0 M9 M10 M1 M3; bottom row M2 M6 M5 M4).

**S28** -- zoom on the pins and rails.
- Zoom in on the top left (vdd pin and rail, vin pins) and the bottom (vss rail). One picture of each corner if needed.

**S29** (optional) -- connectivity.
- Annotation Browser / Connectivity showing 0 incomplete nets, 0 shorts [CHECK: ProjectState section 6c says "Annotation Browser Connectivity = 0/0"]; or the Route -> Automatic Routing result message (11/11 and 2/2, 0 opens, 0 shorts).

## G6. DRC (do S31 first, before you start fixing)

**S31** -- *Problems faced / layout*, BEFORE any fix.
- Assura -> Run DRC (Run Name e.g. `drc_start`, Run Directory `.`, Rules File `/home/install/FOUNDRY/analog/45nm/assura/assuraDRC.rul`), then open the error layer window (ELW).
- Must be visible: the ELW with the list of the 13 errors by rule (OXIDETHK.SP.1 1, CONT.SE.3 2, CONT.SE.4 2, METAL1.SP.1.1 3, METAL1.SP.1.2 2, METAL1.SP.1.3 3).

**S30** -- the Run DRC form with the rules file path visible (take it while starting the run above).

**S32** -- *Layout / final DRC*.
- After the fixes (Morning_Guide.md part 1), the final run: the Assura message window or ELW showing no errors ("0 errors"/"no violations", [CHECK] exact wording). If errors remain, take the ELW with the remaining rule list instead and tell me; the report text must say what remains.

## G7. LVS

**S33** -- the Run LVS form: Schematic design Sld_80/Low_AmpSd/schematic, Layout design Sld_80/Low_AmpSd/layout, Extract rules `/home/install/FOUNDRY/analog/45nm/assura/extract.rul`, Compare rules `/home/install/FOUNDRY/analog/45nm/assura/compare.rul`.

**S34** (optional but useful, goes into *Problems faced*) -- the FIRST LVS result, if it shows mismatches (for example I0 and C0 only in the schematic): the LVS result/debug window with the mismatch summary.

**S35** -- *final LVS*: the result window after the fixes (message "schematic and layout match" [CHECK exact wording], or the final status if it does not match). Include the cell summary (devices and nets counts, pin count).

## G8. Parasitic extraction (PEX)

**S36** -- Quantus (or Assura RCX) run form with the settings (extraction type, LVS run name, output view name).

**S37** -- Library Manager showing the new extracted view under Sld_80 / Low_AmpSd (for example `av_extracted`).

**S38** -- the extracted view opened (layout with parasitic info / or the extracted schematic-like view): any recognisable picture that shows the extracted cellview name in the title bar.

## G9. Post-layout simulation (extracted view in the same test benches)

Use the same settings as the schematic runs you compare with (section mc, 27 C, V0 = 2.0 V), see Morning_Guide.md part 3.

**S42** -- ADE L showing how the extracted view is selected: Setup -> Environment, Switch View List with the extracted view name first (or the config view window with Low_AmpSd bound to the extracted view).

**S39** -- *Output waveform for the layout, AC*: `low_amp1` with the extracted view. Markers like S16 and S17: low-frequency gain and the 0 dB crossing with the phase at that frequency.

**S40** -- *Output waveform for the layout, transient*: `low_amp1_tran` with the extracted view. The same four markers as S19 on the 1.0 V crossings, so that tPLH and tPHL can be read.

**S41** -- the average-current calculator value for the extracted view (`average(IT("/V0/PLUS"))`).

After G9: switch the test benches back to the schematic view (remove the extracted view from the switch view list) so that nothing stays pointing at the layout.

## Quick reference: report section -> screenshots

| Report section | Screenshots |
|---|---|
| Circuit diagram | S43, S01 |
| Screenshot of the simulator based circuit implementation | S01, S02, S07 |
| Waveform, DC and transient (no sizing) | S03, S04, S05, S06, S08, S09 |
| Circuit with sizing | S10, S11, S12, S13, S18 |
| Waveform, DC and transient (with sizing) | S14, S15, S16, S17, S19, S20 |
| Table power/delay/PDP (proof) | S09, S20, S08, S19 (plus S05, S06, S16, S17 for gain/GBW) |
| PVT | S21, S22, S23, S24, S25 |
| Layout | S26, S27, S28, S29, S30, S31, S32 |
| LVS and PEX | S33, S34, S35, S36, S37, S38 |
| Waveform for the layout | S39, S40, S41, S42 |
