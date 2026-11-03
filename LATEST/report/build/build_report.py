import re, copy
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

import os
H=os.path.dirname(os.path.abspath(__file__))   # LATEST/report/build
S=os.path.join(H,'..','..','screenshots')+os.sep; I=os.path.join(H,'img')+os.sep
SRC=os.path.join(H,'Report_Draft.docx')
OUT=os.path.join(H,'..','Report_Final_Draft.docx')
d=Document(SRC)

def fmt(run,size=12,bold=None,italic=None):
    run.font.name='Times New Roman'; run.font.size=Pt(size)
    rpr=run._element.get_or_add_rPr(); rf=rpr.find(qn('w:rFonts'))
    if rf is None: rf=OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii','w:hAnsi','w:eastAsia','w:cs'): rf.set(qn(a),'Times New Roman')
    if bold is not None: run.bold=bold
    if italic is not None: run.italic=italic
def clear(p):
    for r in list(p.runs): r._element.getparent().remove(r._element)
def set_text(p,text,bold=None,italic=None,hl=False,align=None):
    clear(p); r=p.add_run(text); fmt(r,bold=bold,italic=italic)
    if hl: r.font.highlight_color=WD_COLOR_INDEX.YELLOW
    if align is not None: p.alignment=align
def add_after(p,text='',italic=False,hl=False,align=None,keep_next=False):
    new=OxmlElement('w:p'); p._p.addnext(new); q=Paragraph(new,p._parent)
    if text:
        r=q.add_run(text); fmt(r,italic=italic)
        if hl: r.font.highlight_color=WD_COLOR_INDEX.YELLOW
    if align is not None: q.alignment=align
    return q
def delete(p): p._element.getparent().remove(p._element)
def replace_in(p,old,new):
    for r in p.runs:
        if old in r.text:
            r.text=r.text.replace(old,new); return True
    if old in p.text:
        full=p.text.replace(old,new); lead=p.runs[0].bold if p.runs else None
        set_text(p,full,bold=None); return True
    return False
def find(start=None,contains=None):
    for p in d.paragraphs:
        if start and p.text.startswith(start): return p
        if contains and contains in p.text: return p
    raise KeyError(start or contains)

fig=[0]
def put_image(p,path,width,caption):
    clear(p); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next=True
    p.add_run().add_picture(path,width=Inches(width))
    fig[0]+=1
    c=add_after(p,f'Figure {fig[0]}: {caption}',italic=True,align=WD_ALIGN_PARAGRAPH.CENTER)
    return c
def put_note(p,text,hl=False): set_text(p,text,italic=not hl,hl=hl)

# ---------- screenshot slots ----------
slots=[p for p in d.paragraphs if p.text.startswith('[SCREENSHOT')]
seen={}
def sid(p): return re.match(r'\[SCREENSHOT (S\d+(?:-S\d+)?)',p.text).group(1)
for p in slots:
    k=sid(p); seen[k]=seen.get(k,0)+1
    if k=='S43':
        put_image(p,I+'fig2_raw-2.png',5.0,'Fig. 2 of the reference paper [1] (cascade second-stage topology), reproduced for reference.')
    elif k=='S01':
        put_image(p,S+'S01_baseline_schematic_fit_view.jpg',6.2,'Virtuoso schematic of Sld_80/Low_AmpSd_base (the unsized circuit): 16 transistors M0-M15, the bias source I0 (2 uA), the load capacitor C0 (1 pF) and the pins out, vdd, vss, vin+ and vin-.')
    elif k=='S02':
        put_image(p,I+'S02_tb_low_amp1_early.jpg',5.8,'Test bench low_amp1 (DC and AC): supply V0 = 2 V, inputs V2 on vin+ and V3 on vin-, and the Low_AmpSd symbol. This early picture shows V2 = 1 V; for the recorded baseline results V2 was set to the trip-point value 1.028 V (with AC magnitude 1).')
    elif k=='S07':
        put_image(p,I+'S07_tb_tran_clean.png',4.8,'Test bench low_amp1_tran (transient): unity-gain follower (out tied to vin-), supply V0 and a pulse source V1 on vin+ (0.8 V to 1.2 V, delay 1 us, rise and fall 10 ns, width 10 us, period 20 us). In this picture V0 shows 2.2 V, the value left from PVT case B; the nominal runs use V0 = 2 V. The same bench is used for the baseline and the sized circuit.')
    elif k=='S03':
        put_image(p,I+'b42138aa-image.png',5.6,'Baseline DC sweep of vin+ (vin- = 1 V), out versus dc: sharp transition; out crosses 1.0 V at vin+ of about 1.028 V (trip point).')
    elif k=='S04':
        put_image(p,I+'4bfcb708-image.jpg',4.3,'Baseline DC operating point at V2 = 1.028 V: out = 1.13226 V; supply source V0: i = -7.94298 uA, pwr = -15.886 uW (the first line, 46.3812 mV, is the output of an earlier run at V2 = 1 V).')
    elif k=='S05':
        put_image(p,I+'b566ec58-image.png',5.4,'Baseline AC gain (gain_dB = dB20(VF("/out"))): marker M1 at 1.26 Hz reads 44.6 dB (DC gain); marker M2 at 708.0 kHz reads -255 mdB (0 dB crossing, GBW about 0.7 MHz).')
    elif k=='S06':
        put_image(p,I+'91fd5a20-image.png',5.4,'Baseline AC gain and phase: marker M3 on the phase curve at 707.946 kHz reads -89.7362 deg, so the phase margin is 180 - 89.74 = about 90.3 deg.')
    elif k=='S08':
        put_image(p,I+'0c6830db-image.jpg',5.0,'Baseline transient (unity-gain follower): markers on the output at 1.0 V, M1 = 1.1762 us (rising) and M2 = 11.2699 us (falling). With the input crossing 1.0 V at 1.005 us and 11.015 us this gives tPLH = 171.2 ns and tPHL = 254.9 ns.')
    elif k=='S09':
        put_image(p,I+'60601d81-image.jpg',5.6,'ADE L outputs table of the baseline transient run: the expression average(IT("/V0/PLUS")) gives -12.335... uA in the Value column (full value -12.3356 uA).')
    elif k=='S10':
        put_image(p,I+'S10_sized_schematic.png',6.3,'Schematic of Sld_80/Low_AmpSd (the sized circuit), opened from instance I0 of the test bench: 16 transistors, I0, C0 and the pins vdd, vss, vin+, vin- and out. The sized W and L values are listed in Table 1 and shown in the netlist excerpt below.')
    elif k=='S11':
        c=put_image(p,I+'S11_netlist_excerpt.png',6.0,'Excerpt of the Spectre netlist of the sized circuit: M9 and M10 (input pair) w = 1.6u, l = 150n; M5, M6, M12 and M15 w = 640n, l = 300n; M8 shown for comparison (unchanged, 320n / 150n).')
        q=add_after(c); q.alignment=WD_ALIGN_PARAGRAPH.CENTER
        q.add_run().add_picture(I+'S11_props.png',width=Inches(2.2)); fig[0]+=1
        add_after(q,f'Figure {fig[0]}: Property Editor of M9 in the sized schematic: Length 150n, Finger Width 1.6u, Total Width 1.6u, 1 finger, model g45n2svt.',italic=True,align=WD_ALIGN_PARAGRAPH.CENTER)
    elif k=='S12':
        put_note(p,'The sizes of M5, M6, M12 and M15 (w = 640n, l = 300n) are shown in the netlist excerpt above.')
    elif k=='S13':
        put_image(p,S+'G2_testbench_low_amp1.jpg',5.4,'Test bench low_amp1 with the sized Low_AmpSd: V2 on vin+ = 1.016 V (bias used for the AC and transient runs, 1.016089 V) with AC magnitude 1, V3 = 1 V, V0 = 2 V.')
    elif k=='S18':
        put_note(p,'The transient test bench of the sized circuit is the same low_amp1_tran bench shown in the previous section; its Low_AmpSd symbol resolves to the sized Low_AmpSd schematic.')
    elif k=='S14':
        put_image(p,I+'S14_dc_sized_marker.png',5.6,'DC sweep of the sized circuit (V2 on vin+ swept 0.8 V to 1.2 V, vin- = 1 V, 27 C): marker M1 at vin+ = 1.0637 V where out = 1.000975 V. The steep part of the curve is near 0.85 V. The AC and transient runs of this report were taken with V2 = 1.016089 V (see text).')
    elif k=='S16':
        put_image(p,I+'S16_ac_sized.jpg',5.8,'AC gain (red) and phase (yellow) of the sized circuit: M2 at 1.995 Hz reads 46.6578 dB (DC gain); M3 at 1.72607 MHz reads 968.6 udB (0 dB crossing, GBW = 1.726 MHz); M4 at 1.72784 MHz reads -90.005 deg (phase margin = about 90.0 deg).')
    elif k=='S17':
        put_note(p,'The markers for the 0 dB crossing (1.726 MHz) and the phase at that frequency (-90.005 deg) are in the figure above.')
    elif k=='S19':
        put_image(p,I+'S19_tran_sized.jpg',5.6,'Transient of the sized follower (model section mc): output markers at 1.0 V, M3 = 1.12502 us (rising) and M2 = 11.1316 us (falling), giving tPLH = 120.0 ns and tPHL = 116.6 ns. The red trace is the supply current.')
    elif k=='S20':
        put_note(p,'[SCREENSHOT TO ADD (S20): ADE L outputs table showing average(IT("/V0/PLUS")) = -16.354 uA for the sized circuit (model section mc).]',hl=True)
    elif k=='S21':
        put_note(p,'[SCREENSHOT TO ADD (S21): ADE L window showing the model-library section and temperature used for a PVT run.]',hl=True)
    elif k=='S22':
        put_note(p,'[SCREENSHOT TO ADD (S22): nominal tt, 27 C, 2.0 V transient with delay markers (tPLH 82.1 ns, tPHL 119.7 ns) and average current -16.227 uA.]',hl=True)
    elif k=='S23':
        put_image(p,I+'S23_tran_ss.jpg',5.6,'PVT case A (ss, 125 C, VDD = 1.8 V): output markers at 1.0 V, M1 = 1.15875 us and M2 = 11.2493 us, giving tPLH = 153.8 ns and tPHL = 234.3 ns; average current -9.065 uA.')
    elif k=='S24':
        put_image(p,I+'17b38038-image.jpg',5.0,'PVT case B (ff, -40 C, VDD = 2.2 V): output markers at 1.0 V, M1 = 1.04443 us (rising) and M2 = 11.0794 us (falling), giving tPLH = 39.4 ns and tPHL = 64.4 ns; average current -35.23 uA.')
    elif k=='S25':
        put_image(p,I+'S25_pvt_summary.png',6.2,'Summary of the PVT runs of the sized circuit, plotted from the values in the PVT table .')
    elif k=='S26':
        put_image(p,I+'8a8544a7-image.png',4.4,'Layout of Sld_80/Low_AmpSd (all levels shown): PMOS row on top, two NMOS rows below, vdd and vss rails and strap on Metal1, pins on the boundary, routed signal nets with their labels.')
    elif k=='S27':
        put_image(p,I+'4cccb95d-image.png',4.2,'Placement of the 16 transistors with instance names (before routing): top PMOS row M7, M8, M11, M12, M15, M13, M14; middle NMOS row M0, M9, M10, M1, M3; bottom row M2, M6, M5, M4.')
    elif k=='S28':
        put_image(p,I+'6717da96-image.png',4.4,'Pins (vin-, vin+, out, vdd, vss) and the Metal1 rails: vdd rail at the top, vss strap in the middle and vss rail at the bottom (before routing).')
    elif k=='S31':
        put_image(p,I+'e2b8de5c-image.png',5.8,'Assura DRC error list after the fixes (run drc1): OXIDETHK.SP.1 (1), CONT.SE.3 (2), CONT.SE.4 (2), METAL1.SP.1.1 (3), METAL1.SP.1.2 (2), METAL1.SP.1.3 (3): 13 errors left.')
    elif k=='S30':
        put_image(p,I+'62e4bbc8-image.png',4.0,'Assura Run DRC form: library Sld_80, cell Low_AmpSd, view layout, rules file /home/install/FOUNDRY/analog/45nm/assura/assuraDRC.rul.')
    elif k=='S29':
        put_image(p,I+'12e435f8-image.png',3.6,'Annotation Browser after routing: Connectivity (0/0), i.e. no incomplete nets and no shorts (router summary: 11/11 signal nets and 2/2 power nets routed with 0 opens and 0 shorts).')
    elif k in ('S32','S33','S34','S35','S36-S38','S39','S40','S41','S42'):
        delete(p)
    else:
        print('UNHANDLED',k)

# ---------- text edits ----------
replace_in(find(contains='[CHECK: title wording]'),' [CHECK: title wording]','')
replace_in(find(contains='[CHECK: edit the wording'),' [CHECK: edit the wording to match what your faculty approved]','')
p=find(contains='[CHECK: retype eq. (4)')
replace_in(p,'[CHECK: retype eq. (4) from the PDF; the text extracted from the PDF is garbled, so it is not copied here.]','It reads A_v = (I_M5 / 2 I_M7) x (b / (n_n V_t^2)) x 1 / (lambda_p^2 n_p + lambda_n^2 n_n).')
replace_in(p,'[CHECK: standard result, cite Allen and Holberg [4]]','(standard result, see [4])')
p=find(contains='The reason for the power increase was not isolated')
replace_in(p,'The reason for the power increase was not isolated in this work [CHECK: possible cause is the larger devices drawing more current in the self-biased loop, to be confirmed by comparing the DC currents of the two versions].','A likely cause, not verified by a separate simulation, is that the tail node of the input pair is the bias node b1 (as drawn in the paper), so the pair current is not fixed by a tail current source: a wider pair conducts more current at the same gate voltage and the total supply current rises.')
set_text(find(start='Verification and extraction'),'Verification: Assura DRC was run on the layout. Assura LVS and Quantus parasitic extraction are part of the tool set but were not run in this project because of the submission time.')
delete(find(start='Documents and scripts'))
set_text(find(start='Power at each corner'),'Power at each corner = (VDD of that corner) x (average current). Observations: the delay changes by about 1.9 times between the nominal and the slow corner (194.0 ns / 100.9 ns) and the fast corner is about 2 times faster than the nominal one (51.9 ns), so over the three cases the delay spans about 3.7 times. The power changes by about 4.7 times between the slow and the fast corner (77.51 µW / 16.32 µW). Power is the weak point: the 20 µW target is met only at the slow corner (high temperature and low VDD). The PDP varies much less (3.17 pJ to 4.02 pJ). Case C was not run.')
set_text(find(start='DRC (Assura, rules file assuraDRC.rul)'),'DRC (Assura, rules file assuraDRC.rul): the error count went from about 50 at the first run to 13 after the fixes described in the problems section. The remaining 13 errors (listed below) were not fixed within the available time.')
set_text(find(start='LVS (Assura, extract.rul'),'LVS (Assura) and parasitic extraction (Quantus) were not run because of the submission time, so there is no LVS result and no post-layout simulation. The layout has been checked for connectivity (Layout XL: no incomplete nets, no shorts) and partly for design rules (13 DRC errors left).')
p=find(contains='DRC status at the time of this draft')
set_text(p,p.text.replace('DRC status at the time of this draft (13 errors left)','DRC status at the end of the work (13 errors left)').replace(' [TO FILL: replace with the final result]',''))
set_text(find(start='Post-layout simulation uses the parasitic-extracted view'),'Post-layout simulation was not performed. It needs the LVS check and the parasitic extraction (Quantus), which were not completed in the available time. The schematic (pre-layout) results of the previous sections are therefore the results reported here.')
set_text(find(start='Expected effect (to be confirmed'),'Expected effect (not verified): the extracted view adds wire resistance and capacitance, so the post-layout GBW and delay would be expected to be somewhat worse than the schematic values.')
replace_in(find(contains='[CHECK: confirm that the paper gives no sizes]'),' [CHECK: confirm that the paper gives no sizes]','')
replace_in(find(contains='[CHECK: wording]'),' [CHECK: wording]','')
replace_in(find(contains='57.78° in Section III-A and 68°'),' [CHECK]','')
replace_in(find(contains='[CHECK with faculty]'),' [CHECK with faculty]','')
p=find(contains='The layout was placed and routed with no open or shorted nets')
t=p.text; t=t[:t.index('The layout was placed and routed')]
t=t.replace('the delay changes by about 1.9 times between the nominal and the slow corner and the power by about 4.7 times between the slow and the fast corner','the delay goes from 51.9 ns at the fast corner to 194.0 ns at the slow corner (about 3.7 times) and the power changes by about 4.7 times between the slow and the fast corner')
set_text(p,t+'The layout was placed and routed with no open or shorted nets (Layout XL connectivity check 0/0), and the Assura DRC error count was brought from about 50 down to 13 remaining errors (OXIDETHK.SP.1, CONT.SE.3, CONT.SE.4 and the Metal1 spacing rules), which were not fixed in the available time. LVS, parasitic extraction and post-layout simulation were not carried out and remain as future work.')
set_text(find(start='11.  Layout: about 50 DRC errors'),'11.  Layout: about 50 DRC errors at the first run, with 13 remaining at the end of the work (OXIDETHK.SP.1, CONT.SE.3, CONT.SE.4, METAL1.SP.1.1, METAL1.SP.1.2, METAL1.SP.1.3).')
set_text(find(start='12.  LVS: the schematic contains'),'12.  LVS and PEX: not run because of the submission time. The schematic contains the ideal parts I0 (idc, 2 µA) and C0 (pcapacitor, 1 pF), which do not exist in the layout, so an Assura LVS run would report them as unmatched unless they are excluded or moved into the test benches. This was identified but not carried out.')
replace_in(find(contains='[CHECK: exact cause]'),' [CHECK: exact cause]','')
replace_in(find(contains='[CHECK: why the router then created shorts]'),'[CHECK: why the router then created shorts]','(the router does not treat fill-purpose shapes as wires to avoid, so it ran its own wires across them)')
set_text(find(start='12.  Remaining DRC errors'),'12.  Remaining DRC errors -> not resolved in the available time: 13 errors were left after Route -> Fix Violations (which had already removed VIA1.X.1). The planned fixes were local Metal1 spacing corrections and moving the gate contacts.')
set_text(find(start='13.  LVS with ideal I0 and C0'),'13.  LVS with ideal I0 and C0 -> not carried out (see problem 12). Planned solution: move I0 and C0 into the test benches and bring the bias node out as an ibias pin, or exclude them from the comparison with an LVS-ignore property.')
set_text(find(contains='values still to be measured are marked'),'All numbers in this report are taken from the recorded simulation results. Items that were not measured or not completed (the DC-bias power of the sized circuit, the delay at the fast PVT corner, the remaining DRC errors, LVS, parasitic extraction and post-layout simulation) are stated as such in the text.')
p=find(contains='Allen and D. R. Holberg')
set_text(p,'[4] P. Allen and D. Holberg, CMOS Analog Circuit Design, Oxford University Press, 2016 (as cited in [1]); used for the cascode output resistance and weak-inversion transconductance concepts.')

replace_in(find(contains='and the fast-corner delay were not simulated'),' and the fast-corner delay','')
replace_in(find(contains='the delay at the fast PVT corner'),'the delay at the fast PVT corner, ','')
# ---------- tables ----------
for t in d.tables:
    for r in t.rows:
        cells=r.cells
        if cells[0].text.startswith('Power calculation: DC-bias power'):
            for c in cells[1:]:
                if 'TO FILL' in c.text:
                    c.paragraphs[0].text=''; run=c.paragraphs[0].add_run('not measured'); fmt(run,size=10)
        if cells[0].text.startswith('Slew rate'):
            for c in cells:
                if 'TO FILL' in c.text:
                    c.paragraphs[0].text=''; run=c.paragraphs[0].add_run('not evaluated'); fmt(run,size=10)
for t in d.tables:
    for r in t.rows:
        if r.cells[0].text.startswith('B: fast'):
            for ci,val in ((4,'51.9 ns (tPLH 39.4, tPHL 64.4)'),(6,'4.02 pJ')):
                c=r.cells[ci]; c.paragraphs[0].text=''; run=c.paragraphs[0].add_run(val); fmt(run,size=10)
# remove the post-layout template table (last table)
last=d.tables[-1]
if 'Post-layout' in last.rows[0].cells[2].text: last._element.getparent().remove(last._element)

def strip_hl(par):
    for r in par.runs:
        if r.font.highlight_color is not None and '[' not in r.text:
            r.font.highlight_color=None
for par in d.paragraphs: strip_hl(par)
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            for par in c.paragraphs:
                if 'TO FILL' not in par.text: strip_hl(par)

for _p in d.paragraphs:
    replace_in(_p,'The new trip point is vin+ = 1.016089 V (out = 0.981 V at that bias), so the systematic offset is smaller than in the baseline (1.028 V), a shift of 11.9 mV.','The sized circuit is biased at vin+ = 1.016089 V (out = 0.981 V at that bias) for the AC and transient runs; the baseline bias was 1.028 V.')
    if _p.text.strip()=='DC. Trip point at vin+ = 1.016089 V.': replace_in(_p,'Trip point at vin+ = 1.016089 V.','DC sweep: the output crosses 1.0 V at vin+ = 1.0637 V (marker M1 in Figure 16). The AC and transient runs below were taken with V2 = 1.016089 V.')
d.save(OUT)
left=[(i,m.group(0)) for i,p in enumerate(Document(OUT).paragraphs) for m in re.finditer(r'\[(CHECK|TO FILL|SCREENSHOT)[^\]]*\]',p.text)]
print('figures',fig[0]); 
for x in left: print(x[0],x[1][:110])
