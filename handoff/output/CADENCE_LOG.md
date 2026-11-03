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
- Result: OXIDETHK.SP.1 went from 1 to 2 errors, all other rules unchanged. The rule is "Thick Active Area to Thick Active Area spacing >= 0.16 um", i.e. it is measured between active areas, so merging the Oxide_thk markers does not help and the new shape made it worse.
- Reverted: selected only the new rectangle (made only Oxide_thk selectable via NS, then selected, then toolbar delete), restored AS, saved. Layout geometry is the same as in `layout_drc_start`.
- Lesson for the guide: the "draw one OXIDETHK rectangle over the gap" alternative in Morning_Guide Step 1.3 rule 1 is wrong for this rule; remove it. The real fix is to increase the distance between the two active areas.
- Tool notes for this lab PC: keyboard shortcuts typed over AnyDesk (F5, r) did not work, use the menus and toolbar; the Error Layer Window must be raised from the top-bar app menu (click "Error Layer Window" at the top, pick it from the list; do not click Quit); Assura asks "stop viewing current job?" before each new run, answer Yes.
