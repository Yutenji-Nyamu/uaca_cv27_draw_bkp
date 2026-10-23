# 头图批注修订与 Overleaf 更新 · 2026-10-23

## 批注逐项处理

| 批注原意 | 处理结果 |
|---|---|
| 曲线原来标红4点，中间留蓝的点奇怪，改成最高5点 | 在既有每2动作一个圆点的采样格点中，按原始U从高到低选5个；标红动作10、12、14、16、18。实际只将动作12对应的原生圆点改为红色。原始101个曲线点、圆点位置、斑马线、三帧和所有其他图元保持原稿。 |
| EXPO目前整个曲线是左右各25均值，还是前50到当前点均值？ | 当前正式稿：第1–5个记录用中心±5均值；第6–49个记录用已有前缀均值；第50个起用含当前记录的向前50记录均值。 |
| 试试前50个改成左右25平均，单独画这个图 | 独立建立2页EXPO Draw.io：原稿 / 试稿。试稿第1–50个记录用原始记录中心±25的均值（含中心，最多51条；开头截断）；第51个起沿用原稿。只改变两条曲线的前50个纵坐标，横坐标、纵轴15–85%、图例、星标、70/76%和+6均保持。 |

试稿开头震荡减小；切回向前MA50时，UACA第50→51个记录为54.90%→44.00%，Baseline为45.10%→42.00%。该接点来自两种窗口的切换。试稿保存在独立候选中，正式头图训练曲线沿用用户此前确认版本。

## 当前文件

- `final/head/UACA_head_simple.drawio`、PDF、PNG：当前两行头图。
- `final/head/UACA_head_current_layout.drawio`、PDF、PNG：同步标红规则的三行并行终版。
- `final/elements/action_uncertainty.drawio`、PNG，以及`final/signals/UACA_signal_collection.drawio`首个头图页同步。
- `candidates/head_annotations_20261023/expo/EXPO_first50_center25_comparison.drawio`：独立2页EXPO对照。
- `previews/head_annotations_20261023/index.html`：当前头图和EXPO并排对照入口。
- 批注原稿及改前正式文件：`logs/head_annotations_20261023/before/`；批注原文和逐对象检查：同目录`annotation_qa.json`。

## Overleaf 全部变更

项目：https://www.overleaf.com/project/6ad9802e57f0d6e672b0072b

**新增0、修改1、删除0。**

| 修改文件 | 改前（当前云端原图） | 改后 |
|---|---|---|
| `fig/uaca_head_simple_20261022.pdf` | Turn Switch，Step19/28/52，10–65横轴，5/10NFEs；EXPO和GRPO横轴起点仍被截去 | 当前本地N39 Place Burger & Fries，Step5/16/48，0–100横轴，四噪声各10NFEs，最高5个现有圆点标红；EXPO和GRPO补回起始数据、横轴从0开始，沿用已确认纵轴范围和EXPO前5点规则 |

本轮云端仅上传同名PDF。main.tex、teaser.tex、teaser_simple.tex、caption、正文、Bib修改均为0。云端保留的原三行PDF未替换。

## 验收

两份完整头图均为单页矢量PDF，1.5px白边；原生对象与照片全部加载，缺失对象0、失败图片0。已查看完整PDF渲染及独立EXPO试稿。云端重新编译成功，Errors0、Warnings0，静默获取完整论文PDF并核对头图所在第2页。
