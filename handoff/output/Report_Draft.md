>> AMRITA SCHOOL OF ENGINEERING, BENGALURU
>> DEPARTMENT OF ELECTRONICS & COMMUNICATION ENGINEERING
>> B.TECH. V SEMESTER (ECE AND EAC) AY 2026-2027
>> ASSIGNMENT FOR 23ECE302 VLSI DESIGN
>> SYSTEM DESIGN FOR 23ECE383 VLSI DESIGN LABORATORY
>> REPORT
>> JULY TO NOVEMBER 2026
>> 
>> DESIGN AND SIMULATION OF A LOW-POWER CMOS OPERATIONAL AMPLIFIER WITH A CASCADE SECOND STAGE (FIG. 2) IN 45 nm gpdk045 TECHNOLOGY [CHECK: title wording]
>> 
>> Submitted by
| REGISTER NUMBER | NAME | SIGNATURE WITH DATE |
|---|---|---|
| [TO FILL: register number] | [TO FILL: name] | [TO FILL] |
| [TO FILL: register number] | [TO FILL: name] | [TO FILL] |
| [TO FILL: register number] | [TO FILL: name] | [TO FILL] |
| [TO FILL: register number] | [TO FILL: name] | [TO FILL] |
>> 
>> BATCH NUMBER: [TO FILL]
>> 
>> FACULTY EXAMINER SIGNATURE WITH EVALUATION DATE: ____________________
<<PAGEBREAK>>

## TITLE OF THE SYSTEM DESIGN PROJECT:
Design and Simulation of a Low-Power CMOS Operational Amplifier with a Cascade Second Stage (Fig. 2 of the reference paper) in 45 nm gpdk045 Technology: Schematic, Sizing, PVT Analysis and Layout. [CHECK: edit the wording to match what your faculty approved]

## TITLE OF THE PAPER:
Low-Power CMOS Operational Amplifier Design in 45nm Technology

## DETAILS OF THE PAPER (SOURCE OF THE TITLE):
- Authors: Debjyoti Chowbey and Ratul K. Baruah, Department of Electronics and Communication Engineering, Tezpur University, Tezpur, India.
- Published in: 2025 Devices for Integrated Circuit (DevIC), 5-6 April 2025, Kalyani, India, pp. 528-533. IEEE, ISBN 979-8-3503-9110-7.
- DOI: 10.1109/DevIC63749.2025.11012572 (IEEE Xplore).
- Circuit assigned to this project: Fig. 2 of the paper, "Cascade Second Stage Topology for improved gain in weak inversion region" (assigned by Dr. Kaveri Hatti). Only this circuit (16 transistors, a bias current source and a load capacitor) is implemented here. The 29-transistor full design of the paper (Fig. 3) is outside the scope of this project.
- Paper specification targets (Table I of the paper): VDD = 2.0 V, power consumption < 20 µW, open-loop gain >= 60 dB, GBW >= 2.0 MHz, slew rate >= 2.5 V/µs, phase margin >= 50°, rail-to-rail input common-mode range and output swing.
- Headline results claimed by the paper (for the full Fig. 3 design, not for Fig. 2 alone): gain 66.85 dB, GBW 2.31 MHz, power 12.5 µW, slew rate 2.5 V/µs. These are quoted for reference only and are not the results of this project.

## CIRCUIT DIAGRAM:
The circuit implemented is Fig. 2 of the paper: a differential input stage whose outputs are copied by current mirrors into a cascoded (cascade) second stage that drives the output node.

[SCREENSHOT S43: Fig. 2 of the paper, cropped from the PDF (page 2), with the caption "Fig. 2 of [1]" - reproduced for reference with citation]

[SCREENSHOT S01: schematic window of Sld_80/Low_AmpSd_base (the unsized circuit), full circuit visible, all 16 transistors, I0 and C0 readable]

Table 1 lists the connectivity of the circuit as built in Virtuoso (taken from the Spectre netlist of the schematic; D = drain, G = gate, S = source, B = body). The Virtuoso device names differ from the paper's names; the mapping below was inferred from the topology.

| Virtuoso | Paper | Type / role | D, G, S, B nets | W / L baseline | W / L sized |
|---|---|---|---|---|---|
| M9 | M1 | NMOS input pair, vin- [g45n2svt] | b2, vin-, b1, vss | 320n / 150n | 1.6u / 150n |
| M10 | M2 | NMOS input pair, vin+ [g45n2svt] | b3, vin+, b1, vss | 320n / 150n | 1.6u / 150n |
| M8 | M3 | PMOS diode load (b2) [g45p2svt] | b2, b2, vdd, vdd | 320n / 150n | 320n / 150n |
| M11 | M4 | PMOS diode load (b3) [g45p2svt] | b3, b3, vdd, vdd | 320n / 150n | 320n / 150n |
| M7 | M8 | PMOS mirror of M8 into M2 [g45p2svt] | net14, b2, vdd, vdd | 320n / 150n | 320n / 150n |
| M12 | M6 | PMOS pull-up mirror [g45p2svt] | net48, b3, vdd, vdd | 320n / 150n | 640n / 300n |
| M15 | M15 | PMOS cascode pull-up [g45p2svt] | out, net28, net48, vdd | 320n / 150n | 640n / 300n |
| M13 | M12 | PMOS diode (cascode bias) [g45p2svt] | net28, net28, vdd, vdd | 320n / 150n | 320n / 150n |
| M14 | M11 | PMOS mirror of M13 (b4) [g45p2svt] | b4, net28, vdd, vdd | 320n / 150n | 320n / 150n |
| M3 | M14 | NMOS sink for M13 [g45n2svt] | net28, b1, vss, vss | 320n / 150n | 320n / 150n |
| M2 | M9 | NMOS diode (net14) [g45n2svt] | net14, net14, vss, vss | 320n / 150n | 320n / 150n |
| M6 | M7 | NMOS pull-down [g45n2svt] | net39, net14, vss, vss | 320n / 150n | 640n / 300n |
| M5 | M16 | NMOS cascode pull-down [g45n2svt] | out, b4, net39, vss | 320n / 150n | 640n / 300n |
| M4 | M13 | NMOS diode (b4) [g45n2svt] | vss, b4, b4, vss | 320n / 150n | 320n / 150n |
| M0 | M10 | NMOS bias diode (b1) [g45n2svt] | b1, b1, vss, vss | 320n / 150n | 320n / 150n |
| M1 | M5 | NMOS tail / bias (shorted to b1) [g45n2svt] | b1, b1, vss, vss | 320n / 150n | 320n / 150n |

Table 1: device connectivity and sizes (from the Spectre netlists of the baseline and sized schematics; I0 = isource 2 µA from vdd to b1, C0 = 1 pF from out to vss).

Net names: b1 is the bias/tail node, b2 and b3 are the diode-connected PMOS load nodes, b4 is the bias node for the lower cascode, net14 is the diode node of the NMOS mirror M2, net28 is the bias node of the upper cascode, net48 and net39 are the intermediate nodes of the upper and lower cascode branches. Ibias = 2 µA flows from vdd into b1 (I0) and the load capacitor C0 = 1 pF sits between out and vss.

## THEORY AND WORKING PRINCIPLE:
**Why low power and why moderate/weak inversion.** The power dissipation of a circuit is P = VDD x Itotal (eq. (1) of the paper), so low power requires a small supply, a small total current, or both. In the 45 nm node the supply headroom is small, so the paper biases the transistors in weak or moderate inversion, where the drain current is exponentially related to the gate-source voltage (eq. (2) of the paper) and the transconductance per unit current is highest. The price is lower speed and a larger device area [1].

**Working of the circuit as built.** The numbering below uses the Virtuoso names, with the paper's names in brackets.
1. **Bias.** A 2 µA current source (I0) feeds the node b1. The diode-connected NMOS devices M0 (M10) and M1 (M5) are tied to b1 and set the bias voltage; M3 (M14) has its gate on b1 and mirrors the bias current into the cascode bias branch. As drawn in the paper, the tail node of the input pair and the bias node b1 are the same node, so the tail current follows the bias branch.
2. **Differential input stage.** The NMOS pair M9 (M1, vin-) and M10 (M2, vin+) shares the source node b1. Their drains feed the diode-connected PMOS loads M8 (M3, node b2) and M11 (M4, node b3). A differential input voltage steers the tail current between the two branches, so the branch currents become unequal.
3. **Mirrors to the output stage.** M7 (M8) mirrors the left-branch current (gate b2) into the diode-connected NMOS M2 (M9, node net14); M6 (M7) mirrors net14 and becomes the pull-down current. On the other side, M12 (M6) mirrors the right-branch current (gate b3) and becomes the pull-up current. The output current is therefore proportional to the difference of the two branch currents, which is the "push-pull" action the paper describes for Fig. 1.
4. **Cascode (cascade) second stage.** The pull-up mirror M12 is stacked with the cascode device M15 (gate on net28), and the pull-down mirror M6 is stacked with the cascode device M5 (M16, gate on b4). Cascoding raises the output resistance seen at `out` because the cascode device shields the mirror transistor from the output voltage swing. The bias voltages for the cascodes come from two diode-connected devices: the PMOS M13 (M12) on node net28, whose current is sunk by M3 and which sets the gate of the upper cascode M15; and the NMOS M4 (M13) on node b4, which receives a copy of that current through the mirror M14 (M11) and sets the gate of the lower cascode M5. The paper states that this raises the gain by raising the output resistance without extra power [1].
5. **Load.** The load capacitor C0 = 1 pF at the output sets the dominant pole of the amplifier.

**Gain expression.** For the Fig. 1 push-pull stage the paper gives (eq. (3)) A_v = gm1 (S6/S4) / (gds6 + gds7), where gm1 is the transconductance of the input pair, S6/S4 is the mirror size ratio and gds are the output conductances at the output node. For the cascode version, eq. (4) of the paper expresses the gain in terms of the bias currents, the mirror ratio b = (M6 to M4 size ratio), the thermal voltage Vt, the channel-length-modulation factors lambda_n and lambda_p and the subthreshold slope factors n_n and n_p. [CHECK: retype eq. (4) from the PDF; the text extracted from the PDF is garbled, so it is not copied here.] In words: the gain is (input-pair gm x current ratio) x (output resistance), and the cascode increases the output resistance roughly from r_o to gm x r_o x r_o on each side [CHECK: standard result, cite Allen and Holberg [4]]. In weak inversion gm = I_D / (n Vt), so the input-pair gm is limited by the bias current, and more gain has to come from the output resistance.

**Dynamic (adaptive) tail biasing.** The paper's full design (Fig. 3, not implemented here) adds extra mirrors that boost the tail current when a differential input is present (eqs. (5)-(9) of the paper). This is out of scope for this project.

**Why sizing changes the results (reasoning used for the sizing step).** The sizing applied in this project had two ideas: (i) widen the input pair M9/M10 from 320 nm to 1.6 µm at the same length of 150 nm, which increases the W/L of the pair five times so the pair operates at a higher gm/I_D (more weakly inverted) and gives more transconductance, and therefore more gain and a higher GBW (GBW is about gm / (2 pi CL) for a single dominant pole at the output); (ii) lengthen the output and cascode devices M5, M6, M12 and M15 from 150 nm to 300 nm, with the width doubled to 640 nm so that W/L stays the same (about 2.13), which reduces channel-length modulation (larger r_o) and therefore increases the output resistance and gain. The results in Table 2 agree with the direction of these arguments (gain and GBW went up, delay went down), but the measured power also went up. The reason for the power increase was not isolated in this work [CHECK: possible cause is the larger devices drawing more current in the self-biased loop, to be confirmed by comparing the DC currents of the two versions].

## TOOL & TECHNOLOGY USED:
- **Operating system and computer:** Red Hat Linux lab workstation, accessed remotely.
- **Cadence Virtuoso 6.1.8 (64-bit):** Schematic Editor for entry, Analog Design Environment ADE L for DC, AC and transient analyses and the calculator for measurements, Spectre as the circuit simulator (relative tolerance 1e-3, temperature 27 C unless stated otherwise).
- **Layout:** Virtuoso Layout Suite XL, with connectivity-driven layout from the schematic and the Virtuoso Space-based Router for routing.
- **Verification and extraction:** Assura DRC and Assura LVS, Quantus (parasitic extraction, PEX) [CHECK: confirm which extractor is finally used].
- **Technology:** gpdk045, the Cadence 45 nm generic PDK. Devices: `nmos2v` (model g45n2svt) and `pmos2v` (model g45p2svt), the thick-oxide 2 V devices. Baseline size W = 320 nm, L = 150 nm, m = 1 for every transistor. Supply VDD = 2.0 V. Model sections available: tt, ff, ss, fs, sf, mc. All DC, AC and transient results (without sizing, with sizing and post-layout) use section mc; tt, ss and ff are used only for the PVT analysis.
- **Library and cells:** library Sld_80 with cells `Low_AmpSd` (op-amp, schematic and symbol), `Low_AmpSd_base` (unsized backup), `low_amp1` (DC and AC test bench) and `low_amp1_tran` (unity-gain follower transient test bench).
- **Documents and scripts:** reports and tables compiled with Python (python-docx); arithmetic (power, PDP, percentages) rechecked in Python.

**Test benches.**
- `low_amp1`: V0 = 2 V on vdd; vss at ground; V2 on vin+ with a DC value equal to the trip-point bias (1.028 V baseline, 1.016089 V sized) and AC magnitude 1; V3 on vin- = 1 V DC. Used for the DC sweep and the AC analysis. The 1 pF load C0 and the 2 µA bias source I0 are inside `Low_AmpSd`.
- `low_amp1_tran`: unity-gain follower (out tied to vin-); vpulse on vin+ from 0.8 V to 1.2 V, delay 1 µs, rise and fall time 10 ns, pulse width 10 µs, period 20 µs; transient stop time 40 µs, moderate accuracy. Used for delay, average power and PVT.
- Measurement method (the same for both versions): delay tp = average of tPLH and tPHL, measured between the 1.0 V crossings of the input and the output; average supply current from the calculator expression `average(IT("/V0/PLUS"))`; power = VDD x average current; PDP = power x tp. For AC, the expressions `dB20(VF("/out"))` and `phase(VF("/out"))` were plotted with a 1 Hz to 1 GHz sweep at 20 points per decade.

## SCREENSHOT OF THE SIMULATOR BASED CIRCUIT IMPLEMENTATION:
Baseline (unsized) circuit, all transistors W = 320 nm, L = 150 nm.

[SCREENSHOT S01: schematic of Sld_80/Low_AmpSd_base] (same as the circuit-diagram section; use one of the two places)

[SCREENSHOT S02: schematic of test bench low_amp1 with the Low_AmpSd_base instance, V0 = 2 V, V2 = 1.028 V (AC mag 1), V3 = 1 V visible]

[SCREENSHOT S07: schematic of test bench low_amp1_tran (follower, vpulse on vin+) with the Low_AmpSd_base instance, vpulse parameters visible]

## SCREENSHOT OF THE OUTPUT WAVEFORM OBTAINED FROM THE SIMULATOR (DC AND TRANSIENT):
**Baseline results (without sizing).**

*DC.* The DC sweep of vin+ (vin- = 1 V) shows a sharp, smooth S-shaped transition with the trip point at vin+ of about 1.028 V (read from the plot). At V2 = 1.028 V the output is 1.13 V DC (mid-rail) and the supply current of V0 is 7.943 µA, i.e. a DC power of 2 V x 7.943 µA = 15.886 µW (meets the < 20 µW target).

[SCREENSHOT S03: DC sweep of V2 (0.95 to 1.1 V or the range used), plot of out, marker at the 1.0 V crossing at vin+ = 1.028 V]

[SCREENSHOT S04: DC operating point / calculator showing the V0 supply current 7.943 µA]

*AC.* DC gain 44.6 dB (marker at 1.26 Hz), -3 dB point about 4 kHz, GBW (0 dB crossing) about 0.7 MHz (marker 708 kHz at -0.255 dB), phase -89.74° at 707.9 kHz, so the phase margin is about 90.3°. The gain is about 15 dB short of the 60 dB target and the GBW is about three times short of 2 MHz.

[SCREENSHOT S05: AC gain (dB20) of the baseline with a marker at 1.26 Hz reading 44.6 dB]

[SCREENSHOT S06: AC gain and phase of the baseline with a marker at the 0 dB crossing (about 708 kHz) and the phase reading -89.74 deg]

*Transient.* In the unity-gain follower the output settles about 28 mV below the input (systematic offset, consistent with the DC trip point at 1.028 V). The rising edge is fast and the falling edge is slow because the pull-down is weak with a bias current of only 2 µA. With the input crossing 1.0 V at 1.005 µs (rising) and 11.015 µs (falling), the output crosses 1.0 V at 1.1762 µs and 11.2699 µs, giving tPLH = 171.2 ns, tPHL = 254.9 ns and tp = 213 ns. The average supply current is -12.3356 µA (sign: current flows out of the + terminal of V0), so the transient average power is 2 V x 12.3356 µA = 24.67 µW (above the 20 µW target; the DC-bias power was 15.886 µW). PDP = 24.67 µW x 213 ns = 5.26 pJ.

[SCREENSHOT S08: transient waveform of low_amp1_tran (baseline), vin+ and out, markers at the 1.0 V crossings: in 1.005 us / out 1.1762 us (rising) and in 11.015 us / out 11.2699 us (falling)]

[SCREENSHOT S09: calculator / output table showing average(IT("/V0/PLUS")) = -12.3356 uA for the baseline]

## SCREENSHOT OF THE CIRCUIT BASED ON SIZING CONCEPT:
Sizing v1 (applied to Sld_80/Low_AmpSd; the unsized circuit is kept as `Low_AmpSd_base`):
- Input pair M9 and M10: W = 1.6 µm, L = 150 nm (was 320 nm / 150 nm).
- M5, M6 (NMOS) and M12, M15 (PMOS): W = 640 nm, L = 300 nm (was 320 nm / 150 nm).
- All other transistors unchanged (320 nm / 150 nm); Ibias still 2 µA; C0 = 1 pF.
These values were verified in the Spectre netlist of the sized schematic. The new trip point is vin+ = 1.016089 V (out = 0.981 V at that bias), so the systematic offset is smaller than in the baseline (1.028 V), a shift of 11.9 mV.

[SCREENSHOT S10: schematic of Sld_80/Low_AmpSd (sized), full circuit visible]

[SCREENSHOT S11: properties form (Q) of M9 or M10 showing W = 1.6u, L = 150n]

[SCREENSHOT S12: properties form (Q) of M5, M6, M12 or M15 showing W = 640n, L = 300n]

[SCREENSHOT S13: schematic of test bench low_amp1 with the sized Low_AmpSd instance and V2 = 1.016089 V visible]

[SCREENSHOT S18: schematic of test bench low_amp1_tran with the sized Low_AmpSd instance]

## SCREENSHOT OF THE OUTPUT WAVEFORM OBTAINED FROM THE SIMULATOR FOR THE CIRCUIT WITH SIZING CONCEPT (DC AND TRANSIENT):
**Results with sizing.**

*DC.* Trip point at vin+ = 1.016089 V.

[SCREENSHOT S14: DC sweep of the sized circuit, out vs V2, marker at the 1.0 V crossing / trip point 1.016089 V]

*AC.* DC gain 46.66 dB, GBW 1.726 MHz, phase -90.005° at 1.728 MHz, so the phase margin is about 90.0°. Compared with the baseline: +2.06 dB gain and GBW about 2.4-2.5 times larger, phase margin unchanged. The gain is still 13.34 dB below the 60 dB target and the GBW is 0.27 MHz below the 2 MHz target.

[SCREENSHOT S16: AC gain of the sized circuit, marker at low frequency reading 46.66 dB]

[SCREENSHOT S17: AC gain and phase of the sized circuit, marker at the 0 dB crossing (1.726 MHz) and phase -90.0 deg at about 1.728 MHz]

*Transient (model section mc).* tPLH = 120.0 ns, tPHL = 116.6 ns, tp = 118.3 ns; average current -16.354 µA, power 2 V x 16.354 µA = 32.71 µW; PDP = 3.87 pJ. The rise and fall delays are now almost equal, unlike the baseline.

[SCREENSHOT S19: transient waveform of the sized follower (section mc), vin+ and out, markers at the 1.0 V crossings showing tPLH = 120.0 ns and tPHL = 116.6 ns]

[SCREENSHOT S20: calculator / output table showing average(IT("/V0/PLUS")) = -16.354 uA for the sized circuit (section mc)]

For reference only, the PVT nominal run of the sized circuit (model section tt, 27 °C, 2.0 V) gives tPLH = 82.1 ns, tPHL = 119.7 ns, tp = 100.9 ns, average current -16.227 µA, power 32.45 µW and PDP 3.27 pJ (see the PVT section).

## PROVIDE THE VALUES FOR THE FOLLOWING ALONG WITH THE SCREENSHOTS AS PROOF:
**Table 2: without and with sizing (same measurement method and model section mc for both columns).**

| Parameter | Value without sizing | Value with sizing | Change |
|---|---|---|---|
| Power calculation: transient average power (2 V x average supply current) | 24.67 µW (avg. current 12.3356 µA) | 32.71 µW (avg. current 16.354 µA) | +32.6 % |
| Power calculation: DC-bias power at the trip point | 15.886 µW (7.943 µA) | [TO FILL: V0 DC current of the sized circuit] | |
| Delay calculation: tPLH | 171.2 ns | 120.0 ns | |
| Delay calculation: tPHL | 254.9 ns | 116.6 ns | |
| Delay calculation: tp = (tPLH + tPHL)/2 | 213 ns | 118.3 ns | -44.5 % |
| Power Delay Product (PDP = P x tp) | 5.26 pJ | 3.87 pJ | -26.4 % |
| DC gain | 44.6 dB | 46.66 dB | +2.06 dB |
| GBW | about 0.7 MHz | 1.726 MHz | about 2.4-2.5x |
| Phase margin | about 90.3° | about 90.0° | about the same |
| Trip point (vin+ for out = 1.0 V) | 1.028 V | 1.016089 V | -11.9 mV |

Proof screenshots: power S09 and S20; delay S08 and S19; gain and GBW S05, S06, S16, S17.

**Comparison with the paper specification (Table I of the paper).**

| Parameter | Specification | Without sizing | With sizing | Status after sizing |
|---|---|---|---|---|
| Supply VDD | 2.0 V | 2.0 V | 2.0 V | met |
| Power | < 20 µW | 24.67 µW (transient avg.); 15.886 µW (DC) | 32.71 µW (transient avg.) | not met in transient |
| Open-loop gain | >= 60 dB | 44.6 dB | 46.66 dB | not met (13.34 dB short) |
| GBW | >= 2.0 MHz | about 0.7 MHz | 1.726 MHz | not met (0.27 MHz short) |
| Phase margin | >= 50° | about 90.3° | about 90.0° | met |
| Slew rate | >= 2.5 V/µs | not measured | not measured | [TO FILL if measured] |
| ICMR, output swing | rail-to-rail | not measured | not measured | not evaluated |

## SCREENSHOT OF THE PVT ANALYSIS:
PVT (process, voltage, temperature) analysis was run on the **sized** circuit with the follower test bench `low_amp1_tran`, changing the model section, the temperature and VDD together. The corner sections available in the gpdk045 model file are tt, ff, ss, fs, sf and mc.

| Case | Section | Temp | VDD | tp | Power | PDP |
|---|---|---|---|---|---|---|
| Nominal | tt | 27 °C | 2.0 V | 100.9 ns (tPLH 82.1, tPHL 119.7) | 32.45 µW (avg. current 16.227 µA) | 3.27 pJ |
| A: slow | ss | 125 °C | 1.8 V | 194.0 ns (tPLH 153.8, tPHL 234.3) | 16.32 µW (avg. current 9.065 µA) | 3.17 pJ |
| B: fast | ff | -40 °C | 2.2 V | not measured | 77.51 µW (avg. current 35.23 µA) | n/a |
| C: tt, 125 °C, 2.0 V | tt | 125 °C | 2.0 V | not run | not run | not run |

Power at each corner = (VDD of that corner) x (average current). Observations: the delay changes by about 1.9 times between the nominal and the slow corner (194.0 ns / 100.9 ns); the power changes by about 4.7 times between the slow and the fast corner (77.51 µW / 16.32 µW). Power is the weak point: the 20 µW target is met only at the slow corner (high temperature and low VDD). Delay at the fast corner and Case C were not measured. [TO FILL if time permits: tp for case B and case C]

[SCREENSHOT S21: ADE L window with the model-library setup showing the section selection and the temperature / V0 values for the PVT runs]

[SCREENSHOT S22: nominal tt, 27 C, 2.0 V: transient with delay markers (tPLH 82.1 ns, tPHL 119.7 ns) and avg. current -16.227 uA]

[SCREENSHOT S23: slow ss, 125 C, 1.8 V: transient with delay markers (tPLH 153.8 ns, tPHL 234.3 ns) and avg. current -9.065 uA]

[SCREENSHOT S24: fast ff, -40 C, 2.2 V: transient waveform and avg. current -35.23 uA]

[SCREENSHOT S25: summary of the three PVT runs in one picture (for example the ADE results table or the three waveforms overlaid)]

## SCREENSHOT OF THE LAYOUT:
**Layout of the sized circuit (Sld_80/Low_AmpSd/layout).** The layout view was created with Layout XL (Launch -> Layout XL -> Create New; Connectivity -> Generate -> All From Source) in the gpdk045 technology.
- *Placement:* three rows following the floorplan sketch: top PMOS row M7, M8, M11, M12, M15, M13, M14; middle NMOS row M0, M9, M10, M1, M3 (M9 under M8 and M10 under M11 so that the input pair sits below its loads); bottom NMOS row M2, M6, M5, M4.
- *Pins:* Metal1 pins, vdd at the top, vin- and vin+ on the left, out on the right and vss at the bottom.
- *Rails:* vdd rail at the top and vss rails (a strap between the middle and bottom rows and a rail at the bottom, joined by a vertical link at the right edge), all on Metal1 drawing.
- *Device parameters:* body tie type Detached; PMOS top tap and NMOS bottom tap; gate connection PMOS bottom and NMOS top. A single merged Nwell rectangle covers the whole PMOS row.
- *Routing:* Route -> Automatic Routing -> All Nets routed the 11 signal nets (11/11, 0 opens, 0 shorts); vdd and vss were routed as selected nets (2/2, 0 opens, 0 shorts). The Annotation Browser reports connectivity 0/0 (no incomplete nets, no shorts).
- *DRC (Assura, rules file assuraDRC.rul):* the error count went from about 50 to 14 to 13 remaining at the time of this draft (rule list below). [TO FILL: final DRC status after the fixes]
- *LVS (Assura, extract.rul and compare.rul):* [TO FILL: LVS outcome and, if any, the remaining mismatches and how they were resolved]

DRC status at the time of this draft (13 errors left): OXIDETHK.SP.1 (1 error, thick-oxide active spacing >= 0.16 µm), CONT.SE.3 (2, gate contact to active >= 0.06 µm), CONT.SE.4 (2, 1.8 V gate contact to active >= 0.07 µm), METAL1.SP.1.1 (3, >= 0.06 µm), METAL1.SP.1.2 (2, >= 0.1 µm), METAL1.SP.1.3 (3, wide-metal spacing >= 0.25 µm). [TO FILL: replace with the final result]

[SCREENSHOT S26: complete layout of Low_AmpSd (press f to fit, Shift+F for all levels), all three rows and the pins visible]

[SCREENSHOT S27: layout with instance names shown (Options -> Display -> Show Name Of -> instance), so that M0-M15 are readable]

[SCREENSHOT S28: zoom on the pins and the vdd / vss rails]

[SCREENSHOT S31 (before fixing): Assura DRC error list showing the 13 errors]

[SCREENSHOT S30: Assura Run DRC form with the rules file path]

[SCREENSHOT S29 (optional): connectivity check showing 0 incomplete nets and 0 shorts / router result 11/11 and 2/2]

[SCREENSHOT S32 (final): Assura DRC result with no errors] [TO FILL: only if the final DRC is clean]

[SCREENSHOT S33: Assura Run LVS form with the schematic and layout cellviews and the two rule files]

[SCREENSHOT S34 (optional): first LVS result showing the mismatch caused by the ideal I0 and C0] [TO FILL]

[SCREENSHOT S35 (final): Assura LVS result window showing the match (or the final status)] [TO FILL: LVS outcome]

[SCREENSHOT S36-S38: Quantus extraction form, the extracted view in the Library Manager and the extracted view opened] [TO FILL: after PEX]

## SCREENSHOT OF THE OUTPUT WAVEFORM OBTAINED FROM THE SIMULATOR FOR THE LAYOUT:
Post-layout simulation uses the parasitic-extracted view of Low_AmpSd in the same test benches and the same measurement method as the schematic results. Both columns use model section mc, 27 °C, 2.0 V. Results below are placeholders until the extraction is done.

| Parameter | Schematic (sized) | Post-layout | Change |
|---|---|---|---|
| DC gain | 46.66 dB | [TO FILL: post-layout DC gain] | [TO FILL] |
| GBW | 1.726 MHz | [TO FILL: post-layout GBW] | [TO FILL] |
| Phase margin | about 90.0° | [TO FILL: post-layout PM] | [TO FILL] |
| tPLH | 120.0 ns | [TO FILL] | [TO FILL] |
| tPHL | 116.6 ns | [TO FILL] | [TO FILL] |
| tp | 118.3 ns | [TO FILL: post-layout tp] | [TO FILL] |
| Average supply current | 16.354 µA | [TO FILL] | [TO FILL] |
| Transient average power | 32.71 µW | [TO FILL] | [TO FILL] |
| PDP | 3.87 pJ | [TO FILL: post-layout PDP] | [TO FILL] |

[SCREENSHOT S39: AC gain and phase of the extracted view in low_amp1 with markers at the DC gain and the 0 dB crossing] [TO FILL]

[SCREENSHOT S40: transient waveform of the extracted view in low_amp1_tran with the 1.0 V crossing markers] [TO FILL]

[SCREENSHOT S41: average supply current of the extracted view] [TO FILL]

[SCREENSHOT S42: ADE setup showing that the extracted view is used (switch view list or config)] [TO FILL]

Expected effect (to be confirmed by the results): the extracted view adds wire resistance and capacitance, so the post-layout GBW and delay are expected to be somewhat worse than the schematic values. [CHECK: write the actual conclusion from the numbers]

## ANY OTHER RELEVANT INFORMATION:
**Deviations from the paper and limitations.**
1. Only Fig. 2 of the paper is implemented (16 transistors, Ibias and a load capacitor). The paper's headline figures (66.85 dB, 2.31 MHz, 12.5 µW) belong to the full Fig. 3 design with dynamic tail biasing and cannot be compared one-to-one with these results.
2. The paper reports no transistor sizes for Fig. 2 and no bias current in the text extracted for this project. W = 320 nm, L = 150 nm (baseline) and Ibias = 2 µA are choices made in this project. [CHECK: confirm that the paper gives no sizes]
3. gpdk045 thick-oxide (2 V) devices g45n2svt and g45p2svt were used, with VDD = 2.0 V as in Table I of the paper.
4. The paper's Fig. 2 omits some gate connections. The mirror diode connections were added following the paper's text (nets b1 to b4), and an NMOS input pair was used. The device mapping between Virtuoso names and the paper names is inferred from the topology.
5. The tail node of the input pair is shorted to the bias node b1, as it appears in the paper's drawing. An alternative reading (tail node separated from the bias node) was considered and not applied because the circuit works as drawn.
6. The gain, GBW and phase margin are measured with the 1 pF load C0 inside Low_AmpSd. A phase margin of about 90° means the response is close to a single-pole roll-off up to the unity-gain frequency. [CHECK: wording]
7. Process corners ss and ff were available and used for the PVT analysis; no corner limitation affected the study. The corner cases fs and sf, the nominal-voltage hot case (Case C) and the fast-corner delay were not simulated.
8. Slew rate, PSRR, CMRR, ICMR and output swing (Table I and Section III of the paper) were not evaluated in this project.
9. Inconsistency inside the paper: the phase margin is 57.78° in Section III-A and 68° in the Conclusion. [CHECK]
10. Delay definition used: propagation delay tp = (tPLH + tPHL)/2 between the 1.0 V crossings of the input and output of a unity-gain follower. The faculty may expect a different definition (for example settling time). [CHECK with faculty]
11. The simulation results are from the schematic (pre-layout) circuit except where marked as post-layout.

## CONCLUSION:
The Fig. 2 cascade second-stage amplifier of the reference paper was recreated in Cadence Virtuoso with the gpdk045 45 nm PDK. After correcting the bias source, the floating mirror gates and the input-pair type, the baseline circuit (all devices 320 nm / 150 nm, Ibias = 2 µA) gave a DC gain of 44.6 dB, a GBW of about 0.7 MHz, a phase margin of about 90°, a propagation delay of 213 ns and a transient average power of 24.67 µW (PDP 5.26 pJ).

Sizing (input pair widened to 1.6 µm, output and cascode devices lengthened to 300 nm) improved the gain by 2.06 dB to 46.66 dB, raised the GBW to 1.726 MHz (about 2.4-2.5 times), cut the delay by 44.5 % to 118.3 ns and reduced the PDP by 26.4 % to 3.87 pJ, at the cost of 32.6 % more power (32.71 µW). The sized circuit still misses three paper targets: the gain is 13.34 dB below 60 dB, the GBW is 0.27 MHz below 2 MHz and the transient power is above 20 µW. These misses are partly expected because the paper's headline numbers belong to the larger Fig. 3 design, and the bias current and sizes of Fig. 2 are not given in the paper, so they were chosen here.

The PVT study shows a large spread: the delay changes by about 1.9 times between the nominal and the slow corner and the power by about 4.7 times between the slow and the fast corner; the power target is met only at the slow corner. The layout was placed and routed with no open or shorted nets and is being cleaned of design-rule errors (13 errors remained at the time of this draft). [TO FILL: final DRC status, LVS result and the post-layout comparison, then update this paragraph]

## PROBLEMS FACED DURING THE IMPLEMENTATION:
1. VSS check-and-save error in the schematic.
2. Warning about a hanging `out` wire in a test bench.
3. Output stuck at 1.9989 V and flat for all vin+ (0 to 2 V) in the DC sweep.
4. Schematic changes not showing up in the netlist (stale netlist).
5. Gain far below the paper (44.6 dB against 60 dB) and GBW below 2 MHz in the baseline.
6. The direct-plot function gave empty windows for the AC plots in this installation.
7. Layout: five router shorts after drawing the rails.
8. Layout: 16 open body (B) terminals.
9. Layout: 40 gate-contact spacing errors from router-placed contacts.
10. Layout: 6 Nwell spacing errors.
11. Layout: about 50 DRC errors at the first run, with 13 remaining at the time of this draft (OXIDETHK.SP.1, CONT.SE.3, CONT.SE.4, METAL1.SP.1.1, METAL1.SP.1.2, METAL1.SP.1.3). [TO FILL: update]
12. LVS: the schematic contains the ideal parts I0 (idc, 2 µA) and C0 (pcapacitor, 1 pF) that do not exist in the layout. [TO FILL: describe the mismatch seen and how it was handled]

## PROBLEMS RESOLVED USING SOLUTIONS:
Each item gives problem -> cause -> solution.
1. **VSS check-and-save error** -> problem with the vss pin and the wire attached to it [CHECK: exact cause] -> set the pin direction to inputOutput and redrew the wire onto the pin.
2. **Hanging `out` wire warning** -> the `out` wire in the test bench has no further connection -> harmless; kept for plotting the output.
3. **Output stuck at 1.9989 V, flat for all vin+** -> the Spectre netlist showed three causes: (a) the bias source had no DC value, so Ibias was 0 A; (b) four floating gate nets (net4, net10, net44, net33) because the mirrors were not diode-connected; (c) the input pair M9 and M10 were PMOS instead of NMOS -> (a) set the idc source to 2 µA, (b) labelled the nets b1, b2, b3, b4 so that the mirrors are diode-connected, (c) changed the cell of M9 and M10 from pmos2v to nmos2v (Q -> Cell Name) with the body on vss.
4. **Stale netlist** -> a second ADE L session was attached to the Low_AmpSd cell -> ADE was used only from low_amp1 and the netlist was regenerated (Simulation -> Netlist -> Recreate).
5. **Shorted tail node (decision)** -> the paper's drawing has a dot joining the tail node and the bias node -> the circuit works as drawn, so the paper's drawing was followed and the alternative was not applied.
6. **Gain and GBW below target** -> the unsized devices have small gm and small output resistance -> sizing v1 (see the sizing section) raised gain to 46.66 dB and GBW to 1.726 MHz; the remaining gap is reported honestly in the conclusion.
7. **Empty plot windows for AC** -> the direct-plot function of this installation did not produce a plot -> the outputs were set up as expressions in ADE L (Outputs -> Setup) using dB20(VF("/out")) and phase(VF("/out")).
8. **Router shorts (5)** -> the rails were first drawn on the Metal1 fill purpose instead of the drawing purpose [CHECK: why the router then created shorts] -> the rails were redrawn on Metal1 drawing.
9. **Open body terminals (16)** -> the transistors had no body connection -> body taps (Bodytie Type = Detached) were added on every transistor.
10. **Gate-contact spacing errors (40)** -> the router placed M1_PO contacts too close to the active area -> set the pcell Gate Connection parameter to Top for NMOS and Bottom for PMOS.
11. **Nwell spacing errors (6)** -> every PMOS had its own n-well and the wells were too close -> drew one merged Nwell rectangle over the whole PMOS row.
12. **Remaining DRC errors** -> hand fixes in the Metal1 spacing and at the gate contacts (Route -> Fix Violations had already removed VIA1.X.1) -> [TO FILL: describe what was done and the final result]
13. **LVS with ideal I0 and C0** -> [TO FILL: chosen solution (ignore property, or moving I0 and C0 to the test benches and adding an ibias pin) and result]

## ANY OTHER COMMENT:
- The results above come from a simple one-step sizing; further sizing rounds were not done. Ideas that were not tried: lengthening more devices or increasing the mirror ratio of M12 against M11 for more gain (at the cost of more power), and a smaller Ibias to reduce power (at the cost of GBW).
- All numbers in this report are taken from the recorded simulation results; values still to be measured are marked [TO FILL] and doubtful statements are marked [CHECK]. Remove the markers before submitting.
- The student work was done on a lab workstation; the netlists of the baseline and the sized circuit are kept in the project folder for reference.

## REFERENCES:
[1] D. Chowbey and R. K. Baruah, "Low-Power CMOS Operational Amplifier Design in 45nm Technology," in Proc. 2025 Devices for Integrated Circuit (DevIC), Kalyani, India, 5-6 Apr. 2025, pp. 528-533, doi: 10.1109/DevIC63749.2025.11012572.
[2] Cadence Design Systems, Inc., Virtuoso Analog Design Environment, Virtuoso Schematic and Layout Suite, Spectre Circuit Simulator, Assura Physical Verification and Quantus Extraction documentation, as installed with the tools on the lab workstation.
[3] Cadence Design Systems, Inc., Generic Process Design Kit gpdk045 (45 nm) documentation and model files, as provided on the lab workstation (/home/install/FOUNDRY/analog/45nm/).
[4] P. E. Allen and D. R. Holberg, CMOS Analog Circuit Design, Oxford University Press. [CHECK: edition and year; cited for the cascode output resistance and weak-inversion transconductance concepts]
