"""Rebuild portable SVG/PDF/PNG from derived CSV; Python + matplotlib only."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;O=R/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
rows=list(csv.DictReader((R/'derived/points.csv').open()))
for r in rows:
 for k in ['success_rate','whole_rate','first3_rate']:r[k]=float(r[k]) if r[k] else None
colors={'high':'#0072B2','low':'#D55E00'}
def plot(ax,family,field):
 for policy in ['high','low']:
  rr=sorted([r for r in rows if r['family']==family and r['policy']==policy],key=lambda r:r[field]);ax.plot([100*r[field]for r in rr],[100*r['success_rate']for r in rr],color=colors[policy],marker='D'if policy=='high'else'o',label=policy.capitalize()+' U',lw=2,ms=5)
 for pol,color in [('weak','#60666d'),('strong','#009E73')]:
  r=next(r for r in rows if r['family']==family and r['policy']==pol);ax.axhline(100*r['success_rate'],color=color,ls='--',lw=1.2,label=f"All {pol} (historical): {r['successes']}/{r['n']}")
 ax.set(xlabel='Whole-episode takeover decisions (%)'if field=='whole_rate'else'Takeover decisions in first 3 chunks (%)',ylabel='Episode success (%)',ylim=(25,70),xlim=(-1,35)if field=='whole_rate'else(-2,102));ax.grid(alpha=.18)
def save(fig,name):
 for ext in ['svg','pdf','png']:fig.savefig(O/(name+'.'+ext),bbox_inches='tight',dpi=160)
 plt.close(fig)
for field in ['whole_rate','first3_rate']:
 fig,ax=plt.subplots(figsize=(8.7,5.4));plot(ax,'G',field);ax.set_title('G: Clean CP140 → Uτ3 CP70 | C20 | First 3 chunks only');ax.legend(fontsize=9,loc='lower right');save(fig,'G-'+field)
fig,axs=plt.subplots(1,2,figsize=(14,5.2))
for ax,f in zip(axs,['G','H']):plot(ax,f,'whole_rate');ax.set_title('G: Only first 60 actions'if f=='G'else'H: Anywhere within 200 actions')
axs[1].legend(fontsize=8,loc='lower right');fig.suptitle('Same models and C20; different eligible time windows and calibration pools');fig.tight_layout();save(fig,'G-vs-H')
ds=list(csv.DictReader((R/'derived/decisions.csv').open()));fig,axs=plt.subplots(1,2,figsize=(12,4.8))
for c,lab,co in [('first3_high_p35','High U p35','#0072B2'),('first3_low_p55','Low U p55','#D55E00')]:
 rr=[d for d in ds if d['condition']==c];qs=sorted({int(d['query'])for d in rr});take=[];u=[]
 for q in qs:
  z=[d for d in rr if int(d['query'])==q];take.append(100*sum(int(d['strong'])for d in z)/len(z));u.append(sum(float(d['u'])for d in z)/len(z))
 axs[0].plot([q+1 for q in qs],take,'o-',c=co,label=lab);axs[1].plot([q+1 for q in qs],u,'o-',c=co,label=lab)
for ax in axs:ax.axvline(3.5,c='gray',ls='--',lw=1);ax.set_xlabel('Chunk number (1-based)');ax.grid(alpha=.18);ax.legend(fontsize=9)
axs[0].set_ylabel('Takeover among active episodes (%)');axs[1].set_ylabel('Mean current weak-policy U');fig.suptitle('Illustrative paired-budget points; later chunks condition on still-active episodes');fig.tight_layout();save(fig,'G-chunk-profile')
print('Figures rebuilt in',O)
