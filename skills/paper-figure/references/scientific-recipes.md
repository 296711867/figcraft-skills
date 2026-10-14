# 20 类科研图：输入与科学含义

JSON 最外层：`type`, `data`, 可选 `title/xlabel/ylabel`，真实数据必须有 `provenance.source`。合成示例必须保留 `synthetic: true`。列表中的模板数据仅用于演示；替换为真实数据后设置 `synthetic: false` 并补来源。

所有值必须有限；本渲染器不自动删除缺失行。自行按预先声明的规则处理并在 provenance 记录。所有额外未知字段不会自动变成标注或计算，请改脚本或明确扩展。

## histogram · 直方图

Distribution of continuous observations

输入：`values; optional bins`。

完整可运行 JSON：[示例](../examples/specs/histogram.json)。

## box · 箱线图

Compare medians, spread and outliers

输入：`groups=[{label, values}]`。

完整可运行 JSON：[示例](../examples/specs/box.json)。

## violin · 小提琴图

Compare distribution shapes

输入：`groups=[{label, values}]`。

完整可运行 JSON：[示例](../examples/specs/violin.json)。

## ecdf · 经验累积分布图

Compare cumulative probabilities without binning

输入：`groups=[{label, values}]`。

完整可运行 JSON：[示例](../examples/specs/ecdf.json)。

## errorbar · 误差棒图

Supplied estimates with declared uncertainty

输入：`x, y, lower, upper, interval_label`。

完整可运行 JSON：[示例](../examples/specs/errorbar.json)。

## confidence-band · 置信带图

Supplied curve and pointwise uncertainty bounds

输入：`x, y, lower, upper, interval_label`。

完整可运行 JSON：[示例](../examples/specs/confidence-band.json)。

## regression · 回归散点与拟合线

Raw paired observations with an ordinary least squares line

输入：`x, y`。

完整可运行 JSON：[示例](../examples/specs/regression.json)。

## residual · 残差诊断图

Inspect supplied fitted values and residuals

输入：`fitted, residuals`。

完整可运行 JSON：[示例](../examples/specs/residual.json)。

## qq · 正态 Q–Q 图

Inspect departure from normality using sample quantiles

输入：`values`。

完整可运行 JSON：[示例](../examples/specs/qq.json)。

## bland-altman · Bland–Altman 一致性图

Compare two measurements on the same subjects

输入：`a, b; sample size >= 2`。

完整可运行 JSON：[示例](../examples/specs/bland-altman.json)。

## forest · 森林图

Compare supplied study effects and uncertainty

输入：`labels, effect, lower, upper, interval_label; optional null, xscale`。

完整可运行 JSON：[示例](../examples/specs/forest.json)。

## roc · ROC 曲线

Binary prediction: false positive rate versus sensitivity

输入：`y_true (0/1), score (higher=positive)`。

完整可运行 JSON：[示例](../examples/specs/roc.json)。

## precision-recall · 精确率–召回率曲线

Binary prediction with positive prevalence baseline

输入：`y_true (0/1), score (higher=positive)`。

完整可运行 JSON：[示例](../examples/specs/precision-recall.json)。

## calibration · 概率校准图

Compare predicted probability with observed frequency

输入：`y_true (0/1), probability (0..1); optional bins`。

完整可运行 JSON：[示例](../examples/specs/calibration.json)。

## confusion · 混淆矩阵

Show supplied counts with explicit class orientation

输入：`matrix (nonnegative integers), labels; optional normalize`。

完整可运行 JSON：[示例](../examples/specs/confusion.json)。

## correlation · 相关矩阵

Pearson correlation from raw rows and variable columns

输入：`matrix (rows=observations), labels (columns)`。

完整可运行 JSON：[示例](../examples/specs/correlation.json)。

## contour · 等高线图

Scalar field on a two-dimensional grid

输入：`x, y, z (shape len(y) by len(x))`。

完整可运行 JSON：[示例](../examples/specs/contour.json)。

## surface · 三维曲面图

Supplied scalar field with essential third-dimensional structure

输入：`x, y, z; optional zlabel`。

完整可运行 JSON：[示例](../examples/specs/surface.json)。

## spectrogram · 时频谱图

Frequency evolution of a uniformly sampled signal

输入：`signal, sample_rate; optional nfft, overlap`。

完整可运行 JSON：[示例](../examples/specs/spectrogram.json)。

## multi-panel · 多面板组合图

Compare related panels with consistent fonts and panel labels

输入：`panels=[{type, data, title?, xlabel?, ylabel?}]; optional columns`。

完整可运行 JSON：[示例](../examples/specs/multi-panel.json)。

## 计算约定与适用边界

- ROC：分数越大越偏向正类，同分阈值一起处理，AUC 用梯形积分；必须有两类。不同模型比较应来自同一验证集，不能拿本合成例子作性能证明。
- PR：AP 为 `sum(delta recall * precision at threshold)`，与用梯形积分算 PR-AUC 不是同一指标。图中横虚线为实际正类比例。
- 校准：概率区间 [0,1]，等宽分箱，空箱不连作零值；演示不生成置信区间或样本量标签，研究使用时可按需要增加 bin count 与区间。
- Bland–Altman：横轴 (A+B)/2，纵轴 A-B，样本 SD (`ddof=1`)，一致性限为均值 ±1.96 SD。这是约定的描述图，解释需考虑差值分布、异方差、样本量与重复测量；不输出自动“可互换”结论。
- Q–Q：正态理论分位 `(i+0.5)/n`；参考线通过第一与第三四分位，不是显著性检验。
- 回归：普通最小二乘直线，不生成 CI、p 值或因果判断；残差图使用用户提供的 fitted/residuals，不暗中重拟合别的模型。
- 森林图：用户给定效应与区间，无自动合并效应。比值指标一般设 `null: 1, xscale: "log"` 且区间全为正；差值指标一般 `null: 0`。
- 相关图：观测行为样本，列为变量，Pearson r；不提供 p 值；常量列拒绝。单变量可得到 1×1 矩阵，但没有比较意义。
- 箱线图：Matplotlib 默认四分位与 1.5 IQR 须，须不是 CI；小提琴图是核密度示意，默认带宽来自 Matplotlib，研究需记录/调整带宽，不用小提琴掩盖小样本。
- 时频图：等间隔采样，Matplotlib 默认 Hann 窗、PSD、dB/Hz，`nfft`/overlap/采样率明确；非等间隔信号不可直接套用。
- 等高线/曲面：仅显示给定网格，不插值填缺值；三维用于确有深度意义的任务，普通精确数值对比优先二维。
- 多面板：`panels` 不嵌套组合图；每个 panel 可为另外 19 类之一，分别给 type/data。宽度默认 180 mm，可改；不同单位不强制共轴。

修改真实图后重新核对方法、数据、单位与所有导出产物。例子都能运行不等于用户数据已经完成科学与视觉验收。
