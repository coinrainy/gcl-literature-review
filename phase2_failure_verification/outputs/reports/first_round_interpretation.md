# Phase 2 第一轮 Failure Verification 解释报告

## 1. 哪些数据集 positive view failure 最明显？

按 `all` 节点组的 `neighbor_label_distribution_js_divergence` 衡量，positive view failure 最明显的是 Actor、Citeseer、PubMed 和 Cora。rate = 0.8 时，Actor = 0.3708，Citeseer = 0.3314，PubMed = 0.3105，Cora = 0.2942；Chameleon = 0.2391，Squirrel = 0.2089。

这说明 edge_drop 对同配数据集并不总是更安全：Cora/Citeseer/PubMed 在强扰动下也出现明显的邻域语义漂移。异配数据集 Chameleon/Squirrel 的全局同配率很低，但由于图更稠密，随机删边下的分布扰动在当前指标里没有排到最前。

## 2. hard negatives 的 false negative rate 是否高于 random batch negatives？

是。六个数据集上 hard negative false negative rate 均高于 random batch negative。

| Dataset | Random Batch FNR | Hard Negative FNR | Ratio |
|---|---:|---:|---:|
| Citeseer | 0.1781 | 0.5274 | 2.96 |
| Cora | 0.1780 | 0.5235 | 2.94 |
| PubMed | 0.3570 | 0.6671 | 1.87 |
| Chameleon | 0.2015 | 0.2700 | 1.34 |
| Squirrel | 0.2002 | 0.2281 | 1.14 |
| Actor | 0.2130 | 0.2368 | 1.11 |

同配 Planetoid 数据集上的 hard-negative 碰撞尤其明显，说明“看起来更难的负样本”很容易包含同类节点；这为 Gap 2 的 negative-side reliability 问题提供了直接初步证据。

## 3. 低同配节点是否比高同配节点更容易出现 joint reliability risk？

当前结果不支持这个强表述。按 joint risk 均值看，低同配组并不稳定高于高同配组：

| Dataset | Low | Medium | High | All |
|---|---:|---:|---:|---:|
| Cora | 0.8665 | 0.9721 | 0.9615 | 0.9526 |
| Citeseer | 0.8566 | 1.1005 | 1.0805 | 1.0279 |
| PubMed | 1.2055 | 1.2385 | 1.3265 | 1.3018 |
| Chameleon | 0.6800 | 0.6893 | 0.6285 | 0.6750 |
| Squirrel | 0.5860 | 0.6561 | 0.7508 | 0.6021 |
| Actor | 0.8185 | 0.8848 | 0.8815 | 0.8347 |

更谨慎的解释是：positive failure 与 negative collision 的共现不是简单由“低同配节点”决定，而是受数据集稠密度、类别分布、局部邻域结构和 hard-negative mining proxy 共同影响。

## 4. 当前结果是否支持继续推进 Gap 2？

支持继续推进 Gap 2 的 failure verification，但暂时不支持直接进入完整新方法实现。

支持点有两个：第一，positive view 在强 edge_drop 下出现可重复的语义扰动；第二，hard negative false negative rate 系统性高于 random batch negative，且 Cora/Citeseer/PubMed 的差距很大。二者合在一起说明“正样本视图可靠性”和“负样本碰撞噪声”都是真实可测的问题。

限制也很明确：joint risk 最高的组并不总是低同配节点，Chameleon/Squirrel 的 positive failure 排名也不如预期高。因此主张应从“heterophily-only failure”收窄为“positive-negative pair reliability failure”，并继续做第二轮诊断验证。

## 5. 如果不支持，应该转向 Gap 1、Gap 6，还是降低论文目标？

当前不是完全不支持，所以不建议立刻转向 Gap 1，也不建议直接降低论文目标。更合理的下一步是继续 Gap 2，但把方法设计前的证据门槛写清楚：

- 若第二轮仍显示 hard-negative collision 稳定强于 positive-side failure，应转向 Gap 6，也就是 scalable mini-batch negative noise 方向。
- 若第二轮只保留 positive-side failure，尤其集中在异配或低同配局部结构上，应转向 Gap 1 的 heterophily view / positive reliability 版本。
- 若第二轮不能复现 positive failure 与 negative collision 的稳定共现，再降低论文目标，改成诊断型或短论文目标。

本轮结论：继续 Gap 2，但先补第二轮 failure verification，不进入训练新方法。
