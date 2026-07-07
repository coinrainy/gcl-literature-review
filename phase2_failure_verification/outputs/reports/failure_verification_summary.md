# Phase 2 第一轮 Failure Verification 汇总

## 当前状态

- 覆盖数据集：Cora, Citeseer, PubMed, Chameleon, Squirrel, Actor。
- 运行脚本：`compute_graph_statistics.py`、`simulate_positive_view_failure.py`、`diagnose_negative_pair_noise.py`、`aggregate_failure_results.py`。
- positive view 设置：`augmentation=edge_drop`，rates = 0.1, 0.2, 0.4, 0.6, 0.8，`num-trials=5`。
- negative pair 设置：batch sizes = 128, 256, 512, 1024，top-k = 5, 10, 20, 50，`num-batches=50`。
- 输出行数：graph statistics 6 行，positive view failure 600 行，negative pair noise 288 行，joint reliability risk 120 行。
- 数据集加载失败：无。Cora 已通过本地 Planetoid raw cache 和 PyG processed cache 正常加载。

## 解释边界

- 标签只用于 post-hoc diagnostic analysis；本轮没有训练新方法，没有用标签做增强选择、训练目标或 pair weighting。
- hard-negative 诊断基于当前脚本中的 feature/proxy 相似性，适合作为 failure verification 证据，不应直接写成新方法效果。
- `joint_reliability_risk_score` 是第一版归一化风险排序指标，用于定位正视图扰动和负样本碰撞是否共现，不是最终论文主结论。

## 图统计摘要

| Dataset | Nodes | Edges | Features | Classes | Global Edge Homophily |
|---|---:|---:|---:|---:|---:|
| Cora | 2708 | 5278 | 1433 | 7 | 0.8100 |
| Citeseer | 3327 | 4552 | 3703 | 6 | 0.7355 |
| PubMed | 19717 | 44324 | 500 | 3 | 0.8024 |
| Chameleon | 2277 | 31371 | 2325 | 5 | 0.2299 |
| Squirrel | 5201 | 198353 | 2089 | 5 | 0.2221 |
| Actor | 7600 | 26659 | 932 | 5 | 0.2167 |

## Positive View Failure 摘要

按 `all` 节点组的平均 JS divergence 看，edge drop 越强，邻域标签分布扰动越明显。rate = 0.8 时排序为：

| Dataset | JS Divergence at rate 0.8 |
|---|---:|
| Actor | 0.3708 |
| Citeseer | 0.3314 |
| PubMed | 0.3105 |
| Cora | 0.2942 |
| Chameleon | 0.2391 |
| Squirrel | 0.2089 |

低同配组的 positive-side 扰动在 Cora、Citeseer、PubMed 中更明显，但在 Squirrel 上并不成立；Actor 和 Chameleon 的 medium/high 组更高。

## Negative Pair Noise 摘要

hard negatives 的 false negative rate 在全部六个数据集上都高于 random batch negatives。

| Dataset | Random Batch FNR | Hard Negative FNR | Ratio |
|---|---:|---:|---:|
| Citeseer | 0.1781 | 0.5274 | 2.96 |
| Cora | 0.1780 | 0.5235 | 2.94 |
| PubMed | 0.3570 | 0.6671 | 1.87 |
| Chameleon | 0.2015 | 0.2700 | 1.34 |
| Squirrel | 0.2002 | 0.2281 | 1.14 |
| Actor | 0.2130 | 0.2368 | 1.11 |

## Joint Risk Top Rows

| Dataset | Augmentation | Rate | Group | Joint Risk |
|---|---|---:|---|---:|
| PubMed | edge_drop | 0.8 | high_homophily | 1.7111 |
| PubMed | edge_drop | 0.8 | all | 1.6954 |
| PubMed | edge_drop | 0.8 | medium_homophily | 1.6636 |
| PubMed | edge_drop | 0.8 | low_homophily | 1.6351 |
| Citeseer | edge_drop | 0.8 | medium_homophily | 1.5991 |
| Citeseer | edge_drop | 0.8 | high_homophily | 1.4991 |
| Cora | edge_drop | 0.8 | medium_homophily | 1.4614 |
| Citeseer | edge_drop | 0.8 | all | 1.4568 |
| PubMed | edge_drop | 0.6 | high_homophily | 1.4572 |
| PubMed | edge_drop | 0.6 | all | 1.4423 |

## 初步判断

第一轮结果支持继续推进 Gap 2 的 failure verification：positive view 在强 edge drop 下出现稳定扰动，hard negatives 的 false negative rate 又系统性高于 random batch negatives，说明 positive-side 与 negative-side reliability 问题可以被同一诊断框架捕捉。

但结果不支持把主张写成“低同配节点必然更容易出现 joint reliability risk”。当前 joint risk 更常出现在 medium/high homophily 组或全体节点组，下一轮应把论点收窄为“正视图失败与负样本碰撞会在部分数据集和局部节点组共现”，再决定是否进入方法设计。
