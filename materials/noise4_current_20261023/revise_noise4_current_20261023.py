from pathlib import Path
import copy, json, math, re, shutil, base64, io
import xml.etree.ElementTree as E
import numpy as np
from PIL import Image

R=Path(r'E:\0school\研二上\cvpr\uaca\draw')
TAG='noise4_current_20261023'
L=R/'logs'/TAG; C=R/'candidates'/TAG; P=R/'previews'/TAG
A=R/'assets/noise4_appendix_20261023'
for p in [L,C,P,C/'head',C/'elements',C/'appendix',C/'signals',L/'native_pages']:p.mkdir(parents=True,exist_ok=True)
snapshot=L/'before'
if not snapshot.exists():shutil.copytree(R/'final',snapshot)

S='main_dv_main_dv_layout_'; PAR='main_dv_main_dv_group'
wording={
'N12':(['Initial reach','Roller approach','Roller alignment'],['Free-space motion','Where to grasp?','Ends within reach']),
'N17':(['Mug placement','Switching hands','Right-hand grasp'],['Mug on table','How to regrasp?','Grasp established']),
'N19':(['Initial reach','Handle approach','At pot handles'],['Free-space motion','How to align?','Grippers aligned']),
'N31':(['Initial reach','Bottle approach','At the bottles'],['Free-space motion','How to align?','Ready to grasp']),
'N35':(['Initial reach','Object approach','Above the object'],['Free-space motion','Which grasp pose?','Gripper aligned']),
'N39':(['Initial reach','Food approach','At the food'],['Free-space motion','How to grasp both?','Grippers aligned']),
'N43':(['Initial reach','Can approach','At the cans'],['Free-space motion','How to align?','Grippers aligned']),
'N45':(['Left-hand retreat','Shoe positioning','Lowering shoe'],['Free-space motion','How to orient?','Shoe aligned']),
'N49':(['Carry object','Object release','Gripper retreat'],['Object held','When to release?','Object in basket']),
'N52':(['Initial reach','Reach initiation','Object approach'],['Free-space motion','Where to grasp?','Gripper aligned']),
'N53':(['Hand retreat','Phone approach','Lift phone'],['Phone on table','Where to grasp?','Grasp established']),
'N56':(['Initial reach','Stapler approach','Above stapler'],['Free-space motion','Where to press?','Ready to press']),
'N63':(['Initial reach','Bottle approach','Above bottle'],['Free-space motion','Where to grasp?','Gripper aligned']),
'N71':(['Bowl released','Switching hands','Right-hand reach'],['Bowl on table','Which hand next?','Next bowl targeted']),
'N75':(['Initial reach','Switch approach','At the switch'],['Free-space motion','How to align?','Ready to press'])}
rows=[r for r in json.loads((A/'selection.json').read_text(encoding='utf8')) if r['id']!='N20']
byid={r['id']:r for r in rows}
manifest=[];qa=[];audit=[]

def n(v):return str(round(float(v),6))
def load(p):return E.fromstring(Path(p).read_text(encoding='utf8'))
def cells(model):return {c.get('id'):c for c in model.find('root')}
def geo(c,**kw):
    for k,v in kw.items():c.find('mxGeometry').set(k,n(v))
def style(c,**kw):
    s=[p for p in c.get('style','').split(';') if p and p.split('=')[0] not in kw]
    c.set('style',';'.join(s)+';'+''.join(f'{k}={v};' for k,v in kw.items()))
def pts(c,points):
    c.remove(c.find('mxGeometry'))
    g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    E.SubElement(g,'mxPoint',x=n(points[0][0]),y=n(points[0][1]),attrib={'as':'sourcePoint'})
    E.SubElement(g,'mxPoint',x=n(points[-1][0]),y=n(points[-1][1]),attrib={'as':'targetPoint'})
    if len(points)>2:
        a=E.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in points[1:-1]:E.SubElement(a,'mxPoint',x=n(x),y=n(y))
def clone(root,source,ident,**kw):
    c=copy.deepcopy(source);c.set('id',ident)
    if kw:geo(c,**kw)
    root.append(c);return c
def save(model,path,title):
    book=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
    page=E.SubElement(book,'diagram',id=Path(path).stem,name=title);page.append(copy.deepcopy(model))
    E.ElementTree(book).write(path,encoding='utf-8',xml_declaration=True)
def add_render(model,path,stem,title,pdf=False):
    save(model,path,title);manifest.append(dict(file=str(path),stem=stem,pdf=pdf))
def photo(c,path):
    im=Image.open(path).convert('RGB');b=io.BytesIO();im.save(b,format='JPEG',quality=96)
    c.set('style',re.sub(r'image=[^;]+','image=data:image/jpeg,'+base64.b64encode(b.getvalue()).decode(),c.get('style')))
def revise_annotations(model,row,record=False):
    ix=cells(model);root=model.find('root');phases,reasons=wording[row['id']]
    for c in list(root):
        if c.get('id','').startswith('u_photo_letter'):root.remove(c)
    for j in range(3):
        p=ix[[S+'112',S+'117',S+'122'][j]];r=ix[[S+'113',S+'118',S+'123'][j]]
        if record:audit.append(dict(id=row['id'],letter='ABC'[j],step=row['steps'][j],before=[p.get('value'),r.get('value')],after=[phases[j],reasons[j]]))
        p.set('value',phases[j]);r.set('value',reasons[j])
        row['selected_frames'][j].update(phase=phases[j],explanation=reasons[j])
    return model

# Same native appendix pages; only remove the rejected duplicate, revise captions,
# and remove the photo-corner letters. All raw curves and selected frames stay fixed.
oldbook=load(R/'drafts/appendix/UACA_noise4_selected16_20261023.drawio')
appendixbook=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
appendix_models={}
for page in oldbook.findall('diagram'):
    ident=page.get('id').removeprefix('noise4-')
    if ident not in byid:continue
    model=revise_annotations(copy.deepcopy(page.find('mxGraphModel')),byid[ident],True)
    root=model.find('root');ix=cells(model)
    assert not any(c.get('id','').startswith(('u_photo_letter','u_dot','u_frame_connector')) for c in root)
    assert E.tostring(ix['u_raw_continuous'])==E.tostring(cells(page.find('mxGraphModel'))['u_raw_continuous'])
    qa.append(dict(id=ident,full_trajectory_points=len(json.loads((A/ident/'series.json').read_text())['action']),photos=byid[ident]['steps'],photo_badges=0))
    if ident=='N75':
        add_render(model,L/'native_pages/N75_full.drawio','N75_full','N75 | full trajectory reference')
    else:
        appendix_models[ident]=model
        d=E.SubElement(appendixbook,'diagram',id=ident,name=f'{ident} | {byid[ident]["task"]}');d.append(copy.deepcopy(model))
        add_render(model,L/f'native_pages/{ident}.drawio',ident,f'{ident} | full action-level uncertainty')
E.ElementTree(appendixbook).write(C/'appendix/UACA_appendix_action_uncertainty.drawio',encoding='utf-8',xml_declaration=True)

def replace_head_signal(model):
    row=byid['N75'];ix=cells(model);root=model.find('root')
    revise_annotations(model,row)
    data=json.loads((A/'N75/series.json').read_text());xx=data['action'];yy=data['noise4']
    lo,hi=0,65;ymax=.23
    fx=lambda v:90+(v-lo)/(hi-lo)*1144
    fy=lambda v:348-v/ymax*126
    prefixes=('u_stripe','u_grid','u_y','u_raw','u_tick','u_xt','u_x_end','u_photo_guide','u_photo_step','u_peak','u_dot','u_frame_connector')
    for c in list(root):
        if c.get('id','').startswith(prefixes):root.remove(c)
    for j,step in enumerate(range(lo,hi,2)):
        clone(root,ix['u_stripe_0'],f'u_stripe_{j}',x=fx(step),y=222,width=1144/65,height=126)
    for j,v in enumerate([0,.1,.2]):
        c=clone(root,ix['u_grid0'],f'u_grid{j}');pts(c,[(90,fy(v)),(1234,fy(v))])
        c=clone(root,ix['u_y0'],f'u_y{j}',x=32,y=fy(v)-10,width=51,height=20);c.set('value',f'{v:.3f}')
    frame=ix['u_frame'];root.remove(frame);root.append(frame)
    c=clone(root,ix['u_raw_continuous'],'u_raw_continuous');pts(c,[(fx(x),fy(y)) for x,y in zip(xx,yy) if lo<=x<=hi])
    for j,v in enumerate([0,10,20,30,40,50,60,65]):
        c=clone(root,ix['u_tick0'],f'u_tick{j}');pts(c,[(fx(v),348),(fx(v),352)])
        c=clone(root,ix['u_xt0'],f'u_xt{j}',x=fx(v)-22,y=352,width=44,height=20);c.set('value',str(v))
    reds={26,28,30,32}
    for j,step in enumerate(range(lo,hi+1,2)):
        t=ix['u_dot18'] if step in reds else ix['u_dot0']
        c=clone(root,t,f'u_dot{j}',x=fx(step)-4.2,y=fy(yy[xx.index(step)])-4.2,width=8.4,height=8.4)
        style(c,fillColor='#EC7063' if step in reds else '#FFFFFF',strokeColor='#4D4D4D' if step in reds else '#5DADE2',strokeWidth=.65 if step in reds else 1.6)
    for j,step in enumerate(row['steps']):
        f=row['selected_frames'][j]
        pic=ix[[S+'109',S+'114',S+'119'][j]];photo(pic,R/f['file'])
        ix[['rev6_step26_label',S+'116',S+'121'][j]].set('value',f'Step {step}')
        c=clone(root,ix[f'u_photo_guide{j}'],f'u_photo_guide{j}');pts(c,[(fx(step),222),(fx(step),348)])
        pg=pic.find('mxGeometry');cx=float(pg.get('x'))+float(pg.get('width'))/2
        c=clone(root,ix[f'u_frame_connector{j}'],f'u_frame_connector{j}');pts(c,[(cx,197),(cx,210),(fx(step),210),(fx(step),222)])
        c=clone(root,ix[f'u_photo_step{j}'],f'u_photo_step{j}',x=fx(step)-9,y=201,width=18,height=19)
    return model

def replace_noise_source(model,prefix):
    ix=cells(model);root=model.find('root');get=lambda i:ix[prefix+'n'+str(i)]
    gray=get(5002);gg=gray.find('mxGeometry');x=float(gg.get('x'));w=float(gg.get('width'))
    first=get(5008);last=get(5017);g1=first.find('mxGeometry');g4=last.find('mxGeometry')
    cy1=float(g1.get('y'))+22;cy4=float(g4.get('y'))+22
    gray.set('value','<b>A</b><sub>1</sub><sup>0</sup>');geo(gray,y=cy1-25);style(gray,fontSize=23)
    gray4=clone(root,gray,prefix+'noise4_initial4',y=cy4-25);gray4.set('value','<b>A</b><sub>4</sub><sup>0</sup>')
    root.remove(get(5004))
    for edge,extra,cy in [(5005,5006,cy1),(5014,5015,cy4)]:
        c=get(edge);c.attrib.pop('source',None);c.attrib.pop('target',None)
        pts(c,[(x+w,cy),(float(g1.get('x')),cy)]);style(c,endArrow='block')
        if prefix+'n'+str(extra) in ix:root.remove(get(extra))
    for i,k,sup in [(5008,1,'τ'),(5009,1,'τ+δ'),(5010,1,None),(5017,4,'τ'),(5018,4,'τ+δ'),(5019,4,None)]:
        get(i).set('value',f'<b>A</b><sub>{k}</sub>'+('' if sup is None else f'<sup>{sup}</sup>'))
        if i in [5008,5017]:style(get(i),fontSize=22)
        if i in [5009,5018]:style(get(i),fontSize=19)
    for i in [5007,5016]:get(i).set('value','10 NFEs')
    prior=get(5003);prior.set('value','<b>A</b><sub>k</sub><sup>0</sup> ∼ 𝒩(0, I)');prior.set('parent',gray.get('parent'))
    compact=cy4-cy1<140
    geo(prior,x=x-39,y=cy4+(27 if compact else 34),width=180,height=20 if compact else 26);style(prior,fontSize=18 if compact else 20)
    dots=clone(root,get(5001),prefix+'noise4_ellipsis',x=float(g1.get('x'))+12,y=(cy1+cy4)/2-16,width=20,height=25)
    dots.set('value','⋮');style(dots,fontFamily='VGPOMath',fontSize=28,fontColor='#222222',fontStyle=0)
    k=clone(root,get(5001),prefix+'noise4_K',x=x-12,y=(cy1+cy4)/2-12,width=76,height=24)
    k.set('value','K = 4');style(k,fontFamily='VGPOMath',fontSize=19,fontColor='#222222',fontStyle=2)
    return model

experiments=json.loads((R/'assets/candidates_20261017/curves/experiments.json').read_text())
curve_qa=[]
def partial_ma(a,w=50):
    a=np.array(a,float);s=np.r_[0,np.cumsum(a[:,1])];i=np.arange(len(a))+1;start=np.maximum(0,i-w)
    return np.column_stack((a[:,0],(s[i]-s[start])/(i-start)))
def restore_curves(model):
    root=model.find('root');ix=cells(model)
    oldrlt={k:E.tostring(v) for k,v in ix.items() if k.startswith('r2_RLT')}
    for exp in experiments[:2]:
        family=exp['id'];p='r2_'+family;group=ix[p+'_curve0'].get('parent')
        xmax=35000 if family=='EXPO' else 168
        ymin,ymax=(15,105) if family=='EXPO' else (15,80)
        fx=lambda v:37.6+v/xmax*226.4
        fy=lambda v:180.8-(v-ymin)/(ymax-ymin)*172.8
        series=[partial_ma(a) for a in exp['train']]
        peaks=[];counts=[]
        for j,a in enumerate(series):
            a=a[a[:,0]<=xmax];counts.append(len(a));pts(ix[p+f'_curve{j}'],[(fx(x),fy(y)) for x,y in a])
            stable=a[49:];px,py=stable[np.argmax(stable[:,1])];peaks.append((float(px),float(py)))
            g=ix[p+f'_star{j}'].find('mxGeometry');size=float(g.get('width'))
            geo(ix[p+f'_star{j}'],x=fx(px)-size/2,y=fy(py)-size/2)
            pts(ix[p+f'_peak_h{j}'],[(37.6,fy(py)),(fx(px),fy(py))])
            # First complete window and all later windows exactly reproduce the prior MA50.
            raw=np.array(exp['train'][j],float)
            assert np.allclose(partial_ma(raw)[49:,1],np.convolve(raw[:,1],np.ones(50)/50,'valid'))
        for c in list(root):
            if c.get('id','').startswith((p+'_grid',p+'_yt',p+'_xt')):root.remove(c)
        ticks=[20,40,60,80,100] if family=='EXPO' else [20,40,60,80]
        for j,v in enumerate(ticks):
            c=clone(root,ix[p+'_grid0'],p+f'_grid{j}');pts(c,[(37.6,fy(v)),(264,fy(v))])
            c=clone(root,ix[p+'_yt0'],p+f'_yt{j}',y=fy(v)-9.88);c.set('value',str(v))
        ticks=[0,50,100,150,200,250] if family=='EXPO' else [0,50,100,150]
        for j,v in enumerate(ticks):
            x=v/250*xmax if family=='EXPO' else v
            c=clone(root,ix[p+'_xt0'],p+f'_xt{j}',x=fx(x)-19,y=185.8,width=38,height=19.76);c.set('value',str(v))
        if family=='EXPO':ix[p+'_xaxis'].set('value','Training Steps (approx.)')
        y0,y1=[fy(py) for px,py in peaks]
        # Existing peak values refer to full 50-record windows; the warm-up is now also visible.
        for j,key in enumerate(['_bpeak','_upeak']):
            c=ix[p+key];c.set('value',f'{peaks[j][1]:.2f}%');geo(c,x=48.8,y=(y0+1 if j==0 else y1-17))
        bx=89 if family=='EXPO' else 113.6
        pts(ix[p+'_bracket'],[(bx-5.6,y1),(bx,y1),(bx,y0),(bx-5.6,y0)])
        c=ix[p+'_gain'];c.set('value',f'+{peaks[1][1]-peaks[0][1]:.2f}');geo(c,x=bx+7.2,y=(y0+y1)/2-7.2)
        if family=='EXPO':
            geo(ix[p+'_bpeak'],x=45.5);geo(ix[p+'_upeak'],x=45.5)
        if family=='EXPO':
            c=clone(root,ix[p+'_upeak'],p+'_peak_scope',x=107,y=12,width=145,height=17)
            c.set('value','MA50 peaks');style(c,fontColor='#555555',fontSize=12,align='right')
        # Restore z order: grid under curves/labels, original legends above.
        grid=[c for c in list(root) if c.get('id','').startswith(p+'_grid')]
        for c in grid:root.remove(c)
        at=list(root).index(ix[p+'_frame'])
        for j,c in enumerate(grid):root.insert(at+j,c)
        if not any(q['id']==family for q in curve_qa):curve_qa.append(dict(id=family,window=50,min_periods=1,x_limits=[0,xmax],y_limits=[ymin,ymax],points=counts,full_window_peaks=peaks,display_ticks=ticks,axis_units='approximate training rounds, 140 actions per displayed step' if family=='EXPO' else 'training rounds'))
    assert all(E.tostring(cells(model)[k])==v for k,v in oldrlt.items())
    return model

# Stage both parallel head versions and the independent components.
for name in ['UACA_head_simple','UACA_head_current_layout']:
    model=load(snapshot/'head'/f'{name}.drawio').find('diagram/mxGraphModel')
    before=cells(copy.deepcopy(model))
    replace_head_signal(model);replace_noise_source(model,'method_final_');restore_curves(model)
    after=cells(model)
    untouched=[]
    # All real-world photographs and their four task names are preserved.
    for k,c in before.items():
        if k.startswith('main_real_'):assert E.tostring(c)==E.tostring(after[k]);untouched.append(k)
    assert len(set(after))==len(list(model.find('root')))
    add_render(model,C/'head'/f'{name}.drawio',name,name+' | N75 noise4 | partial MA50',True)
for name in ['action_uncertainty','method','training_curves']:
    model=load(snapshot/'elements'/f'{name}.drawio').find('diagram/mxGraphModel')
    if name=='action_uncertainty':replace_head_signal(model)
    elif name=='method':replace_noise_source(model,'')
    else:restore_curves(model)
    add_render(model,C/'elements'/f'{name}.drawio',name,name+' | noise4 current')

collection=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
headmodel=load(C/'elements/action_uncertainty.drawio').find('diagram/mxGraphModel')
d=E.SubElement(collection,'diagram',id='N75-head',name='HEAD | N75 turn_switch');d.append(copy.deepcopy(headmodel))
for ident,model in appendix_models.items():
    d=E.SubElement(collection,'diagram',id=ident,name=f'APPENDIX | {ident} {byid[ident]["task"]}');d.append(copy.deepcopy(model))
E.ElementTree(collection).write(C/'signals/UACA_signal_collection.drawio',encoding='utf-8',xml_declaration=True)
(C/'signals/selection.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
(L/'annotation_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
(L/'curve_qa.json').write_text(json.dumps(curve_qa,ensure_ascii=False,indent=2),encoding='utf8')
(L/'signal_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
(L/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copy2(__file__,R/'scripts'/Path(__file__).name)
print(json.dumps(dict(appendix_pages=len(appendix_models),collection_pages=len(collection.findall('diagram')),render_jobs=len(manifest),curves=curve_qa),ensure_ascii=False))
