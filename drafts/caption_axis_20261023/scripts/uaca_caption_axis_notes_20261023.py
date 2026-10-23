from pathlib import Path
import json,html,shutil,re
R=Path(r'E:\0school\研二上\cvpr\uaca\draw');O=R/'candidates/caption_axis_20261023';P=R/'previews/caption_axis_20261023';L=R/'logs/caption_axis_20261023'
source={p['id']:p for p in json.loads((O/'references/caption_sources.json').read_text(encoding='utf-8'))}
rows=[
('0 · 直接模板','dvca_own','DVCA','DVCA 概览。去噪方差表征动作生成中的不确定性，DVCA 在训练时提高更不确定动作的权重。它可即插即用地接入不同的流式机器人策略和在线后训练方法，提升性能与样本效率。','最贴近当前整张头图：信号、干预、适用范围、收益，四项构成一条叙事。'),
('1 · 策略内生不确定性','ugrow','U-GROW','U-GROW 整体概览。','首图图注只有这一句；图内承担方法解释。我们的图含曲线和真机任务，可采用更完整的概览句。'),
('1 · 策略内生不确定性','dvac','Denoising Tells When to Replan / DVAC','首图展示去噪方差与操作阶段的关系：一个 LIBERO 回合中，自由移动时信号较低，接触操作时升高；跨任务统计也显示，操作阶段的平均方差更大。','先讲可见现象，再交代实例和汇总统计。适合上方信号框的叙事。'),
('1 · 策略内生不确定性','geometry','The Geometry of Flow-Matching Uncertainty','首图以两种示意地形对照置信与不确定的流匹配速度场；场沿地形下降方向运动，深红色曲线表示从不同噪声出发的去噪路径。','用图形关系解释信号来源，同时明确线条的语义。'),
('2 · 动作、token 与阶段级学习信号','attena','AttenA+','该框架从速度场构造动作注意力，将学习重点分配给缓慢而关键的操作步骤。图注同时交代其对判别式、生成式及世界动作模型的适配，以及在 LIBERO、RoboTwin 上的成功率收益。','最值得借鉴：短句说明信号和训练重点，再说明跨架构适用性。'),
('2 · 动作、token 与阶段级学习信号','entropy80','Beyond the 80/20 Rule','推理链中的少数高熵 token 对应推理路径的分岔。仅使用这些位置的策略梯度也能带来显著收益，并随模型规模增强；图注进一步报告 32B 模型在两届 AIME 上的成绩及更长生成预算带来的提升。','把少数局部位置的现象直接连接到训练收益。'),
('2 · 动作、token 与阶段级学习信号','sarm','SARM','方法图依次展示数据处理、奖励模型训练，以及使用奖励信号训练策略。图注区分奖励模型使用的带标注数据，以及包含次优轨迹的多样化未标注专家数据。','当图里数据流较多时，按子图次序解释对象与去向。'),
('2 · 动作、token 与阶段级学习信号','vgpo','VGPO','首图用一个视觉推理例子说明：VGPO 在早期关注问题和图像，并在后续推理中保持更强、更持久的视觉关注，使推理持续依托视觉证据。','首图是现象对比；先前用于风格参考的方法总览在图 3，两者已分开记录。'),
('3 · 通用策略优化与在线后训练','expo','EXPO','左侧解释 EXPO 如何稳定、高效地训练表达能力较强的策略：其优化避免将这类策略直接置于价值函数的梯度优化路径中。右侧汇总 EXPO 与既有方法在多个任务上的平均表现。','方法框和结果图各用一句，适合“统一接入机制＋增益”结构。'),
('3 · 通用策略优化与在线后训练','dppo','DPPO','DPPO 用策略梯度微调预训练扩散策略，将去噪过程建模为一个 MDP，让环境奖励传入去噪链，并利用每步可计算的高斯似然更新。图注最后概括仿真及硬件实验中的探索、稳定性、鲁棒性和泛化效果。','先给关键机制，再给实验收益；较长，适合机制图而非我们当前简短头图。'),
('3 · 通用策略优化与在线后训练','parl','PA-RL','PA-RL 用统一的 actor–critic 过程支持不同策略类别和骨干网络的离线学习与在线微调。首图图注强调复用预训练先验，并以少量示范或零样本尝试初始化后，约 40 分钟的真机改进及仿真结果说明其适用范围。','“可接入哪些策略＋在线学习带来什么”写得清楚，适合借鉴通用性表达。'),
('3 · 通用策略优化与在线后训练','pirl','πRL','框架以 Flow-Noise 和 Flow-SDE 两条路径支持流式 VLA 的在线强化学习，改善分布内性能与分布外泛化。图注还强调少样本 SFT 配合 RL 的效果，以及利用 3D Gaussian Splatting 仿真缩小视觉差异、实现零样本迁移到真机。','按图中主要贡献分段描述；我们的头图可只保留统一机制和结果两项。'),
('4 · 高效适配与一致性生成','expo_ft','EXPO-FT','首图比较不同方法的平均训练成功率；EXPO-FT 在较少交互下获得可靠提升，而若干对照方法的收敛稳定性较弱。','结果型首图直接说测量对象、比较对象与结果。'),
('4 · 高效适配与一致性生成','rl_token','RL Token','首图展示如何借助编码器和解码器，把 VLA 内部特征压缩成具有任务意义的 RL token，再用这一表征训练轻量 actor–critic，使精细操作可通过数小时乃至数分钟的机器人经验得到改进。','表征来源、接入接口、训练模块和实际效果串成一个流程。'),
('4 · 高效适配与一致性生成','consistency_policy','Consistency Policy','首图对比从随机动作去噪到预测动作的两种过程：Diffusion Policy 通过多个去噪步骤生成动作；Consistency Policy 用单步生成缩短推理时间，同时维持有竞争力的成功率。不同颜色的点表示生成过程中不同阶段的动作序列。','先给共同起点，再用生成路径表达机制差异。'),
('4 · 高效适配与一致性生成','shortcut','Shortcut Models','首图在多种推理预算下对比流匹配模型与 shortcut 模型。后者在单次前向到多步生成之间都能维持较好的质量；同一列共享初始噪声，便于观察预算变化的影响。','对我们最相关的是同噪声、不同预算的比较条件；图注明确交代了这一点。'),
('4 · 高效适配与一致性生成','flowpolicy','FlowPolicy','首图用推理耗时与平均成功率两个维度，对照 FlowPolicy、二维 DP 以及三维 DP3、Simple DP3，在 Adroit 和 Metaworld 上展示效率与性能的关系。','首图是结果对照；完整方法流程在图 2。适合学习简短、明确的比较口径。'),
]
source['flowpolicy'].update(url='https://ojs.aaai.org/index.php/AAAI/article/view/33617',pdf='https://ojs.aaai.org/index.php/AAAI/article/view/33617/35772')
caps=[
('A · 推荐 · 贴近 DVCA 的完整概览','UACA 概览。UACA 以策略自一致性估计逐动作不确定性，并据此重加权在线后训练中的优势或监督损失，优先学习高不确定性动作。该机制可接入不同的流式机器人策略和后训练算法，在仿真与真机任务中提升成功率与样本效率。'),
('B · 更短 · 接近 DVCA 的长度','UACA 利用策略自一致性估计逐动作不确定性，并优先学习高不确定性动作。作为可插拔的重加权机制，UACA 在不同流式机器人策略与在线后训练算法上提升性能及样本效率。'),
('C · 强调信号来源和统一接口','UACA 概览。在相同观察与初始噪声下，UACA 比较不同去噪步数生成的动作，以估计逐动作不确定性。该自一致性信号用于重加权 GRPO 优势、逐动作回归损失或流匹配损失，从而提高在线后训练的成功率与样本效率。'),
('D · 按当前上下两行读图','UACA 概览。上：比较相同输入与初始噪声、不同推理预算下的动作预测，估计逐动作不确定性，并通过执行帧展示信号随任务阶段的变化。下：将该信号接入在线后训练的学习目标，在不同方法及仿真与真机任务中获得性能和样本效率提升。'),
]
def links(key):
 s=source[key]
 if key=='dvca_own':return '[本地正文](<E:/0school/研二上/iclr27/overleaf-iclr2027/iclr2027_conference.tex:84>)'
 return f"[首图来源]({s['url']}) · [PDF]({s['pdf']})"
out=['# UACA 头图图注：分组参考与中文候选','',
'日期：2026-10-23。收录自身 DVCA 及 16 篇相关工作的首图图注，共 17 篇；另列 UA-OPD 的已核对入口。按与当前头图的关联度和写作参考价值选择，组内顺序用于阅读。',
'','以下相关论文均为**图注中文转述**，保留图注的信息和组织方式；“借鉴点”是本次针对 UACA 的判断。每项链接可查看原文。当前稿先讨论中文。',
'','最建议用 DVCA 的“信号 → 重加权 → 适用范围 → 收益”结构，吸收 AttenA+ 的跨模型表述，以及 RL Token 的来源到接口表述。U-GROW 的首图图注极短；VGPO、FlowPolicy 的首图分别是现象图、结果图，应与其后续方法总览区分。','']
group=''
for g,key,name,para,borrow in rows:
 if g!=group:out+=['## '+g,''];group=g
 out += ['### '+name+' · 图 1','',para,'','借鉴点：'+borrow,'',links(key),'']
out+=['### 补充：UA-OPD','',
'已核对题名与作者主页：When to Trust Your Teacher: Uncertainty-Aware On-Policy Distillation for Embodied Policies。OpenReview PDF 当前返回验证页面；图注列为待补。已收集的方法图继续保存在本地参考目录。',
'','[论文页面](https://openreview.net/forum?id=hHUZi8oHfo) · [PDF 入口](https://openreview.net/pdf?id=hHUZi8oHfo) · [作者主页](https://rhx11111.github.io/)','',
'## UACA 中文候选','',
'现有句子侧重“U_h 如何重加权 S_h，以及 GRPO/MSE/FM 接口”。现在的整张头图还包含逐动作实例、训练曲线和真机任务，因此 A、B 将适用范围和收益一并纳入。','']
for title,cap in caps:out+=['### '+title,'',cap,'']
out+=['推荐 A。它保留当前已选定的“策略自一致性／逐动作不确定性”，也将优势和监督损失的接入方式交代完整。若版面紧，选 B。C 更偏方法定义，D 更适合希望 caption 显式引导上下两行阅读的写法。','',
'本轮论文图注候选保存在此处；Overleaf 新增 0、修改 0、删除 0。','']
(O/'01_CAPTION_REFERENCES_ZH.md').write_text('\n'.join(out),encoding='utf-8')

axis='''# EXPO 横轴来源、两版候选与修改记录

日期：2026-10-23。修改起点为当前 `final/head/UACA_head_simple.drawio` 的 A 版（2026-10-22）。

## 数据回忆

- 任务是 `turn_switch`，对照为历史 Old Clean 与旧 Editor-U τ2。
- 实际绘图源是 `assets/candidates_20261017/curves/experiments.json` 的 EXPO 项，来自 10 月 17 日实验窗口 `review1017r1132/curves.csv` 的 `expo-train` 两个序列。
- Old Clean 共 304 个回合结果，累计动作从 59 到 43,802；U τ2 共 340 个回合结果，累计动作从 185 到 47,810。
- 每个原始 y 为该训练回合是否成功（0 或 100）；MA50 对连续 50 个回合求均值，横坐标放在窗口末回合结束时的累计动作数。先平滑，再按当前范围截取。
- 当前显示到 35,000 个动作，纵轴沿用 15–85。完整 MA50 首点分别为 7,795 和 7,493 个动作。
- 当前蓝色峰值 70% 位于 29,421 个动作，红色峰值 76% 位于 16,875 个动作，差值 6 个百分点。

## 为什么与后两张不同

EXPO 横轴的计量对象是累计执行的训练动作，即环境交互步数；GRPO 和 RL Token 使用训练轮次。`Actions (k)` 还把千这个单位放在标题中，所以字面形式也不同。

历史 EXPO 实现区分真实动作、执行 chunk、环境回合和 learner call：回合长度可变，采样后还会按累计动作触发学习调用，每次调用内部包含多次优化。要切换成训练回合或学习调用轴，应从对应的事件日志逐点对齐 `episode`、`physical_actions`、`completed_calls` 等字段，再重新计算点位与峰值横坐标。现有绘图 CSV 只保留 x 与原始成功值，因此本轮采用已记录的环境步数，统一其展示样式。

历史计数机制参照 `C:/Users/86136/Documents/rl/docs/methods/expo-ft/AUDIT_20261003.md`；当前两条曲线数值仍以本轮上述绘图源为准。后续如需轮次轴，可直接利用对应 run 的 episode 与 learner 事件做映射。

## 本轮候选

| 版本 | 横轴标题 | 刻度 | 修改对象数 |
|---|---|---|---:|
| 原版 | Actions (k) | 10、20、30、35 | 0 |
| A · 推荐 | Environment Steps | 10k、20k、30k、35k | 5 |
| B | Environment Steps (k) | 10、20、30、35 | 1 |

两版共用原始曲线路径。MA50、数据范围、纵轴、星标、水平虚线、峰值数字、增益括号、图例、颜色、字体、字号、线宽和布局均沿用当前稿。原生对象比较确认：A 仅 4 个刻度文字及 1 个轴标题变更，B 仅 1 个轴标题变更。

推荐 A：轴名与后两张的排版长度更接近，刻度自身携带千位单位。B 保持原先的短数字刻度，适合追求最小改动。

## 文件与验收

- `EXPO_axis_candidates.drawio`：3 页；第 1 页为原版/A/B 三图对照，第 2、3 页为放回当前头图的 A/B。
- 预览在 `previews/caption_axis_20261023/`：`comparison.png`、`head_A.png`、`head_B.png`；矢量 PDF 只导出 A/B 完整主图。
- 同目录网页 `index.html` 汇集图注、来源和各版预览。
- 独立修改记录 `logs/caption_axis_20261023/object_changes.json`、`expo_source_summary.json`、`render_result.json`。
- 实际渲染检查涵盖原生对象、嵌入图片、整图、EXPO 局部及论文尺寸；PDF 保留约 1–2 px 白边。

## 范围

本轮新增候选和参考整理；现有 `final` 修改 0、删除 0。Overleaf 新增 0、修改 0、删除 0。图注尚处于中文候选阶段。

Git 备份内容为本轮原创中文整理、可编辑候选、预览、主图矢量 PDF 和必要修改记录。论文原始 PDF、网页缓存、逐字图注抽取保存在本地参考区。
'''
(O/'02_EXPO_AXIS_AND_CHANGES.md').write_text(axis,encoding='utf-8')

H=lambda x:html.escape(x,quote=True)
parts=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UACA · 图注与 EXPO 横轴候选</title><style>body{font:16px/1.75 system-ui,"Microsoft YaHei",sans-serif;color:#24313d;max-width:1320px;margin:auto;padding:30px;background:#f6f7f8}h1{font-size:26px}h2{font-size:21px;margin-top:36px}h3{font-size:17px}section,article,figure{background:white;border:1px solid #dde2e6;border-radius:8px;padding:22px;margin:16px 0}img{width:100%;height:auto}a{color:#176ba8}p{margin:9px 0}.note{color:#667580;font-size:14px}nav{display:flex;gap:20px}summary{cursor:pointer;font-weight:600}figcaption{font-size:14px;color:#52616d}.cap{background:#f3f7fb;padding:16px;border-left:3px solid #6ca1c8}code{font-size:14px}</style><h1>UACA 头图：中文图注与 EXPO 横轴候选</h1><nav><a href="#axes">横轴三图对照</a><a href="#captions">我们的图注候选</a><a href="#references">分组参考</a></nav><p class="note">2026-10-23 · 当前终版保留 · Overleaf 新增 / 修改 / 删除：0 / 0 / 0</p>']
parts+=['<section id="axes"><h2>EXPO：保持数据，仅调整横轴文字</h2><p>原始 x 是累计执行动作数；MA50 是 50 个训练回合的成功率平均。A 用 Environment Steps 与 10k 等刻度，B 将 (k) 放在标题中。</p><p><a href="../../candidates/caption_axis_20261023/EXPO_axis_candidates.drawio">可编辑 Draw.io · 3 页</a> · <a href="../../candidates/caption_axis_20261023/02_EXPO_AXIS_AND_CHANGES.md">数据来源与修改对照</a></p><figure><img src="comparison.png"><figcaption>原版 / A / B。点击图片可在浏览器中放大。</figcaption></figure>']
for key in ['A','B']:parts += [f'<details><summary>{key} · 放回头图查看</summary><figure><a href="head_{key}.png"><img src="head_{key}.png"></a><figcaption><a href="head_{key}.pdf">主图矢量 PDF</a></figcaption></figure></details>']
parts+=['</section><section id="captions"><h2>UACA 中文图注候选</h2><p>推荐 A；追求更短可选 B。完整参考与写作判断见 <a href="../../candidates/caption_axis_20261023/01_CAPTION_REFERENCES_ZH.md">中文整理</a>。</p>']
for title,cap in caps:parts += [f'<h3>{H(title)}</h3><p class="cap">{H(cap)}</p>']
parts += ['</section><section id="references"><h2>分组参考 · 17 篇首图图注</h2><p class="note">相关论文为中文转述。借鉴点是本轮针对 UACA 的判断。</p>']
group=''
for g,key,name,para,borrow in rows:
 if g!=group:parts += ['<h2>'+H(g)+'</h2>'];group=g
 s=source[key]
 link=f'<a href="{H(s["url"])}">首图来源</a> · <a href="{H(s["pdf"])}">PDF</a>' if key!='dvca_own' else '用户本地 DVCA 正文 · 图 1'
 parts += [f'<article><h3>{H(name)} · 图 1</h3><p>{H(para)}</p><p class="note">借鉴：{H(borrow)}</p><p>{link}</p></article>']
parts += ['<article><h3>UA-OPD · 图注待补</h3><p>已核对作者主页和论文题名；OpenReview PDF 当前返回验证页面。</p><a href="https://openreview.net/forum?id=hHUZi8oHfo">论文</a> · <a href="https://rhx11111.github.io/">作者主页</a></article></section></html>']
(P/'index.html').write_text('\n'.join(parts),encoding='utf-8')
(O/'caption_paraphrases.json').write_text(json.dumps([dict(group=g,id=k,name=n,figure='Figure 1',chinese_paraphrase=p,application_note=b,source=source[k].get('url','user-owned DVCA manuscript')) for g,k,n,p,b in rows],ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(__file__,R/'scripts/uaca_caption_axis_notes_20261023.py')
print('Wrote Chinese reference catalog, four caption proposals, axis provenance and review HTML.')
