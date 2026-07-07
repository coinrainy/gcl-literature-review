# Failure Verification Summary

## 当前状态

- 覆盖数据集：Actor, Chameleon, Citeseer, PubMed, Squirrel
- graph statistics 行数：5
- positive view failure 行数：500
- negative pair noise 行数：240
- joint reliability risk 行数：100
- 缺失输入：无

## 解释边界

- 标签只用于后验 diagnostic analysis，不用于无监督训练、增强选择或目标优化。
- raw feature / PCA / simple encoder 得到的 hard-negative 结果只能视为 proxy。
- joint_reliability_risk_score 是第一版归一化加和，用于排序风险区域，不是论文主结论。

## 初步判断规则

- 若低同配或异配数据集同时出现更高 positive failure score 与 negative collision score，则 Gap 2 值得继续。
- 若只出现 positive failure，应回到 Gap 1 的 view / positive reliability calibration。
- 若只出现 batch/hard-negative collision，应转向 scalable mini-batch negative noise。
- 若二者均不明显，不建议直接进入顶会方法主线。

## Joint Risk Top Rows

| Dataset | Augmentation | Rate | Group | Joint Risk |
|---|---|---:|---|---:|
| PubMed | edge_drop | 0.8 | high_homophily | 1.7111387139251573 |
| PubMed | edge_drop | 0.8 | all | 1.695446160699529 |
| PubMed | edge_drop | 0.8 | medium_homophily | 1.6636173978865059 |
| PubMed | edge_drop | 0.8 | low_homophily | 1.6351282995207628 |
| Citeseer | edge_drop | 0.8 | medium_homophily | 1.5991052297921025 |
| Citeseer | edge_drop | 0.8 | high_homophily | 1.4990820091123978 |
| PubMed | edge_drop | 0.6 | high_homophily | 1.4571906345105294 |
| Citeseer | edge_drop | 0.8 | all | 1.4567622363255048 |
| PubMed | edge_drop | 0.6 | all | 1.4423130830838944 |
| PubMed | edge_drop | 0.6 | medium_homophily | 1.3987658698123169 |
