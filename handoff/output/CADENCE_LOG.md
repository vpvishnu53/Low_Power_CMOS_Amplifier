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
