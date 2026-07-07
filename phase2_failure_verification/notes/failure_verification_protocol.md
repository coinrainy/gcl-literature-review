# Gap 2 Failure Verification Protocol

## 研究问题

主线暂定为 **Positive-Negative Pair Reliability Calibration for Graph Contrastive Learning**，中文暂定为“图对比学习中的正负样本可靠性校准”。本阶段只验证 failure mode 是否成立，不直接实现完整新方法。

核心问题有三个：

1. positive view 是否真的不可靠：同一节点在两个增强视图中是否仍保持语义一致。
2. negative pair 是否真的有噪声：batch negatives / hard negatives 中是否混入同类或语义近邻。
3. 现有方法是否只局部解决问题：negative-side 方法、heterophily-aware view construction、negative-free 方法是否缺少统一的 pair-level reliability diagnostics。

## 假设

- H1：异配图或低同配节点上，edge dropping / feature masking 更容易破坏邻域语义和正样本视图可靠性。
- H2：hard negatives 中的 false negative rate 高于随机 batch negatives，且 batch size 或 top-k 越大，collision 风险越明显。
- H3：positive failure 与 negative collision 会在部分数据集或节点组上共现，因此单独修正 positive 或 negative 都可能不够。
- H4：标签只能用于后验诊断，不能参与无监督训练、增强选择或 pair weighting。

## 数据集

第一轮优先跑：

- 同配 sanity check：Cora、Citeseer、PubMed、Amazon Computers、Coauthor CS。
- 经典异配图：Chameleon、Squirrel、Actor、Cornell、Texas、Wisconsin。

后续扩展：

- 大规模或更严格异配图：Penn94、genius、twitch-gamers、arXiv-year、snap-patents、pokec。
- Gap 7 备选 graph-text / TAG：ogbn-arxiv with title / abstract、PubMed TAG、WikiCS、Reddit TAG。

## Baseline 对照角色

- GRACE / GCA：默认正视图可靠，batch negatives 大多可靠。
- ProGCL / GDCL / IFL-GCL：更偏 negative side，适合检查 negative correction 是否能解释 positive-side failure。
- ROSEN：更偏 heterophily local positive false positive。
- HLCL / PolyGCL / HeterGCL / M3P-GCL：通过异配友好 view construction 间接缓解 positive view failure。
- HGMS：主要针对 heterogeneous graph / metapath 场景。
- BGRL / CCA-SSG：避免或弱化 negatives，但仍依赖 view reliability。
- GraphMAE / GraphMAE2：非对比式 baseline，用来判断 failure 是否 GCL 特有。

## Diagnostics

- Graph statistics：确认同配程度、度分布、类别分布和基础图属性。
- Positive view failure：扫描 edge dropping / feature masking 强度，统计边类型保留、邻域标签分布漂移、本节点跨视图表示相似度。
- Negative pair noise：统计随机 batch negatives 的同类 collision，以及 hard negatives 的同类 collision。
- Joint reliability risk：把 positive failure score 与 negative collision score 做第一版归一化加和，用于定位共现风险。

## 何时认为 Gap 2 成立

如果观察到以下现象，则 Gap 2 值得继续：

1. 异配图或低同配节点上，positive view failure 明显高于同配图或高同配节点。
2. hard negatives 中 false negative rate 明显高于随机 negatives。
3. 增强强度越高，positive reliability 越低。
4. 现有 negative-side 方法不能解释 positive-side failure。
5. 现有 heterophily-aware view construction 方法不能提供 pair-level reliability diagnostics。
6. positive failure 和 negative collision 在部分数据集 / 节点组上同时存在。

## 何时认为 Gap 2 不成立

如果观察不到上述现象，应考虑：

1. 回到 Gap 1 的 view reliability / positive reliability calibration。
2. 转向 scalable mini-batch negative noise。
3. 降低论文目标，不做顶会方法主线。

## 下一步方法设计

只有当 failure verification 支持 Gap 2 时，才进入方法设计。下一步应优先设计一个不依赖标签训练的 reliability estimator，用结构、增强一致性、表示稳定性和可选文本证据估计 positive reliability 与 negative reliability，并在训练后用标签做诊断验证其行为是否符合 failure evidence。

