# Phase 2 First Round Interpretation

## 运行范围

- 请求数据集：Cora、Citeseer、PubMed、Chameleon、Squirrel、Actor。
- 完成数据集：Actor、Chameleon、Citeseer、PubMed、Squirrel。
- 失败 / 跳过数据集：Cora。
- Cora 失败原因：PyG 在下载 / 加载时无法连接 `github.com:443`，具体堆栈已记录在 `run_log.md`。
- 标签使用边界：标签只用于 post-hoc diagnostic analysis，没有用于训练、增强选择或 pair weighting。
- hard negative 诊断边界：本轮没有训练 GCL encoder；hard negative 使用 raw node features 作为 proxy embeddings，因此只能作为第一轮 failure signal。

## 1. Gap 2 是否有初步证据支持？

**结论：部分支持，但还不足以直接进入方法设计。**

支持 Gap 2 的证据主要来自 negative side：在 5/5 个成功数据集上，hard negative false negative rate 都高于 random batch negative false negative rate，说明“hard negative 越难越有价值”这一假设在 raw-feature proxy 空间中确实存在明显风险。

暂时不足的地方在 positive-negative 共现：低同配节点的 joint reliability risk 只在 Chameleon 上高于高同配节点，其他 4 个成功数据集并不支持“低同配区域更容易同时出现 positive failure 与 negative collision”的强结论。因此，本轮结果更像是给出了 Gap 2 的初步风险信号，而不是足以支撑新方法设计的完整证据链。

## 2. 哪些数据集 positive view failure 最明显？

positive view failure proxy 使用 JS neighborhood-label drift、absolute local homophily change、low-reliability positive ratio 的均值。数值越高，代表 edge_drop 后的 positive view 可靠性风险越高。

| Rank | Dataset | Positive Failure Proxy | Max JS Drift | Max Low-Reliability Positive Ratio |
|---:|---|---:|---:|---:|
| 1 | Actor | 0.0609 | 0.3908 | 0.0000 |
| 2 | Citeseer | 0.0579 | 0.3968 | 0.0000 |
| 3 | PubMed | 0.0528 | 0.3648 | 0.0000 |
| 4 | Chameleon | 0.0355 | 0.2792 | 0.0000 |
| 5 | Squirrel | 0.0342 | 0.2809 | 0.0000 |

**回答：Actor、Citeseer、PubMed 的 positive view failure proxy 最明显。**

需要注意：本轮 `low_reliability_positive_ratio` 全部为 0，说明 raw-feature proxy 下同节点跨视图相似度没有低于同类平均相似度；positive-side 信号主要来自邻域标签分布漂移和 local homophily change，而不是 embedding positive collapse。

## 3. Hard negative false negative rate 是否高于 random batch negative？

| Dataset | Random Batch FNR | Hard Negative FNR | Hard - Random |
|---|---:|---:|---:|
| Citeseer | 0.1781 | 0.5274 | 0.3493 |
| PubMed | 0.3570 | 0.6671 | 0.3102 |
| Chameleon | 0.2015 | 0.2700 | 0.0684 |
| Squirrel | 0.2002 | 0.2281 | 0.0279 |
| Actor | 0.2130 | 0.2368 | 0.0238 |

**回答：是。hard negative false negative rate 在 5/5 个成功数据集上都高于 random batch negative。**

这个结果支持继续检查 negative pair noise，尤其是 scalable mini-batch / hard-negative mining 场景。不过由于 hard negatives 由 raw features proxy 得到，还不能直接等价为训练后 GCL embedding 空间里的 hard negative failure。

## 4. 是否存在 positive failure 与 negative collision 共现？

joint reliability risk 使用 aggregate 脚本中的第一版归一化加和：

`joint_reliability_risk_score = normalized_positive_failure_score + normalized_negative_collision_score`

| Dataset | Low-Homophily Joint Risk | High-Homophily Joint Risk | Low - High | Low Positive Failure | High Positive Failure |
|---|---:|---:|---:|---:|---:|
| Chameleon | 0.6800 | 0.6285 | 0.0515 | 0.0314 | 0.0386 |
| Actor | 0.8185 | 0.8815 | -0.0631 | 0.0566 | 0.0640 |
| PubMed | 1.2055 | 1.3265 | -0.1211 | 0.0606 | 0.0460 |
| Squirrel | 0.5860 | 0.7508 | -0.1647 | 0.0259 | 0.0434 |
| Citeseer | 0.8566 | 1.0805 | -0.2239 | 0.0609 | 0.0480 |

**回答：存在局部共现信号，但不稳定。**

Chameleon 上低同配节点的 joint risk 高于高同配节点，符合 Gap 2 对异配 / 低同配区域的预期；但 Actor、PubMed、Squirrel、Citeseer 均不是这个模式。因此本轮不能声称“低同配节点普遍更容易出现 positive failure 与 negative collision 共现”。

## 5. 下一步应该继续 Gap 2、转向 Gap 1，还是转向 scalable mini-batch negative noise？

**建议：短期不要直接进入 Gap 2 方法设计；优先转向 scalable mini-batch negative noise 做补充验证，同时保留 Gap 2 作为中期主线。**

理由：

- negative-side 证据强：5/5 个成功数据集上 hard negative FNR 均高于 random batch FNR。
- positive-side 证据中等：positive failure proxy 在 Actor / Citeseer / PubMed 更明显，但 raw-feature positive reliability 没有显示 low-reliability positive ratio。
- joint 共现证据弱：只有 Chameleon 显示低同配节点 joint risk 高于高同配节点。

如果下一轮使用训练后 GRACE / GCA embeddings 后仍观察到：

1. hard negative FNR 明显高于 random batch FNR；
2. edge_drop 强度越高 positive reliability 越低；
3. 低同配 / 异配节点上 positive failure 与 negative collision 共现；

则继续推进 Gap 2。否则：

- 若主要仍是 negative collision 信号，转向 scalable mini-batch negative noise。
- 若训练后 embeddings 显示 positive view failure 更强但 negative collision 不稳定，转向 Gap 1 的 view / positive reliability calibration。

## 6. 下一轮最低必要检查

1. 补齐 Cora：等待 GitHub / PyG 下载可用，或提供 cached/custom `.npz` 输入。
2. 用训练后 GRACE / GCA embeddings 替代 raw-feature proxy，重新计算 hard negative FNR 与 positive pair reliability。
3. 保持标签只做 post-hoc diagnostic analysis，不进入训练、增强选择或 pair weighting。
