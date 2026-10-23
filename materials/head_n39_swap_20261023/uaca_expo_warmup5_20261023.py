from pathlib import Path
import copy,json,shutil,xml.etree.ElementTree as E
import numpy as np

R=Path(r'E:\0school\研二上\cvpr\uaca\draw');TAG='expo_warmup5_20261023'
L=R/'logs'/TAG;C=R/'candidates'/TAG;P=R/'previews'/TAG
for p in [L,C,P,L/'before']:p.mkdir(parents=True,exist_ok=True)
exps=json.loads((R/'assets/candidates_20261017/curves/experiments.json').read_text())
manifest=[];qa=[]
def n(x):return str(round(float(x),6))
def geo(c,**kw):
    for k,v in kw.items():c.find('mxGeometry').set(k,n(v))
def points(c,xy):
    c.remove(c.find('mxGeometry'));g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    E.SubElement(g,'mxPoint',x=n(xy[0][0]),y=n(xy[0][1]),attrib={'as':'sourcePoint'})
    E.SubElement(g,'mxPoint',x=n(xy[-1][0]),y=n(xy[-1][1]),attrib={'as':'targetPoint'})
    a=E.SubElement(g,'Array',attrib={'as':'points'})
    for x,y in xy[1:-1]:E.SubElement(a,'mxPoint',x=n(x),y=n(y))
def clone(root,source,ident,**kw):
    c=copy.deepcopy(source);c.set('id',ident);geo(c,**kw);root.append(c);return c
def smooth(seq,center5):
    raw=np.array(seq,float)
    y=np.array([raw[max(0,i-49):i+1,1].mean() for i in range(len(raw))])
    if center5:
        for i in range(5):y[i]=raw[max(0,i-5):min(len(raw),i+6),1].mean()
    return np.column_stack((raw[:,0],y))
def clip_lower(a,ymin):
    # Ordinary plot clipping. All following points are above the lower limit.
    valid=np.flatnonzero(a[:,1]>=ymin)
    k=int(valid[0]);assert np.all(a[k:,1]>=ymin)
    if k==0:return a
    x0,y0=a[k-1];x1,y1=a[k];cross=x0+(ymin-y0)/(y1-y0)*(x1-x0)
    return np.vstack(([cross,ymin],a[k:]))

for rel in ['head/UACA_head_simple','head/UACA_head_current_layout','elements/training_curves']:
    source=R/'final'/(rel+'.drawio');name=Path(rel).name
    for ext in ['drawio','png','pdf']:
        old=source.with_suffix('.'+ext);dest=L/'before'/old.name
        if old.exists() and not dest.exists():shutil.copy2(old,dest)
    book=E.fromstring(source.read_text(encoding='utf8'));model=book.find('diagram/mxGraphModel');root=model.find('root')
    ix={c.get('id'):c for c in root};before={k:E.tostring(v) for k,v in ix.items()}
    for family,ymin,ymax in [('EXPO',15,85),('GRPO',35,80)]:
        exp=next(e for e in exps if e['id']==family);prefix='r2_'+family
        xmax=35000 if family=='EXPO' else 168
        fx=lambda v:37.6+v/xmax*226.4
        fy=lambda v:180.8-(v-ymin)/(ymax-ymin)*172.8
        peaks=[];first5=[];clipped=[]
        for j,seq in enumerate(exp['train']):
            a=smooth(seq,family=='EXPO');a=a[a[:,0]<=xmax]
            old=smooth(seq,False);assert np.allclose(a[5:,1],old[:len(a)][5:,1])
            displayed=clip_lower(a,ymin);points(ix[prefix+f'_curve{j}'],[(fx(x),fy(y)) for x,y in displayed])
            px,py=a[np.argmax(a[:,1])];peaks.append([float(px),float(py)])
            g=ix[prefix+f'_star{j}'].find('mxGeometry');size=float(g.get('width'))
            geo(ix[prefix+f'_star{j}'],y=fy(py)-size/2)
            points(ix[prefix+f'_peak_h{j}'],[(37.6,fy(py)),(fx(px),fy(py))])
            first5.append(a[:5,1].tolist());clipped.append(len(a)-len(displayed)+1 if a[0,1]<ymin else 0)
        for cell in list(root):
            if cell.get('id','').startswith((prefix+'_grid',prefix+'_yt')):root.remove(cell)
        ticks=[20,40,60,80] if family=='EXPO' else [40,60,80]
        grid=[]
        for i,v in enumerate(ticks):
            cell=clone(root,ix[prefix+'_grid0'],prefix+f'_grid{i}');points(cell,[(37.6,fy(v)),(264,fy(v))]);grid.append(cell)
            cell=clone(root,ix[prefix+'_yt0'],prefix+f'_yt{i}',y=fy(v)-9.88);cell.set('value',str(v))
        for cell in grid:root.remove(cell)
        pos=list(root).index(ix[prefix+'_frame'])
        for i,cell in enumerate(grid):root.insert(pos+i,cell)
        yb,yu=[fy(p[1]) for p in peaks]
        geo(ix[prefix+'_upeak'],y=yu-17);geo(ix[prefix+'_bpeak'],y=yb+1)
        bx=89 if family=='EXPO' else 113.6
        points(ix[prefix+'_bracket'],[(bx-5.6,yu),(bx,yu),(bx,yb),(bx-5.6,yb)])
        geo(ix[prefix+'_gain'],y=(yb+yu)/2-7.2)
        if family=='EXPO' and prefix+'_peak_scope' in ix:root.remove(ix[prefix+'_peak_scope'])
        if name=='UACA_head_simple':qa.append(dict(id=family,y_limits=[ymin,ymax],x_limits=[0,xmax],first5_values=first5,display_peaks=peaks,initial_records_below_axis=clipped,first5_rule='mean of original records within center +/- 5, inclusive; truncate at beginning' if family=='EXPO' else 'trailing MA50, min_periods=1',from_record6='unchanged trailing MA50 with min_periods=1'))
    # The edit is confined to EXPO/GRPO chart content required by the two requests.
    allowed=tuple('r2_'+f+'_'+s for f in ['EXPO','GRPO'] for s in ['curve','grid','yt','star','peak_h','upeak','bpeak','bracket','gain','peak_scope'])
    after={c.get('id'):E.tostring(c) for c in root}
    assert all(after[k]==v for k,v in before.items() if not k.startswith(allowed))
    out=C/(name+'.drawio');E.ElementTree(book).write(out,encoding='utf-8',xml_declaration=True)
    manifest.append(dict(file=str(out),stem=name,pdf=rel.startswith('head/')))
(L/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(L/'curve_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
renderer=(R/'scripts/export_noise4_current_20261023.cjs').read_text(encoding='utf8').replace('noise4_current_20261023',TAG)
(R/'scripts'/('export_'+TAG+'.cjs')).write_text(renderer,encoding='utf8')
shutil.copy2(__file__,R/'scripts'/Path(__file__).name)
print(json.dumps(qa,ensure_ascii=False))
