from pathlib import Path
import copy,json,re,shutil
import xml.etree.ElementTree as E

R=Path(r'E:\0school\研二上\cvpr\uaca\draw');T='head_selected_expo_20261023'
L=R/'logs'/T;C=R/'candidates'/T;P=R/'previews'/T
for p in [L/'before',C/'head',C/'elements',C/'signals',P]:p.mkdir(parents=True,exist_ok=True)
def read(p):return E.fromstring(p.read_text(encoding='utf8'))
def write(b,p):E.ElementTree(b).write(p,encoding='utf-8',xml_declaration=True)
def ix(m):return {c.get('id'):c for c in m.find('root')}
def n(v):return str(round(float(v),6))
def geo(c,**kw):
    g=c.find('mxGeometry')
    for k,v in kw.items():g.set(k,n(v))
def points(c,xy):
    c.remove(c.find('mxGeometry'));g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    E.SubElement(g,'mxPoint',x=n(xy[0][0]),y=n(xy[0][1]),attrib={'as':'sourcePoint'})
    E.SubElement(g,'mxPoint',x=n(xy[-1][0]),y=n(xy[-1][1]),attrib={'as':'targetPoint'})
    a=E.SubElement(g,'Array',attrib={'as':'points'})
    for x,y in xy[1:-1]:E.SubElement(a,'mxPoint',x=n(x),y=n(y))
def save(m,p,title):
    b=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
    d=E.SubElement(b,'diagram',id=p.stem,name=title);d.append(copy.deepcopy(m));write(b,p)
def subtree(m,seeds,keep_roots=True):
    z=copy.deepcopy(m);root=z.find('root');ids=set(seeds)
    while True:
        more={c.get('id') for c in root if c.get('parent') in ids}-ids
        if not more:break
        ids|=more
    if keep_roots:ids|={'0','1'}
    for c in list(root):
        if c.get('id') not in ids:root.remove(c)
    return z
def snapshot(rel):
    f=R/'final'/rel;dst=L/'before'/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copy2(f,dst)
    return dst

for rel in ['head/UACA_head_simple.drawio','head/UACA_head_simple.pdf','head/UACA_head_simple.png',
            'head/UACA_head_current_layout.drawio','head/UACA_head_current_layout.pdf','head/UACA_head_current_layout.png',
            'elements/action_uncertainty.drawio','elements/action_uncertainty.png','elements/training_curves.drawio','elements/training_curves.png',
            'elements/method.drawio','elements/method.png','signals/UACA_signal_collection.drawio']:
    snapshot(rel)
compare=R/'candidates/head_annotations_20261023/expo/EXPO_first50_center25_comparison.drawio'
if not (L/'before/EXPO_selection_annotated.drawio').exists():shutil.copy2(compare,L/'before/EXPO_selection_annotated.drawio')
selection=read(L/'before/EXPO_selection_annotated.drawio')
chosen=next(d for d in selection.findall('diagram') if d.get('id')=='center25')
assert any('用这个图' in c.get('value','') for c in chosen.iter('mxCell'))
selected=ix(chosen.find('mxGraphModel'))
book=read(L/'before/head/UACA_head_simple.drawio');draft=book.find('diagram/mxGraphModel')
comments=[{'id':c.get('id'),'text':re.sub('<[^>]*>',' ',c.get('value',''))} for c in draft.iter('mxCell') if re.search('[\u4e00-\u9fff]',re.sub('<[^>]*>',' ',c.get('value','')))]

# Follow the user's edited composition: only the main three panels remain.
# The detached noise-source schematic and real-world panel are in the archive.
model=subtree(draft,{'main_group'});root=model.find('root');cells=ix(model)
discard={'main_layout_4','main_layout_5','main_layout_6','main_real_group'}
while True:
    more={c.get('id') for c in root if c.get('parent') in discard}-discard
    if not more:break
    discard|=more
for c in list(root):
    if c.get('id') in discard or c.get('id','').startswith('1JSs4SlWlBpdugTepuEQ-'):root.remove(c)
cells=ix(model)
for c in root:
    if c.get('parent')=='main_group':
        g=c.find('mxGeometry')
        if g is not None and g.get('x') is not None:g.set('x',n(float(g.get('x'))-454))
geo(cells['main_group'],width=1440,height=722)
geo(cells['main_dv_group'],x=0,y=21,width=1440,height=394)
geo(cells['main_dv_main_dv_group'],x=0,y=0,width=1440,height=394)

# Center title and white cutout against the actual 1440 px blue frame.
for k in ['main_layout_21','main_layout_22']:
    width=float(cells[k].find('mxGeometry').get('width'));geo(cells[k],x=(1440-width)/2)
S='main_dv_main_dv_layout_';photo_starts=[26,496,966]
for j,left in enumerate(photo_starts):
    geo(cells[S+str([109,114,119][j])],x=left)
    geo(cells[f'ann_scene_frame_{j}'],x=left)
    for k in ([112,113],[117,118],[122,123])[j]:geo(cells[S+str(k)],x=left+242)
    stepband=['rev6_step26_band',S+'115',S+'120'][j]
    steplabel=['rev6_step26_label',S+'116',S+'121'][j]
    geo(cells[stepband],x=left+121);geo(cells[steplabel],x=left+121)
geo(cells[S+'110'],x=photo_starts[0]);geo(cells[S+'111'],x=photo_starts[0]+4)

# DVCA uses a polyline whose vertices coincide with its circles. Keep the
# approved every-two-actions markers and connect those exact data samples.
data=json.loads((R/'assets/noise4_current_20261023/N39/series.json').read_text())
lookup=dict(zip(data['action'],data['noise4']))
fx=lambda t:90+float(t)/100*1324
fy=lambda u:356-float(u)/.4*126
geo(cells['u_frame'],x=90,y=230,width=1324,height=126)
for i,t in enumerate(range(0,100,4)):geo(cells[f'u_stripe_{i}'],x=fx(t),y=230,width=26.48,height=126)
for i,v in enumerate([0,.2,.4]):
    points(cells[f'u_grid{i}'],[(90,fy(v)),(1414,fy(v))]);geo(cells[f'u_y{i}'],y=fy(v)-10)
curve=[(fx(t),fy(lookup[t])) for t in range(0,101,2)]
points(cells['u_raw_continuous'],curve)
for i,t in enumerate(range(0,101,2)):geo(cells[f'u_dot{i}'],x=fx(t)-4.2,y=fy(lookup[t])-4.2)
for i,t in enumerate(range(0,101,20)):
    points(cells[f'u_tick{i}'],[(fx(t),356),(fx(t),360)]);geo(cells[f'u_xt{i}'],x=fx(t)-22,y=360)
for j,t in enumerate([5,16,48]):
    points(cells[f'u_photo_guide{j}'],[(fx(t),230),(fx(t),356)])
    cx=photo_starts[j]+116
    points(cells[f'u_frame_connector{j}'],[(cx,205),(cx,218),(fx(t),218),(fx(t),230)])
    geo(cells[f'u_photo_step{j}'],x=fx(t)-9,y=209)
geo(cells['rev7_signal_footer'],x=100,width=1240)
geo(cells[S+'107'],x=1298)

# The selected EXPO native curves are copied verbatim. All axis, peak and
# legend objects are retained from the user's current head.
for j in range(2):
    c=cells[f'r2_EXPO_curve{j}'];c.remove(c.find('mxGeometry'));c.append(copy.deepcopy(selected[c.get('id')].find('mxGeometry')))

manifest=[]
dest=C/'head/UACA_head_simple.drawio';save(model,dest,'CURRENT | N39 + selected EXPO')
manifest.append({'file':str(dest),'stem':'UACA_head_simple','pdf':True})

signal_seeds={'main_layout_20','main_layout_21','main_layout_22','main_dv_group','rev7_signal_footer',S+'107'}
signal=subtree(model,signal_seeds)
for c in signal.find('root'):
    if c.get('parent')=='main_group':c.set('parent','1')
save(signal,C/'elements/action_uncertainty.drawio','N39 | DVCA marker-connected line')
manifest.append({'file':str(C/'elements/action_uncertainty.drawio'),'stem':'action_uncertainty','pdf':False})

training=read(L/'before/elements/training_curves.drawio');tr=ix(training.find('diagram/mxGraphModel'))
for j in range(2):
    c=tr[f'r2_EXPO_curve{j}'];c.remove(c.find('mxGeometry'));c.append(copy.deepcopy(selected[c.get('id')].find('mxGeometry')))
write(training,C/'elements/training_curves.drawio')
manifest.append({'file':str(C/'elements/training_curves.drawio'),'stem':'training_curves','pdf':False})

method=subtree(model,{'uaca_method_group'});mi=ix(method);mi['uaca_method_group'].set('parent','1');geo(mi['uaca_method_group'],x=0,y=0)
save(method,C/'elements/method.drawio','CURRENT | UACA for Post-Training')
manifest.append({'file':str(C/'elements/method.drawio'),'stem':'method','pdf':False})

collection=read(L/'before/signals/UACA_signal_collection.drawio');d=collection.findall('diagram')[0]
d.remove(d.find('mxGraphModel'));d.append(copy.deepcopy(signal));write(collection,C/'signals/UACA_signal_collection.drawio')

assert sum('fillColor=#EC7063;' in cells[f'u_dot{i}'].get('style','') for i in range(51))==5
assert all(abs(float(cells[f'u_dot{i}'].find('mxGeometry').get('x'))+4.2-x)<1e-5 and abs(float(cells[f'u_dot{i}'].find('mxGeometry').get('y'))+4.2-y)<1e-5 for i,(x,y) in enumerate(curve))
old=ix(draft)
for prefix in ['r2_GRPO_','r2_RLT_']:
    assert all(E.tostring(cells[k])==E.tostring(v) for k,v in old.items() if k.startswith(prefix))
expo_unmodified=[k for k in cells if k.startswith('r2_EXPO_') and k not in ['r2_EXPO_curve0','r2_EXPO_curve1']]
assert all(E.tostring(cells[k])==E.tostring(old[k]) for k in expo_unmodified)
qa={'comments':comments,'selected_expo_page':chosen.get('name'),'selected_expo_note':'用这个图吧','current_head_only':True,
    'layout':{'top':[0,26,1440,402],'bottom_method':[0,447,581,275],'bottom_training':[594,447,846,275],'title_center':720,'photo_lefts':photo_starts},
    'signal':{'xrange':[0,100],'yrange':[0,.4],'marker_steps':list(range(0,101,2)),'line_vertices':51,'red_steps':[10,12,14,16,18],'frames':[5,16,48],'stripe_width':26.48,'circle_diameter':8.4,'line_rule':'straight segments between adjacent displayed circles; same raw action samples, no averaging'},
    'preserved':'EXPO axes, peaks, legend; all GRPO/RLT chart content; all 14 appendix pages; photo pixels and text.',
    'archive':'Previous full layouts plus annotated source; detached noise schematic and real-world panel retained there.'}
(L/'annotation_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
(L/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(R/'scripts'/f'export_{T}.cjs').write_text((R/'scripts/export_head_annotations_20261023.cjs').read_text().replace('head_annotations_20261023',T),encoding='utf8')
shutil.copy2(__file__,R/'scripts'/Path(__file__).name)
print(json.dumps({'jobs':len(manifest),'comments':comments,'selected_expo':chosen.get('name'),'dimensions':[1440,722],'line_vertices':len(curve)},ensure_ascii=False))
