from pathlib import Path
import xml.etree.ElementTree as ET
import copy,json,shutil
import numpy as np

R=Path(r'E:\0school\研二上\cvpr\uaca\draw')
O=R/'candidates/caption_axis_20261023'
P=R/'previews/caption_axis_20261023'
L=R/'logs/caption_axis_20261023'
for d in [O/'work',P,L]:d.mkdir(parents=True,exist_ok=True)
source=R/'final/head/UACA_head_simple.drawio'
original=ET.parse(source).getroot()
base=original.find('diagram/mxGraphModel')
source_stat=dict(size=source.stat().st_size,mtime_ns=source.stat().st_mtime_ns)
cells={c.get('id'):c for c in base.iter('mxCell')}
variants={}
changes={}
for key,label in [('A','Environment Steps'),('B','Environment Steps (k)')]:
 m=copy.deepcopy(base);cs={c.get('id'):c for c in m.iter('mxCell')}
 cs['r2_EXPO_xaxis'].set('value',label)
 ids=['r2_EXPO_xaxis']
 if key=='A':
  for i in range(4):
   n=cs['r2_EXPO_xt'+str(i)];n.set('value',n.get('value')+'k');ids.append(n.get('id'))
 diff=[]
 for i,c in cs.items():
  if ET.tostring(c)!=ET.tostring(cells[i]):
   assert i in ids,i
   a,b=copy.deepcopy(c),copy.deepcopy(cells[i]);a.attrib.pop('value',None);b.attrib.pop('value',None)
   assert ET.tostring(a)==ET.tostring(b),i
   diff.append(dict(id=i,before=cells[i].get('value'),after=c.get('value')))
 variants[key]=m;changes[key]=diff

def standalone(model,file,name):
 root=ET.Element('mxfile',host='app.diagrams.net',agent='UACA local editable candidates')
 d=ET.SubElement(root,'diagram',id='caption-axis-'+name,name=name);d.append(copy.deepcopy(model))
 ET.ElementTree(root).write(file,encoding='utf-8',xml_declaration=True)

# Reference and alternatives are side by side using the original EXPO objects.
comparison=copy.deepcopy(base);root=comparison.find('root');root.clear()
ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
comparison.set('pageWidth','970');comparison.set('pageHeight','285')
for n,(key,title,model) in enumerate([
 ('original','原版 · Actions (k)',base),
 ('A','A · 环境步数 · 刻度带 k',variants['A']),
 ('B','B · 环境步数 · 标题带 (k)',variants['B'])]):
 cs=list(model.find('root'));selected={'main_grpo_group'}
 changed=True
 while changed:
  prev=len(selected);selected.update(c.get('id') for c in cs if c.get('parent') in selected);changed=len(selected)>prev
 for c in cs:
  if c.get('id') not in selected:continue
  cc=copy.deepcopy(c)
  for attr in ['id','parent','source','target']:
   if cc.get(attr) in selected:cc.set(attr,key+'_'+cc.get(attr))
  if c.get('id')=='main_grpo_group':
   cc.set('parent','1');g=cc.find('mxGeometry');g.set('x',str(12+n*316));g.set('y','42')
  root.append(cc)
 c=ET.SubElement(root,'mxCell',id=key+'_heading',value=title,style='text;html=1;whiteSpace=nowrap;overflow=visible;fillColor=none;strokeColor=none;fontFamily=Arial;fontSize=16;fontColor=#333333;align=center;verticalAlign=middle;spacing=0;',vertex='1',parent='1')
 ET.SubElement(c,'mxGeometry',x=str(12+n*316),y='8',width='285',height='25',**{'as':'geometry'})

book=ET.Element('mxfile',host='app.diagrams.net',agent='UACA local editable candidates')
for name,m in [('01 · EXPO 三图对照',comparison),('02 · A · 刻度带 k · 整图',variants['A']),('03 · B · 标题带 (k) · 整图',variants['B'])]:
 d=ET.SubElement(book,'diagram',id='caption-axis-'+str(len(book)+1),name=name);d.append(copy.deepcopy(m))
ET.ElementTree(book).write(O/'EXPO_axis_candidates.drawio',encoding='utf-8',xml_declaration=True)
manifest=[]
for key,model in [('comparison',comparison),('head_A',variants['A']),('head_B',variants['B'])]:
 f=O/'work'/f'{key}.drawio';standalone(model,f,key)
 manifest.append(dict(file=str(f),stem=key,pdf=key.startswith('head')))
(L/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(L/'object_changes.json').write_text(json.dumps(dict(source=str(source),source_stat=source_stat,changes=changes,verified_other_object_changes=0),ensure_ascii=False,indent=2),encoding='utf-8')

# The historical exact plotted values are retained as supporting data.
ex=json.loads((R/'assets/candidates_20261017/curves/experiments.json').read_text(encoding='utf-8'))[0]
stats=[]
for label,seq in zip(['Old Clean','Old Editor U tau2'],ex['train']):
 a=np.asarray(seq,float);s=np.column_stack([a[49:,0],np.convolve(a[:,1],np.ones(50)/50,'valid')])
 v=s[s[:,0]<=35000];peak=v[np.argmax(v[:,1])]
 stats.append(dict(series=label,records=len(a),first_raw_x=float(a[0,0]),last_raw_x=float(a[-1,0]),first_ma50_x=float(s[0,0]),last_display_x=float(v[-1,0]),peak_actions=float(peak[0]),peak_success=float(peak[1])))
(L/'expo_source_summary.json').write_text(json.dumps(dict(task=ex['task'],MA=50,window_unit='training episodes',x_unit='cumulative executed training actions',records=stats),ensure_ascii=False,indent=2),encoding='utf-8')

renderer=(R/'scripts/export_head_simple_annotations_20261022.cjs').read_text(encoding='utf-8').replace('head_simple_annotations_20261022','caption_axis_20261023')
(R/'scripts/export_caption_axis_20261023.cjs').write_text(renderer,encoding='utf-8')
shutil.copy2(__file__,R/'scripts/uaca_caption_axis_build_20261023.py')
print(json.dumps(dict(book=str(O/'EXPO_axis_candidates.drawio'),changes=changes,stats=stats),ensure_ascii=False,indent=2))
