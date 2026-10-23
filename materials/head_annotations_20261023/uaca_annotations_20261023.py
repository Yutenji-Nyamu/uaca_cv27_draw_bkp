from pathlib import Path
import copy, json, shutil, re
import xml.etree.ElementTree as E
import numpy as np

R=Path(r'E:\0school\研二上\cvpr\uaca\draw')
TAG='head_annotations_20261023'
L=R/'logs'/TAG; C=R/'candidates'/TAG; P=R/'previews'/TAG
for p in [L/'before',C/'head',C/'elements',C/'signals',C/'expo',P]:p.mkdir(parents=True,exist_ok=True)

def load(p):return E.fromstring(p.read_text(encoding='utf8'))
def write(b,p):E.ElementTree(b).write(p,encoding='utf-8',xml_declaration=True)
def index(m):return {c.get('id'):c for c in m.find('root')}
def snap(rel):
    src=R/'final'/rel; dst=L/'before'/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copy2(src,dst)
    return dst
def standalone(m,p,title):
    b=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
    d=E.SubElement(b,'diagram',id=p.stem,name=title);d.append(copy.deepcopy(m));write(b,p)

comments=[]; manifest=[];checks=[]
s=json.loads((R/'assets/noise4_current_20261023/N39/series.json').read_text())
lookup=dict(zip(s['action'],s['noise4']))
top=sorted(sorted(range(0,101,2),key=lambda t:lookup[t],reverse=True)[:5])
assert top==[10,12,14,16,18]
rels=['head/UACA_head_simple.drawio','head/UACA_head_current_layout.drawio','elements/action_uncertainty.drawio','signals/UACA_signal_collection.drawio']
for rel in rels:
    old=snap(rel);b=load(old);m=b.find('diagram/mxGraphModel');root=m.find('root');ix=index(m)
    before={k:E.tostring(v) for k,v in ix.items()}
    red=ix['u_dot5'].get('style');blue=ix['u_dot0'].get('style')
    for i,t in enumerate(range(0,101,2)):ix[f'u_dot{i}'].set('style',red if t in top else blue)
    removed=[]
    for c in list(root):
        if c.get('id','').startswith('zOz5onOmDczC6H9ViqMu-'):
            comments.append({'file':rel,'id':c.get('id'),'text':re.sub('<[^>]*>',' ',c.get('value',''))})
            removed.append(c.get('id'));root.remove(c)
    after=index(m)
    changed=[k for k,v in before.items() if k in after and v!=E.tostring(after[k])]
    assert changed==['u_dot6'],changed
    assert len([k for k in after if re.fullmatch(r'u_dot\d+',k)])==51
    checks.append({'file':rel,'changed_cells':changed,'removed_annotation_cells':removed})
    dst=C/rel;write(b,dst)
    if not rel.startswith('signals'):
        manifest.append({'file':str(dst),'stem':dst.stem,'pdf':rel.startswith('head/')})

# The EXPO annotation explicitly requests a separate trial, so the final heads
# retain their approved training curves. Only the first 50 curve vertices change.
source=load(L/'before/head/UACA_head_simple.drawio').find('diagram/mxGraphModel')
ix=index(source);wanted={'main_grpo_group'}
while True:
    more={k for k,c in ix.items() if c.get('parent') in wanted}-wanted
    if not more:break
    wanted|=more
m=copy.deepcopy(source);root=m.find('root')
for c in list(root):
    if c.get('id') not in wanted|{'0','1'}:root.remove(c)
ix=index(m);g=ix['main_grpo_group'].find('mxGeometry');g.set('x','0');g.set('y','0');ix['main_grpo_group'].set('parent','1')
baseline=copy.deepcopy(m);trial=copy.deepcopy(m);tx=index(trial)
experiment=next(e for e in json.loads((R/'assets/candidates_20261017/curves/experiments.json').read_text()) if e['id']=='EXPO')
curveqa=[]
for j,seq in enumerate(experiment['train']):
    a=np.array(seq,float);cell=tx[f'r2_EXPO_curve{j}'];geom=cell.find('mxGeometry')
    vertices=[geom.find("mxPoint[@as='sourcePoint']")]+list(geom.find('Array'))+[geom.find("mxPoint[@as='targetPoint']")]
    assert len(vertices)==len(a[a[:,0]<=35000])
    values=[]
    for i in range(50):
        avg=float(a[max(0,i-25):min(len(a),i+26),1].mean());values.append(avg)
        vertices[i].set('y',str(round(180.8-(avg-15)/70*172.8,6)))
    oldgeom=index(baseline)[f'r2_EXPO_curve{j}'].find('mxGeometry')
    ov=[oldgeom.find("mxPoint[@as='sourcePoint']")]+list(oldgeom.find('Array'))+[oldgeom.find("mxPoint[@as='targetPoint']")]
    assert all(v.attrib==o.attrib for v,o in zip(vertices[50:],ov[50:]))
    assert all(v.get('x')==o.get('x') for v,o in zip(vertices,ov))
    curveqa.append({'series':['Baseline','UACA'][j],'first50':values,'record50':values[-1],'record51':float(a[1:51,1].mean()),'first_window':[1,26],'record50_window':[25,75]})
bi=index(baseline);ti=index(trial)
assert [k for k in bi if E.tostring(bi[k])!=E.tostring(ti[k])]==['r2_EXPO_curve0','r2_EXPO_curve1']
book=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
for ident,title,model in [('baseline','01 | Current EXPO',baseline),('center25','02 | First 50 records: centered +/-25',trial)]:
    d=E.SubElement(book,'diagram',id=ident,name=title);d.append(copy.deepcopy(model))
    f=C/'expo'/f'EXPO_{ident}.drawio';standalone(model,f,title)
    manifest.append({'file':str(f),'stem':f.stem,'pdf':False})
write(book,C/'expo/EXPO_first50_center25_comparison.drawio')
qa={'comments':comments,'red_points':top,'marker_selection':'top five among the existing sparse markers; all raw curve points and marker spacing preserved','checks':checks,'expo_trial':{'rule':'For records 1-50: mean of raw records i-25 through i+25 inclusive, truncated at dataset start; record 51 onward unchanged trailing MA50.','axis':[15,85],'peaks':[70,76],'scope':'separate comparison only','series':curveqa}}
(L/'annotation_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
(L/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
renderer=(R/'scripts/export_head_n39_swap_20261023.cjs').read_text(encoding='utf8').replace('head_n39_swap_20261023',TAG)
(R/'scripts'/f'export_{TAG}.cjs').write_text(renderer,encoding='utf8')
shutil.copy2(__file__,R/'scripts'/Path(__file__).name)
print(json.dumps({'red_points':top,'comments':comments,'jobs':len(manifest),'changed_final_cells':'u_dot6 only; two annotations archived','trial_record50_to51':[(x['record50'],x['record51']) for x in curveqa]},ensure_ascii=False))
