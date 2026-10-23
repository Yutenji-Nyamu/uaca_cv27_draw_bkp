# N75 头图与当前四噪声附录 · 2026-10-23

## 当前成果

- N75 turn_switch 作为头图信号，动作9/30/50三帧；头图显示0–65动作。四个红点位于26/28/30/32；连续折线保留全部逐动作值，圆点每2动作一个，与灰白条纹对齐。
- N20 lift_pot重复轨迹从当前集合移除。N75独立作为头图，其余14条为完整轨迹附录。
- 所有照片左上角A/B/C删除；曲线上方A/B/C与竖虚线保留。附录保持无逐点圆圈、无照片到曲线的折线连接。
- 所有三帧说明逐条对照同回合前后帧。N53手机：A手机在桌面、手臂撤回；B左手靠近手机；C抓住并抬起手机。N71标注换手。
- 两份头图与独立组件同步更新。15页信号集合的第1页为头图信号，其余14页为附录。

## 信号和素材

信号字段为 noise4：同一观测和策略下4份初始噪声、每份10 NFEs，执行第一份动作。头图来源示意同步为A_1至A_4、K=4、各10 NFEs。所有信号曲线采用逐动作原始值。

15条轨迹备份均包含完整H264视频、series.json、frame_map.json与3张选定帧。录像25 fps；动作对应按逐臂单调几何投影映射，映射精度和误差保留在选帧清单。采样点沿用上轮已选动作，本轮修正说明文字。

- 本地当前集合：[final/signals/index.html](final/signals/index.html)
- 图稿当前目录：[final](final/README.md)
- 数据与录像：[assets/noise4_current_20261023](assets/noise4_current_20261023)
- 原始75条录像来源：https://github.com/Yutenji-Nyamu/tts_consistency_fig

## EXPO / GRPO 从零开始

原始数据：assets/candidates_20261017/curves/experiments.json。
用户指定规则：m_t = mean(y[max(1,t-49):t])，包含当前记录；第1–49条使用已有记录，第50条及以后使用最近50条。第50条起数值与原MA50逐点一致。

| 图 | 改前 | 改后 |
|---|---|---|
| EXPO | 丢掉前49条；左端在约50轮 | 补回第1条起的部分窗口均值；轴从0开始；截至35000原始动作，Clean244条、U257条 |
| EXPO横轴 | 已确认的近似训练轮次50–250 | 延续近似轮次格式，0–250；0–35000动作线性映射到0–250显示步（140动作/显示步） |
| EXPO纵轴与标注 | 15–85%；完整MA50峰值70/76 | 15–105%容纳开头少量记录的100%；70/76完整窗口峰值用MA50 peaks短标签说明，增益+6.00 |
| GRPO | 从第50轮开始、显示到168轮 | 从第1条均值画起、横轴0–168；常规刻度0/50/100/150；完整窗口峰值66.48/72.02与+5.54保留 |
| RLT | 学生阶段MA20，横轴146–400 | 原生对象全部保留 |

曲线形状随补回开头和显示范围延展；图例、字体、线色、线宽、方法名和星标样式沿用原稿。EXPO不是把每轮固定为140真实动作；这里延续已确认的近似显示坐标，两条轨迹实际回合数分别为244/257。

## 三帧文字改前 / 改后

| 图 | 帧 / 动作 | 改前 | 改后 |
|---|---|---|---|
| N12 | A / 3 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N12 | B / 16 | Roller approach；How to align? | Roller approach；Where to grasp? |
| N12 | C / 35 | At roller ends；Grasps aligned | Roller alignment；Ends within reach |
| N17 | A / 150 | Left hand at mug；Mug position fixed | Mug placement；Mug on table |
| N17 | B / 180 | Switching hands；Which grasp next? | Switching hands；How to regrasp? |
| N17 | C / 202 | Right-hand reach；Fingers aligned | Right-hand grasp；Grasp established |
| N19 | A / 10 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N19 | B / 22 | Handle approach；How to align? | Handle approach；How to align? |
| N19 | C / 48 | Hands at handles；Two-hand alignment | At pot handles；Grippers aligned |
| N31 | A / 10 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N31 | B / 22 | Bottle approach；How to align? | Bottle approach；How to align? |
| N31 | C / 52 | Hands at bottles；Grasps aligned | At the bottles；Ready to grasp |
| N35 | A / 5 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N35 | B / 26 | Object approach；Which grasp pose? | Object approach；Which grasp pose? |
| N35 | C / 52 | Grasp alignment；Fingers centered | Above the object；Gripper aligned |
| N39 | A / 5 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N39 | B / 16 | Food approach；How to align? | Food approach；How to grasp both? |
| N39 | C / 48 | Hands at food；Grasps aligned | At the food；Grippers aligned |
| N43 | A / 5 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N43 | B / 16 | Can approach；How to align? | Can approach；How to align? |
| N43 | C / 48 | Hands at cans；Grasps aligned | At the cans；Grippers aligned |
| N45 | A / 156 | Gripper retraction；Free-space motion | Left-hand retreat；Free-space motion |
| N45 | B / 197 | Shoe above box；How to orient? | Shoe positioning；How to orient? |
| N45 | C / 265 | Shoe in box；Placement aligned | Lowering shoe；Shoe aligned |
| N49 | A / 163 | Carry object；Object held | Carry object；Object held |
| N49 | B / 189 | Release in basket；When to release? | Object release；When to release? |
| N49 | C / 202 | Retract gripper；Object placed | Gripper retreat；Object in basket |
| N52 | A / 3 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N52 | B / 15 | Object approach；Which grasp pose? | Reach initiation；Where to grasp? |
| N52 | C / 52 | Grasp object；Fingers aligned | Object approach；Gripper aligned |
| N53 | A / 154 | Phone held；Stable grasp | Hand retreat；Phone on table |
| N53 | B / 178 | Change grasp；How to orient? | Phone approach；Where to grasp? |
| N53 | C / 235 | Phone tilted；Pose aligned | Lift phone；Grasp established |
| N56 | A / 8 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N56 | B / 40 | Stapler approach；Where to press? | Stapler approach；Where to press? |
| N56 | C / 70 | Above stapler；Ready to press | Above stapler；Ready to press |
| N63 | A / 6 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N63 | B / 15 | Bottle approach；Which grasp pose? | Bottle approach；Where to grasp? |
| N63 | C / 35 | At bottle neck；Fingers aligned | Above bottle；Gripper aligned |
| N71 | A / 177 | Bowl released；Bowl on table | Bowl released；Bowl on table |
| N71 | B / 187 | Switching hands；Which hand next? | Switching hands；Which hand next? |
| N71 | C / 197 | Right-hand reach；Target bowl fixed | Right-hand reach；Next bowl targeted |
| N75 | A / 9 | Initial arm lift；Free-space motion | Initial reach；Free-space motion |
| N75 | B / 30 | Switch approach；How to align? | Switch approach；How to align? |
| N75 | C / 50 | Over switch；Ready to press | At the switch；Ready to press |

## 检查与历史

- 15条选定轨迹的45张场景帧均已核对前后动作；新的标注经局部与整页渲染查看。
- 共20个独立页面/组件完成原生渲染，缺失对象0，图片加载错误0。
- 两份头图PDF均为单页矢量：保留路径、文字和内嵌照片，约1.5 CSS px白边。已查看PDF实际渲染。
- 前一版正式图稿完整保存于 logs/noise4_current_20261023/before/。旧16页候选为历史材料，当前入口统一指向15页集合。
- 逐项记录：logs/noise4_current_20261023/annotation_audit.json、curve_qa.json、signal_qa.json、render_result.json。

动作阶段辅助核对的任务源代码：
- https://raw.githubusercontent.com/RoboTwin-Platform/RoboTwin/main/envs/place_phone_stand.py
- https://raw.githubusercontent.com/RoboTwin-Platform/RoboTwin/main/envs/hanging_mug.py
- https://raw.githubusercontent.com/RoboTwin-Platform/RoboTwin/main/envs/place_dual_shoes.py

## Overleaf 全部变更

本轮新增 **0**、修改 **0**、删除 **0**。云端保留上一轮已确认的EXPO横轴版本；本轮交付更新本地与Git当前稿。
