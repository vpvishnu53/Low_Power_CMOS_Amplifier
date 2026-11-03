# Cadence session log (done by Claude over AnyDesk, lab PC, Virtuoso 6.1.8)

Rules for this session: work only inside Virtuoso/Assura/Quantus; back up before editing; commit after each step.

## Step 0: backup (done 2026-11-03 06:45)
- File -> Save a Copy of `Sld_80/Low_AmpSd/layout` as view `layout_drc_start` (verified in the Open File browser; the cell now has layout, layout_drc_start, layout_routed, physConfig, schematic, symbol).
- Schematic backup (`Low_AmpSd_pre_lvs`) not made yet; do it before Part 2 (Option B).

## Step 1.1: DRC run drc2 (done 06:46)
- Assura -> Run DRC, run name drc2, rules file assuraDRC.rul, library Sld_80, cell Low_AmpSd, view layout. Completed successfully.
- Error Layer Window: OXIDETHK.SP.1 (1), CONT.SE.3 (2), CONT.SE.4 (2), METAL1.SP.1.1 (3), METAL1.SP.1.2 (2), METAL1.SP.1.3 (3) = 13 errors, same as ProjectState.
- Screenshots: screenshots/S30_run_drc_form.jpg, screenshots/S31_drc_errors_before.jpg
- Note: the layout window title bar did not show unsaved changes; nothing was edited yet.

## Step 1.3 attempt 1: OXIDETHK.SP.1 by merging oxide regions (FAILED, reverted) 06:47-06:50
- Drew one Oxide_thk drw rectangle (0.265 x 0.46 um) across the gap between two neighbouring devices (the pair joined by net39, lower middle of the layout), saved, re-ran DRC as drc3.
- Result: OXIDETHK.SP.1 went from 1 to 2 errors, all other rules unchanged. The rule is "Thick Active Area to Thick Active Area spacing >= 0.16 um". My first guess (it is measured between active areas, so merging markers cannot help) is superseded by the revised explanation two bullets below.
- Reverted: selected only the new rectangle (made only Oxide_thk selectable via NS, then selected, then toolbar delete), restored AS, saved. Layout geometry is the same as in `layout_drc_start`.
- Likely cause of the failure (revised at 06:53, not yet proven): the two thick-oxide boxes are about 0.09 um apart over their full height. My rectangle covered only the middle of that gap, so it left a narrow slot above and below it, each narrower than 0.16 um and each counted as a violation (1 error became 2). The merge idea itself may still work if the rectangle overhangs both boxes at top and bottom (about 0.07 um) so no slot is left. [CHECK] untested.
- Second try (rectangle overhanging both boxes) did NOT get created: the AnyDesk screen lagged behind my clicks and the corner clicks ended up as selection clicks (no shape was added, title bar never showed `*`). Stopped editing there. Left state: layout unmodified (equal to layout_drc_start), PR boundary selected, nothing dragged.
- DRC run drc4 on the restored layout shows the original 13 errors again (1/2/2/3/2/3), so the baseline is intact.
- AnyDesk free licence shows "Session will be closed in 5 min..." (non-commercial limit), so sessions are time-limited; reconnecting needs the student.
- Tool notes for this lab PC: keyboard shortcuts typed over AnyDesk (F5, r) did not work, use the menus and toolbar; the screen can lag several seconds behind clicks, wait and re-screenshot before the next click; the Error Layer Window must be raised from the top-bar app menu (click "Error Layer Window" at the top, pick it from the list; do not click Quit); Assura asks "stop viewing current job?" before each new run, answer Yes.

## Report screenshots (DRC paused at the student's request, 06:57)
- S26 captured: screenshots/S26_layout_full_pre_drc_fix.jpg (full layout, View -> Zoom To Fit All, nothing selected, LSW visible). Taken BEFORE the DRC fixes, so retake after the final layout (Morning_Guide Step 1.4.4).
- Not yet captured (need a new AnyDesk session; the free session timed out): S27 (instance names), S28 (pin zooms), all schematics/ADE/waveform/PVT shots (G1-G4), LVS/PEX shots.

## G1/G2 progress (AnyDesk session 2, 06:57-07:03; student said: plain screenshots are fine, only keep ones I am sure about)
- Backup of nothing changed in the design in this session. ADE settings only.
- Captured: screenshots/S01_baseline_schematic_fit_view.jpg (Low_AmpSd_base, whole circuit, fit view; labels small, retake zoomed halves later if wanted), screenshots/G2_testbench_low_amp1.jpg (low_amp1 bench: V0=2, V2=1.016 V acm=1, V3=1, instance of Low_AmpSd).
- ADE L for low_amp1 had an empty setup; loaded the saved state `state1` (dc + ac 1..1G, 20 pts/decade; outputs out, gain_dB, phase_deg). Model library section was `mc` when I found it.
- **Finding (needs the student's OK):** AC gain depends on the model section. Reading the /out magnitude plot at low frequency: section tt gives about 172 V = 44.7 dB, section mc gives about 216 V = 46.7 dB. ProjectState's 46.66 dB therefore matches `mc`, not `tt`. The checklist G0 step 2 says tt; that is inconsistent with ProjectState. These are plot readings, not marker values. The sized AC gain at tt is not a ProjectState number.
- This also supports my earlier assumption that the baseline numbers are mc [resolved 2026-11-03: the student confirmed the baseline was also mc].
- Captured but NOT markered: screenshots/G2b_sized_AC_mc_no_markers.jpg (sized, section mc, gain/phase left, /out magnitude right). Needs markers (DC gain, unity-gain frequency, phase at unity gain) before it goes in the report. The first tt run's plot was not saved (wrong section for the report).
- ADE model section left at `mc` (as found). ADE state1 loaded in session; nothing saved.
- Still to do: markers on this plot, baseline run (swap in Low_AmpSd_base), transient bench, PVT, S27/S28.

## Decision and marker attempt (07:04-07:06)
- Student confirmed: use model section `mc` for all AC and transient numbers in the report (tt only for the typical corner row of PVT, if at all). Checklist G0.2 and Morning_Guide wording that says "section tt" must be updated accordingly. [DONE 2026-11-03: docs updated, see PROGRESS_LOG]
- Marker attempt on the sized AC plot (mc): Marker -> Create Marker... in this Virtuoso build does NOT snap Y to the trace. With Attach to Trace ticked and X = 1 Hz, it placed M1 at 1.0 Hz / -63.284 dB (the Y field keeps a stale value; the real gain at 1 Hz is about +46.7 dB). That marker was wrong, so it was deleted (Marker -> Delete All). No marker values are recorded. Typing a Y value would be inventing data, so I did not.
- Next try: read DC gain / unity-gain frequency / phase margin via ADE calculator functions or ADE Results -> Print, or the viewer's Measurements menu, instead of the Create Marker dialog.

## Note 2026-11-03 evening: screenshot file names
The old layout screenshots named above (S26_layout_full_pre_drc_fix.jpg, S30_run_drc_form.jpg, S31_drc_errors_before.jpg) were replaced by S26_layout_full_real.png, S30_run_drc_form_real.png, S31_drc_errors_real.png and S32_annotation_browser_real.png (taken from the final `layout` view with drc4 = 13 errors).

