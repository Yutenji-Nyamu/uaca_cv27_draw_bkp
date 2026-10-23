from pathlib import Path
import copy,json,re,shutil,base64,zlib,urllib.parse
import xml.etree.ElementTree as E
R=Path(r'E:\0school\研二上\cvpr\uaca\draw');TAG='head_n39_swap_20261023'
L=R/'logs'/TAG;C=R/'candidates'/TAG;P=R/'previews'/TAG
for p in [L,C,P,C/'head',C/'elements',C/'appendix',C/'signals']:p.mkdir(parents=True,exist_ok=True)
if not (L/'before').exists():shutil.copytree(R/'final',L/'before')
S='main_dv_main_dv_layout_';PAR='main_dv_main_dv_group'
def load(p):return E.fromstring(Path(p).read_text(encoding='utf8'))
def ix(m):return {c.get('id'):c for c in m.find('root')}
def n(x):return str(round(float(x),6))
def geo(c,**kw):
    for k,v in kw.items():c.find('mxGeometry').set(k,n(v))
def points(c,xy):
    c.remove(c.find('mxGeometry'));g=E.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
    E.SubElement(g,'mxPoint',x=n(xy[0][0]),y=n(xy[0][1]),attrib={'as':'sourcePoint'})
    E.SubElement(g,'mxPoint',x=n(xy[-1][0]),y=n(xy[-1][1]),attrib={'as':'targetPoint'})
    if len(xy)>2:
        a=E.SubElement(g,'Array',attrib={'as':'points'})
        for x,y in xy[1:-1]:E.SubElement(a,'mxPoint',x=n(x),y=n(y))
def clone(root,source,ident,**kw):
    c=copy.deepcopy(source);c.set('id',ident)
    if kw:geo(c,**kw)
    root.append(c);return c
def save(model,path,title):
    b=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
    d=E.SubElement(b,'diagram',id=Path(path).stem,name=title);d.append(copy.deepcopy(model))
    E.ElementTree(b).write(path,encoding='utf-8',xml_declaration=True)

# Read the official DVCA native objects, rather than approximating their visual relationship.
ref=load(Path(r'E:\0school\研二上\iclr27\drawio\dvca head 0912.drawio'))
page=ref.findall('diagram')[0];reference_page_name=page.get('name');m=page.find('mxGraphModel')
if m is None:m=E.fromstring(urllib.parse.unquote(zlib.decompress(base64.b64decode(page.text),-15).decode()))
reference=ix(m)
appendix=load(L/'before/appendix/UACA_appendix_action_uncertainty.drawio')
n39page=next(d for d in appendix.findall('diagram') if d.get('id')=='N39')
n39=ix(n39page.find('mxGraphModel'))
data=json.loads((R/'assets/noise4_current_20261023/N39/series.json').read_text())
x,y=data['action'],data['noise4'];lookup=dict(zip(x,y))
redsteps=sorted(sorted(range(0,101,2),key=lambda t:lookup[t],reverse=True)[:4])
fx=lambda t:90+t/100*1144
fy=lambda u:348-u/.4*126
manifest=[]

def replace_signal(model):
    root=model.find('root');old=ix(model)
    before={k:E.tostring(c) for k,c in old.items()}
    prefixes=('u_stripe','u_grid','u_y','u_raw','u_tick','u_xt','u_x_end','u_dot','u_photo_guide','u_photo_step','u_frame_connector')
    for cell in list(root):
        if cell.get('id','').startswith(prefixes):root.remove(cell)
    for i,step in enumerate(range(0,100,4)):
        clone(root,reference[S+'1'],f'u_stripe_{i}',x=fx(step),y=222,width=22.88,height=126)
    for i,v in enumerate([0,.2,.4]):
        c=clone(root,old['u_grid0'],f'u_grid{i}');points(c,[(90,fy(v)),(1234,fy(v))])
        c=clone(root,old['u_y0'],f'u_y{i}',x=32,y=fy(v)-10,width=51,height=20);c.set('value',f'{v:.3f}')
    frame=old['u_frame'];root.remove(frame);root.append(frame)
    c=clone(root,old['u_raw_continuous'],'u_raw_continuous');points(c,[(fx(t),fy(lookup[t])) for t in range(101)])
    for i,step in enumerate(range(0,101,2)):
        template=reference[S+('71' if step in redsteps else '37')]
        clone(root,template,f'u_dot{i}',x=fx(step)-4.2,y=fy(lookup[step])-4.2,width=8.4,height=8.4)
    for i,step in enumerate(range(0,101,20)):
        c=clone(root,old['u_tick0'],f'u_tick{i}');points(c,[(fx(step),348),(fx(step),352)])
        c=clone(root,old['u_xt0'],f'u_xt{i}',x=fx(step)-22,y=352,width=44,height=20);c.set('value',str(step))
    for j,step in enumerate([5,16,48]):
        photo_id=[S+'109',S+'114',S+'119'][j]
        image=re.search(r'image=[^;]+',n39[photo_id].get('style')).group()
        old[photo_id].set('style',re.sub(r'image=[^;]+',lambda _:image,old[photo_id].get('style')))
        for ident in [['rev6_step26_label',S+'116',S+'121'][j],[S+'112',S+'117',S+'122'][j],[S+'113',S+'118',S+'123'][j]]:
            old[ident].set('value',n39[ident].get('value'))
        c=clone(root,old[f'u_photo_guide{j}'],f'u_photo_guide{j}');points(c,[(fx(step),222),(fx(step),348)])
        pg=old[photo_id].find('mxGeometry');cx=float(pg.get('x'))+float(pg.get('width'))/2
        c=clone(root,old[f'u_frame_connector{j}'],f'u_frame_connector{j}');points(c,[(cx,197),(cx,210),(fx(step),210),(fx(step),222)])
        clone(root,old[f'u_photo_step{j}'],f'u_photo_step{j}',x=fx(step)-9,y=201,width=18,height=19)
    old[S+'111'].set('value',n39[S+'111'].get('value'))
    # The longer task name already has the approved appendix task-label size.
    size=re.search(r'fontSize=[^;]+',n39[S+'111'].get('style')).group()
    old[S+'111'].set('style',re.sub(r'fontSize=[^;]+',size,old[S+'111'].get('style')))
    after=ix(model)
    changed={S+str(i) for i in [109,111,112,113,114,116,117,118,119,121,122,123]}|{'rev6_step26_label'}
    assert all(E.tostring(after[k])==v for k,v in before.items() if not k.startswith(prefixes) and k not in changed)
    assert len(after)==len(list(root))
    return model

for name in ['UACA_head_simple','UACA_head_current_layout']:
    model=load(R/'candidates/expo_warmup5_20261023'/f'{name}.drawio').find('diagram/mxGraphModel')
    replace_signal(model);dest=C/'head'/f'{name}.drawio';save(model,dest,name+' | N39 0-100')
    manifest.append(dict(file=str(dest),stem=name,pdf=True))
model=load(L/'before/elements/action_uncertainty.drawio').find('diagram/mxGraphModel')
replace_signal(model);save(model,C/'elements/action_uncertainty.drawio','N39 | 0-100 action steps')
manifest.append(dict(file=str(C/'elements/action_uncertainty.drawio'),stem='action_uncertainty',pdf=False))
shutil.copy2(R/'candidates/expo_warmup5_20261023/training_curves.drawio',C/'elements/training_curves.drawio')
manifest.append(dict(file=str(C/'elements/training_curves.drawio'),stem='training_curves',pdf=False))

# Exchange the selected role only: N75 goes back as its complete, marker-free appendix page.
newbook=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
for d in appendix.findall('diagram'):
    if d.get('id')!='N39':newbook.append(copy.deepcopy(d))
n75=load(R/'logs/noise4_current_20261023/native_pages/N75_full.drawio').find('diagram/mxGraphModel')
d=E.SubElement(newbook,'diagram',id='N75',name='N75 | turn_switch');d.append(copy.deepcopy(n75))
E.ElementTree(newbook).write(C/'appendix/UACA_appendix_action_uncertainty.drawio',encoding='utf-8',xml_declaration=True)
save(n75,C/'appendix/N75.drawio','N75 | full trajectory appendix')
manifest.append(dict(file=str(C/'appendix/N75.drawio'),stem='N75_turn_switch',pdf=False))
collection=E.Element('mxfile',host='app.diagrams.net',version='29.0.0',type='device')
d=E.SubElement(collection,'diagram',id='N39-head',name='HEAD | N39 place_burger_fries');d.append(copy.deepcopy(model))
for page in newbook.findall('diagram'):
    d=copy.deepcopy(page);d.set('name','APPENDIX | '+d.get('name'));collection.append(d)
E.ElementTree(collection).write(C/'signals/UACA_signal_collection.drawio',encoding='utf-8',xml_declaration=True)
assert len(newbook.findall('diagram'))==14 and len(collection.findall('diagram'))==15
qa=dict(head='N39',appendix=[d.get('id') for d in newbook.findall('diagram')],range=[0,100],raw_points=101,circle_steps=list(range(0,101,2)),circle_diameter=8.4,gray_bands=25,gray_band_width_actions=2,gray_period_actions=4,marker_pitch_px=22.88,red_steps=redsteps,frames=[5,16,48],y_limits=[0,.4],dvca_reference=dict(file='dvca head 0912.drawio',page=reference_page_name,gray_width_px=20.8,gray_period_px=41.6,marker_pitch_px=20.8,circle_diameter=8.4),alignment='each marker center is on a gray/white boundary; line retains all raw action points')
(L/'swap_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
(L/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
renderer=(R/'scripts/export_noise4_current_20261023.cjs').read_text(encoding='utf8').replace('noise4_current_20261023',TAG)
(R/'scripts'/('export_'+TAG+'.cjs')).write_text(renderer,encoding='utf8')
shutil.copy2(__file__,R/'scripts'/Path(__file__).name)
print(json.dumps(qa,ensure_ascii=False))
