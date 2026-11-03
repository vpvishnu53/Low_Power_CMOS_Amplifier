# Claude Code handoff (VLSI Fig. 2 op-amp project)

Folder layout (this is how it should sit on your laptop):

    project folder\
        Low-Power_CMOS_Operational_Amplifier_Design_in_45nm_Technology.pdf   (the paper)
        System Design Project Report_format.doc                              (faculty template)
        handoff\                                                             (this folder)
            CLAUDE.md, ProjectState.md, OVERNIGHT_PROMPT.md, README.md
            netlists\   output\

## Run it
1. Open a terminal INSIDE the `handoff` folder (so the paper and template are in `..\`).
2. Start Claude Code (`claude`).
3. Paste the text from `OVERNIGHT_PROMPT.md` (everything below the line).
4. Allow it to run Python and install python-docx, or it will pause and wait.
5. In the morning, open `output\PROGRESS_LOG.md` first.

Claude Code has no access to the lab PC (AnyDesk is only a remote screen), so it does documents only; the Cadence steps stay with you, using the guide it writes.
