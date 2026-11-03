# Morning guide: DRC -> LVS -> PEX -> post-layout simulation

Written for the Virtuoso 6.1.8 lab PC (user `train`, project `~/sld_proj`, library `Sld_80`). One step per numbered block. After each step there is a **Check** line (what you should see) and, where useful, a **Send me** line (what to paste in the chat so that I can help if it is not right).

I could not test any of this on your machine. Everything marked **[CHECK]** is my best knowledge of the Cadence menus; if a menu is named differently, look in the neighbouring menu and tell me what you see. Never guess a layer or a net: if you are not sure two shapes are the same net, check it first (Step 1.4).

Keys that work in your install (from CLAUDE.md): `u` undo, `X` check and save (schematic), `q` properties, `r` rectangle, `m` move, `s` stretch, `k` ruler (Shift+K clears all rulers), `f` fit window, Ctrl+F top level only, Shift+F all levels. The lab shell is csh/tcsh (no `2>/dev/null`).

## The one thing to decide before you start (important)

The schematic `Low_AmpSd` contains two ideal parts that have no layout: I0 (the 2 µA bias source, vdd -> b1) and C0 (1 pF, out -> vss). They are fine for simulation but make LVS fail, and **they also matter for PEX**: the extracted view is made from the layout, so it will not contain I0 or C0. If the extracted view has no bias current, the post-layout circuit is dead (output stuck, like the very first bug in your history).

- **Option A (ignore I0 and C0 only for LVS)** is quick, but it fixes LVS only. For post-layout simulation you would still have to add the bias current and the load from outside, and the extracted cell has no pin to inject the bias into.
- **Option B (move I0 and C0 to the test benches, add pin `ibias` on net b1)** fixes LVS, PEX and post-layout simulation in one go. It costs more work (schematic, symbol, two test benches, one pin in the layout).

**My recommendation: do Option B.** Option A is described in Step 2.3 in case you only want a quick LVS result first. If you choose A, you will still have to do B before part 3.

Suggested order: Part 1 (DRC, because the geometry changes) -> Part 2 (LVS on the final geometry) -> Part 3 (PEX and post-layout). Do the backup in Step 0 first.

## Step 0. Backups and the "before" screenshot (10 minutes)

0.1 **Backup the layout.** Library Manager (in the CIW: Tools -> Library Manager), library Sld_80, cell Low_AmpSd. Right-click the `layout` view -> Copy [CHECK], new name `Low_AmpSd` cell, view `layout_drc_start`. (Same trick as your `layout_preroute` / `layout_routed`.)
- Check: the new view appears in the list. Why: if a fix goes wrong you can go back.

0.2 **Backup the schematic** (needed for Option B): copy cell `Low_AmpSd` (all views) to `Low_AmpSd_pre_lvs`. Right-click the cell -> Copy, tick all views [CHECK].
- Check: `Low_AmpSd_pre_lvs` has schematic and symbol and layout.

0.3 Open `Sld_80/Low_AmpSd/layout` (double-click the `layout` view; open in Edit mode).
- Check: you see the placed and routed layout; the title bar says Layout Suite XL.

0.4 Take screenshot **S31** (DRC errors before the fixes) when you run DRC in Step 1.1.

## Part 1. Fix the 13 remaining Assura DRC errors

### Step 1.1 Run DRC and open the error list

1.1.1 In the layout window: **Assura -> Run DRC...**.
- Fill: Run Name `drc2`, Run Directory `.`, Technology `-undefined-` (as before), Rules File `/home/install/FOUNDRY/analog/45nm/assura/assuraDRC.rul`. Click OK.
- Check: a message "Assura DRC finished" [CHECK] and a question whether to view the results. Click **Yes**.

1.1.2 The **Error Layer Window (ELW)** opens (shows rule names with error counts).
- Check: you see the 13 errors: OXIDETHK.SP.1 (1), CONT.SE.3 (2), CONT.SE.4 (2), METAL1.SP.1.1 (3), METAL1.SP.1.2 (2), METAL1.SP.1.3 (3). Take screenshots **S30** (the Run DRC form) and **S31** (the ELW).

1.1.3 To jump to an error: click a rule in the ELW, then press the **right-arrow button** (next error). The layout window zooms to the red marker.
- To read what the rule means: use the **Explain** button or the rule text in the ELW [CHECK]. Select a rule and ask for the explanation; it often draws the dimension that is too small.

### Step 1.2 How to measure and fix (applies to all rules)

1.2.1 **Measure with the ruler:** press `k`, click at one edge, click at the other edge of the gap. The number in the status bar / ruler is the distance in µm. Press Shift+K to clear all rulers.
- Why: so you know by how much you have to move the shape.

1.2.2 **Know your fix tools:** `m` move (select the shape first, press `m`, click once to pick it up, click again to drop it; use the ruler `k` to check the new gap), `s` stretch (select an edge and drag), `r` rectangle on the right layer, Delete key to remove a selected shape, `u` undo.
- Keep the layer selection in the LSW (layer window): when you draw a Metal1 wire, select **Metal1 drawing** in the LSW first. Never draw on a `fill` purpose (that was your early shorts bug).
- Snap grid: if the shape will not land at a clean position, set Options -> Display... or the grid in the status bar so the X and Y snap spacing is the manufacturing grid [CHECK: gpdk045 grid is 0.005 µm].

### Step 1.3 Fix each rule (do one rule at a time, re-run DRC after each rule)

**1. OXIDETHK.SP.1 (1 error): thick-oxide regions too close, spacing must be >= 0.16 µm**
- Physical meaning: every transistor of your design is a thick-oxide (2 V, nmos2v / pmos2v) device, so it carries a thick-oxide marker (layer `OXIDETHK`). Two such regions that are less than 0.16 µm apart are an error, because the mask cannot resolve that gap.
- Locate: ELW -> OXIDETHK.SP.1 -> right-arrow. You will see the marker between two neighbouring devices (probably two transistors placed close in the same row, or a PMOS next to an NMOS).
- Fix (usual): move one of the two devices away by the missing distance (select the device, `m`). If the gap between the two regions is not an Nwell boundary, the **alternative** is to draw one rectangle on layer `OXIDETHK drawing` that covers the gap and merges the two regions (then there is no spacing to violate) [CHECK: merging is normally allowed when both devices are thick-oxide; ask me before doing it]. Moving a device means its wires follow only if they are attached; after the move re-check connectivity (Step 1.4.3).
- Check: after re-running DRC the rule disappears.

**2. CONT.SE.3 (2 errors) and CONT.SE.4 (2 errors): gate contact too close to active**
- Physical meaning: a gate contact is the small square that connects the poly gate to Metal1. If it sits too close to a transistor's active area (the source/drain diffusion), it can short or break during processing. Minimum distances: >= 0.06 µm (CONT.SE.3) and >= 0.07 µm for the 1.8 V/thick-oxide gate contact (CONT.SE.4). My guess is that the 2 + 2 errors are the **same two contacts** flagged by both rules [CHECK: look at whether the markers sit on the same spot].
- Locate: ELW -> CONT.SE.3 -> right-arrow; the marker sits between a contact (a square with a cross in Shift+F view) and an active edge of a neighbouring device.
- Fix (usual): select the contact together with its poly/Metal1 pieces (the router-placed M1_PO contact) and move it **away from the active region** by the missing distance, then extend the poly and the Metal1 connecting to it so the gate stays connected. Alternatively stretch (`s`) the poly end cap so the contact lands further out. Do not move the device: your pcell Gate Connection setting (PMOS Bottom, NMOS Top) already puts the contact outside the active region; the errors are most likely contacts the router placed near a **different** device.
- Check: marker gone; zoom in and confirm the poly still touches the contact and the Metal1 still touches the contact.

**3. METAL1.SP.1.1 (3 errors): Metal1 to Metal1 spacing >= 0.06 µm**
- Physical meaning: two Metal1 shapes that are closer than 0.06 µm. Typical cause: two parallel router wires too close, or a wire too close to a pin or to a rail.
- Locate: ELW -> METAL1.SP.1.1 -> right-arrow. Measure the gap with the ruler.
- Fix (usual): (a) if the two shapes are **different nets**: move one shape away (`m` or `s`) so the gap is >= 0.06 µm, without touching a third shape; (b) if the two shapes are the **same net** (a small notch or gap in one wire): fill the gap with a Metal1 drawing rectangle (`r`). Never join two different nets.
- Check: marker gone and no new marker appeared next to it.

**4. METAL1.SP.1.2 (2 errors): spacing >= 0.1 µm**
- Physical meaning: the larger spacing that applies between Metal1 shapes depending on their width or on how long they run side by side. [CHECK: exact condition from the rule text; use Explain]. In practice: the same kind of fix as rule 3 but the gap must be at least 0.1 µm.
- Fix: as rule 3, to the larger distance. If two long wires run parallel, move one of them.

**5. METAL1.SP.1.3 (3 errors): wide metal spacing >= 0.25 µm**
- Physical meaning: wide Metal1 shapes (the rails, the enlarged pins, big pads) need a larger gap to their neighbours (0.25 µm). This is the likeliest one to come from the **enlarged pins and rails** you drew (vdd, vss, vin+, vin-, out pins enlarged to roughly transistor-box size) sitting close to a router wire. [CHECK: confirm which shape is the wide one by measuring its width with `k`]
- Fix (usual): move the narrow router wire away from the wide shape until the gap is >= 0.25 µm; or reduce the width of the pin rectangle (stretch `s` its edge) so it is no longer "wide"; if the pin is only a label shape you may shrink it with `s` (keep the pin overlapping the wire it should connect to).
- Check: the pin still overlaps its net's wire (use Step 1.4.2 to confirm after the change).

### Step 1.4 After the fixes

1.4.1 Re-run **Assura -> Run DRC** with Run Name `drc3`, then open the ELW.
- Check: no errors; the message says no violations [CHECK wording]. Take screenshot **S32**. If new errors popped up next to the old ones, repeat Step 1.3 for them. If you get stuck for more than 20 minutes on one error, tell me the rule, the measured gap and a screenshot; then move on to LVS (LVS does not depend on DRC).

1.4.2 **Which net is a shape on?** Window -> Assistants -> Navigator [CHECK] -> Nets: click a net name (for example `b1`): its shapes highlight in the layout. Use this before you merge or move shapes.

1.4.3 **Make sure you did not break connectivity:** Annotation Browser / Connectivity should still say 0 incomplete nets and 0 shorts [CHECK: your earlier "Connectivity 0/0" check]. The definitive check is LVS (Part 2).

1.4.4 Save the layout: File -> Save (or the save icon). Backup: copy `layout` to `layout_drc_fixed` in the Library Manager. Take screenshots **S26, S27, S28** of the final layout now (see the checklist, group G5).

## Part 2. Assura LVS

### Step 2.1 Pre-flight

2.1.1 Open the schematic `Sld_80/Low_AmpSd/schematic`, press `X` (check and save).
- Check: 0 errors (warnings about names are OK).

2.1.2 Make sure the layout is saved (File -> Save) and has no unsaved changes (title bar has no `*`).

### Step 2.2 Option B first: move I0 and C0 out of the cell and add the `ibias` pin (recommended)

B.1 **Record what you have.** In the sized schematic note I0: analogLib `idc`, DC current 2u, PLUS on vdd, MINUS on b1; C0: 1 pF between out and vss. (The Spectre line is `I0 (vdd b1) isource dc=2u type=dc`; the bench value must stay 2 µA.)
- Why: you will recreate them in the test benches with identical values; the results must not change.

B.2 **Delete I0 and C0 from `Low_AmpSd` schematic** (click each, press Delete). In the same schematic **add a pin**: Create -> Pin... (key `p`), Pin Names `ibias`, Direction `inputOutput`, then place it and **wire it to the net b1** (for example to the wire that already has the label b1). `X`.
- Check: 0 errors. You may get a warning that the net has two names (b1 and ibias); that is allowed (the pin name wins). If instead you get an error, remove the label `b1` on the wire that the pin touches and keep the other `b1` labels: the other labels stay connected by name. [CHECK]
- Why: the bias current and the load capacitor are test-bench elements, not part of the circuit that is laid out.

B.3 **Update the symbol** so that it gets the new pin: in the schematic window Create -> Cellview -> From Cellview [CHECK; or Design -> Create Cellview -> From Cellview], View Name `symbol`, Tool/Data Type `Composer-Symbol`, OK; if it asks to overwrite the existing symbol, say yes (the pin `ibias` is added; your backup `Low_AmpSd_pre_lvs` has the old one). Open the symbol (Library Manager -> symbol) and check the new pin `ibias` is drawn on the box (move it to a free side with `m` if it overlaps another pin); save.
- Check: the symbol has six pins: out, vdd, vin+, vin-, vss, ibias.

B.4 **Update both test benches** `low_amp1` and `low_amp1_tran`:
1. Open the bench; the instance of Low_AmpSd should show a warning or have the old pin count. Select the instance and use Edit -> Replace... [CHECK] or delete it and place a fresh one with `i` (Library Sld_80, Cell Low_AmpSd, View symbol). Reconnect the old five wires; wire the new pin `ibias` to a new source below.
2. Place analogLib **idc** (`i`, Library analogLib, Cell idc, View symbol): PLUS to the vdd net (the + of V0), MINUS to the `ibias` pin; press `q` and set **DC current = 2u**. Name it `I1` (the instance of Low_AmpSd is already called I0 in the bench).
3. Place analogLib **cap** (`i`, Library analogLib, Cell cap): between the `out` net and ground; press `q`, **Capacitance = 1p**.
4. `X` in each bench.
- Check: 0 errors in both benches. Open ADE L, Simulation -> Netlist -> Recreate, then Netlist -> Display and look for the lines `I1 (...) isource dc=2u` and `capacitor c=1p`, and that the instance of Low_AmpSd has six nets.
- **Regression test:** run the DC sweep, AC and transient again with the **same settings** as before (section tt, 27 C, V0 = 2.0 V, V2 = 1.016089 V). Expected: trip point 1.016089 V and the AC gain 46.66 dB, GBW 1.726 MHz (the same numbers as before, ProjectState section 6b). **If they differ, stop and tell me** (probably the idc direction or the capacitor is wrong).

B.5 **Add the `ibias` pin in the layout.**
1. In the layout (Layout XL): Connectivity -> Update -> Components and Nets [CHECK]. This brings the new pin `ibias` and removes I0/C0 from the source. Check the message window: no errors; the Navigator now lists `ibias` among the pins.
2. Create the pin shape: Create -> Pin... [CHECK; or Create -> Shape -> Pin]. Terminal Names `ibias`, Mode rectangle, Layer `Metal1` purpose `pin`, I/O type inputOutput. Draw a small rectangle **on top of an existing Metal1 wire of net b1** (use the Navigator to highlight net b1, choose a spot with free space around it, for example on the b1 wire near the M0/M1 gate connection). Keep it at least the spacing rules away from other nets (0.1 µm, 0.25 µm to wide shapes) to avoid new DRC errors.
3. If the pin cannot sit on an existing b1 wire without a spacing error, place it in a free area and connect with Route -> Automatic Routing -> Selected Nets after selecting `b1` in the Navigator; or draw a short Metal1 drawing wire to a b1 shape [CHECK].
4. Save and re-run Assura DRC (Step 1.4.1) to make sure the new pin created no DRC error.
- Check: DRC clean again, Connectivity 0/0.

### Step 2.3 Option A (quick, LVS only; use instead of Step 2.2 only if you want a first LVS result fast)

A.1 In the schematic select I0, press `q`, look for a property called `lvsIgnore` (some Cadence setups spell it `lvsIgnore` with value `TRUE`, or the check box "LVS Ignore") [CHECK: this depends on the Assura version; the property may not exist on analogLib `idc` and `pcapacitor`]. If it is not in the list, press **Add** in the form, name `lvsIgnore`, type `string`, value `TRUE`, OK. Do the same for C0. `X`.
A.2 Run LVS (Step 2.4). If I0 and C0 are still reported as extra devices in the schematic, the property is not honoured in this version; then use Option B.
A.3 Remember that the extracted view will lack I0 and C0 (see the top of this guide); you will need Option B for Part 3.

### Step 2.4 Run LVS

2.4.1 In the layout window: **Assura -> Run LVS...**
- Fill: Run Name `lvs1`; Run Directory `.`
- Schematic design: Library `Sld_80`, Cell `Low_AmpSd`, View `schematic`.
- Layout design: Library `Sld_80`, Cell `Low_AmpSd`, View `layout`.
- Rule files: Extraction rules (extract) `/home/install/FOUNDRY/analog/45nm/assura/extract.rul`; Compare rules (compare) `/home/install/FOUNDRY/analog/45nm/assura/compare.rul`. Technology `-undefined-` (as in DRC) [CHECK].
- Leave the other options at their defaults. Take screenshot **S33** of the form, then OK.
- Check: the run starts; a dialog "Assura LVS finished" [CHECK] appears after some seconds.

2.4.2 **Read the result.**
- **"Schematic and Layout Match"** (or similar): done. Take screenshot **S35** of the result window (include the summary of devices, nets and pins) and the LVS result pop-up. Go to Part 3.
- **"Schematic and Layout do not match"**: take screenshot **S34** (first run), click to open the LVS debug / results window [CHECK: Assura -> Open Run... or the "View" button in the finish dialog]. Look at the **Cell Summary** (counts of devices, nets and pins in layout vs schematic) first, then the list of mismatches (unmatched nets, unmatched devices, pin mismatches). Select an entry to highlight it in the layout and schematic ("Probe"/cross-highlight) [CHECK]. You can also list the run folder in the terminal: `cd ~/sld_proj` then `ls lvs1` (csh; no `2>/dev/null`), and look at the files ending in `.csm` and `.cls` [CHECK: file names].
- **Send me** the Cell Summary numbers and the first three mismatch lines if it does not match.

2.4.3 **Common mismatches to expect (my guesses, [CHECK] each against your result):**
1. *Two extra devices in the schematic (I0 isource, C0 capacitor)*: Option A/B not done or not honoured. Fix with Step 2.2.
2. *Pin `ibias` only in the schematic* or *only in the layout*: you did Option B in the schematic but not in the layout (or the reverse). Fix with Step B.5 and Update Components and Nets.
3. *Pin names do not match* (`vin+` vs `vin\+`, upper/lower case): pin names on the layout pins must equal the schematic pin names exactly. Rename the layout pin label (select the pin, `q`).
4. *Body/substrate nets*: NMOS bodies are on vss and PMOS bodies on vdd in the schematic; in the layout the bodies connect through the Detached taps. If the extraction reports an extra net (substrate, `sub!` or an unnamed net) or a "bulk" mismatch, a tap is not connected to its rail: check that every tap has Metal1 to vss (NMOS) or vdd (PMOS) in the layout (Navigator highlight of vss / vdd).
5. *Parallel devices merged*: M0 and M1 are identical, parallel, diode-connected NMOS (both b1, b1, vss, vss). If LVS reports that they were merged (m = 2 on one device), that is normal.
6. *Size mismatch (W or L)*: the layout pcell parameters differ from the sized schematic (if the layout was generated before sizing). Fix: Connectivity -> Update -> Components and Nets and accept the parameter updates [CHECK].
7. *Nets b1..b4 / net14 / net28 / net39 / net48 show as unnamed in the layout*: harmless if the connections are correct; LVS matches by connectivity, not by internal net names.
- After each fix: save, re-run DRC if you touched geometry, re-run LVS with Run Name `lvs2`, `lvs3`, ...

2.4.4 Record the final result for the report (match/mismatch and what you changed).

## Part 3. Parasitic extraction (Quantus) and post-layout simulation

Prerequisites: LVS match (Part 2) and Option B done (otherwise the extracted view has no bias current and no load).

### Step 3.1 Extract

3.1.1 In the layout window: **Quantus -> Run Quantus...** [CHECK: if this menu item is named "Extract..." or the form opens as "Quantus QRC Extraction", use it; the older alternative is **Assura -> Run RCX...**].
3.1.2 Fill the form (tab names may differ):
- **Setup:** extraction type `RC` (resistance and capacitance); reference node `vss`; the LVS run: use the Assura LVS run you just made (name `lvs1` or your final run name, run directory `.`) [CHECK]. Capacitance coupling mode: take the default, or "Decoupled" if there is a choice (simplest) [CHECK].
- **Technology files:** the form needs the technology (QRC) directory or `qrcTechFile` of gpdk045. Find it in the terminal: `ls /home/install/FOUNDRY/analog/45nm/` and look for a folder named like `qrc` or `QRC`; inside, the `qrcTechFile` or a `.tch` file [CHECK]. If you find nothing, ask the lab staff (this is the point you were told to ask early); tell me what `ls` shows.
- **Output:** output type `Extracted View` (the default view name is `av_extracted` or `extracted`), and tick that parasitics are kept in the cellview [CHECK]. Save the netlist too if there is a tick box.
Click OK and take screenshot **S36** of the form first.
- Check: the run finishes; the log in the CIW / terminal shows no errors; Library Manager shows a new view (`av_extracted`) under Sld_80/Low_AmpSd. Screenshot **S37**.

3.1.3 Open that extracted view (double-click it in the Library Manager, or File -> Open -> View `av_extracted`).
- Check: you see the layout or a schematic-like view with parasitic R and C. Screenshot **S38**.
- If extraction fails with a "technology" or "rules" error, tell me the exact message. If it says LVS is not clean, go back to Part 2.

### Step 3.2 Point the test bench at the extracted view

3.2.1 Open `low_amp1` and launch ADE L (the same session you used before; **one ADE L session per design** and only from the bench, not from Low_AmpSd).
3.2.2 **Setup -> Environment...** -> the field **Switch View List**. It probably contains something like `spectre cmos_sch cmos.sch schematic veriloga`. Put the extracted view name **first**: `av_extracted spectre cmos_sch cmos.sch schematic veriloga` [CHECK: keep your other entries as they are, only add the first one]. Keep **Stop View List** as it is. OK.
- Why: when the netlister reaches the Low_AmpSd instance it uses the first view in the list that exists for that cell; the benches themselves have no extracted view and keep using their schematic.
- Alternative (if the switch list does not work): in the Library Manager create a config view for the bench (File -> New -> Cellview, Type `config`, template `spectre` [CHECK]) and bind Low_AmpSd to `av_extracted`.

3.2.3 **Simulation -> Netlist -> Recreate**, then **Simulation -> Netlist -> Display** and read the netlist.
- Check: the Low_AmpSd subckt now has many parasitic resistor and capacitor lines (names like `R...`, `C...`, or a `.. dspf`-style included file) and its devices M0-M15 with the layout instance parameters; the instance has the pin `ibias`; the bench has `I1 ... isource dc=2u` and the 1 pF capacitor. If the netlist still shows the old schematic subckt (no parasitic lines), the switch list is not taking effect: repeat 3.2.2. Screenshot **S42** of the setting.

### Step 3.3 Run the post-layout simulations

Use the **same** conditions as the schematic run you compare with. Recommended: model section `tt`, 27 C, V0 = 2.0 V, for both pre- and post-layout, because ProjectState has the tt transient values for the sized circuit (tp 100.9 ns, 32.45 µW, 3.27 pJ), but the AC values (46.66 dB, 1.726 MHz) were not recorded with a named section [CHECK]. So **first re-run the schematic AC on tt** (switch view list back to the normal one, or run before you add av_extracted) and use that as the "pre-layout" column.

3.3.1 `low_amp1` (AC): V2 DC = 1.016089, AC magnitude 1; ac 1 Hz to 1 GHz, 20 points per decade; outputs `gain_dB = dB20(VF("/out"))` and `phase_deg = phase(VF("/out"))`; Run.
- Check: a gain curve like before. Markers: low-frequency gain, the 0 dB crossing and phase there. Screenshot **S39**. Expect the post-layout numbers to be close to the schematic ones (parasitic C slightly lower GBW).
- If the DC gain is near 0 dB or the output is stuck at a rail, the bias current is missing: look at the netlist for `ibias` (Step 3.2.3).

3.3.2 `low_amp1_tran` (transient): same settings as before (stop 40u, moderate). Set the same view list there (Setup -> Environment is per ADE session). Run. Markers on the 1.0 V crossings (input rising / falling and output rising / falling). Screenshot **S40**. Then `average(IT("/V0/PLUS"))` in the calculator. Screenshot **S41**.
- Compute: tPLH, tPHL, tp = average, power = 2 V x |avg current|, PDP = power x tp. (Or send me the numbers and I compute them in Python.)

3.3.3 **Restore:** remove `av_extracted` from the switch view list, reset the model section to tt / 27 C / V0 = 2.0 V, so that the benches use the schematic again.

### Step 3.4 Pre- vs post-layout comparison (fill this table, then paste into the report section "Output waveform for the layout")

All "Schematic" values below are the recorded ones; replace them with fresh runs on the same section if you re-ran the schematic.

| Parameter | Schematic (sized) | Post-layout | Change (%) |
|---|---|---|---|
| Model section / temperature / VDD | tt, 27 C, 2.0 V | tt, 27 C, 2.0 V | n/a |
| DC gain | 46.66 dB [CHECK section] | [TO FILL] | [TO FILL] |
| GBW (0 dB crossing) | 1.726 MHz [CHECK section] | [TO FILL] | [TO FILL] |
| Phase margin | about 90.0 deg [CHECK section] | [TO FILL] | [TO FILL] |
| tPLH | 82.1 ns (tt) | [TO FILL] | [TO FILL] |
| tPHL | 119.7 ns (tt) | [TO FILL] | [TO FILL] |
| tp = (tPLH + tPHL)/2 | 100.9 ns (tt) | [TO FILL] | [TO FILL] |
| Average supply current | 16.227 uA (tt) | [TO FILL] | [TO FILL] |
| Power (2 V x avg current) | 32.45 uW (tt) | [TO FILL] | [TO FILL] |
| PDP = power x tp | 3.27 pJ (tt) | [TO FILL] | [TO FILL] |

Change (%) = (post - schematic) / schematic x 100. Interpretation to write: the extracted wire resistance and capacitance add load, so a small increase in delay and a small drop in GBW is expected; a very large change would point to a layout problem (for example a very long wire) or a setup problem (missing bias). [CHECK: write the actual comment from your numbers]

## If something goes wrong (quick table)

| Symptom | Likely cause | What to do |
|---|---|---|
| DRC shows new errors after a fix | you moved a shape too close to a third shape | `u` (undo), move less, or move the other shape; re-run DRC |
| LVS says extra devices I0 and C0 | Option A not honoured / not done | Step 2.2 |
| LVS says pin mismatch `ibias` | pin only in the schematic or only in the layout | Step B.5, Update Components and Nets |
| Bench instance shows pin error after the symbol change | old instance | delete and place a new instance (Step B.4) |
| Post-layout output stuck | bias current missing | check the netlist for ibias and I1 |
| Results differ after Option B in the schematic runs | wrong idc direction or cap value | PLUS on vdd, MINUS on ibias; cap 1p |
| Stale netlist | second ADE L session or no recreate | one ADE L session per bench, Simulation -> Netlist -> Recreate |
