> 状态：本页 A/B 横轴方案已弃用。当前修正版见 ../expo_axis_match_20261023/README.md。

# EXPO 横轴来源、两版候选与修改记录

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
