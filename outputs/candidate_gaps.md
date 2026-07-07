# GCL 方法型论文候选 Gap

本文档基于 `outputs/gcl_literature_table.csv` 和 `outputs/method_taxonomy.md` 生成，面向后续方法型论文选题判断。每个 gap 都绑定文献表中的具体证据，并按“现有假设 -> 失败机制 -> 可能方法 -> 实验验证 -> 风险”组织。

## 最推荐优先推进的 3 个 Gap

1. **Gap 1: Heterophily-aware Semantic-Preserving Augmentation**
   - 推荐原因：直接挑战 `GRACE` / `GraphCL` / `GCA` / `BGRL` 的核心假设，即随机扰动或中心性增强在异配图上仍语义保持。补强后 `HLCL` / `HGMS` 已覆盖 heterophily-aware augmentation 的一部分，因此该方向必须聚焦 view / positive reliability calibration 才仍有方法贡献空间。
   - 推荐 venue：NeurIPS / ICLR / ICML；如果以大规模异配 benchmark 和系统评测为主，也适合 KDD / WWW。

2. **Gap 2: Reliability-aware False Negative and False Positive Correction**
   - 推荐原因：`GDCL`、`ProGCL`、`CGC`、`HGMS` 已经确认 false negative 是 GCL 核心问题，但它们主要从聚类、hard negative 概率、反事实生成或异构图 self-expression 入手，仍缺少正负样本双侧、跨图类型可校准的 pair reliability 机制。
   - 推荐 venue：ICML / NeurIPS / ICLR；若强调图挖掘应用和大规模实验，适合 KDD / WWW。

3. **Gap 7: Graph-Text Conflict-aware Contrastive Pretraining**
   - 推荐原因：`GAugLLM`、`GraphGPT`、`MoleculeSTM`、`GraphCLIP` 显示 graph-text/TAG pretraining 和 LLM augmentation 很活跃，但当前多数做法仍未系统处理文本相似但结构冲突、结构相似但文本冲突的样本。
   - 推荐 venue：NeurIPS / ICLR / ICML；若以 text-attributed graph benchmark 和检索/推荐应用为主，适合 KDD / WWW。

## Gap 1: Heterophily-aware Semantic-Preserving Augmentation

- **Gap Name**：Heterophily-aware Semantic-Preserving Augmentation
- **Target Scenario**：异配图、同配-异配混合图、large-scale non-homophilous graph
- **Existing Assumption**：主流 GCL 假设 edge dropping、feature masking、diffusion 或 bootstrap views 不改变节点语义；相邻结构和扩散结构通常被当作可用上下文。
- **Why This Assumption May Fail**：异配图中邻居可能属于不同类别，边不是简单噪声。同一条边在同配图里可能提供平滑信号，在异配图里可能提供角色互补或反同配信号；随机删除或 diffusion 可能把关键异配模式破坏掉。
- **Failure Mode**：false positive view、semantic inconsistency、heterophily edge misclassification、over-smoothing、错误 positive pair。
- **Possible Method**：设计 heterophily-aware view reliability model。先估计边的同配/异配/不确定类型，再按类型生成不同视图：同配边可平滑增强，异配边保留角色差异，不确定边只做弱扰动。对正样本对使用 reliability weight，而不是默认同一节点跨视图一定为强正样本。
- **Possible Modules**：
  - Edge-type uncertainty estimator：估计边是 homophilic、heterophilic 还是 uncertain。
  - View reliability score：衡量增强后节点语义是否仍可信。
  - Dual-channel encoder：分别处理 similarity-preserving 和 role-preserving 信息。
  - Reliability-weighted contrastive loss：低可靠视图降低正对权重。
  - Optional masked reconstruction：用局部结构重构检测增强是否破坏关键邻域。
- **Required Datasets**：Cora、Citeseer、PubMed、Amazon Computers、Coauthor CS 作为同配 sanity check；Chameleon、Squirrel、Actor、Cornell、Texas、Wisconsin；LINKX 论文中的 Penn94、pokec、arXiv-year、snap-patents、genius、twitch-gamers 用于大规模异配。
- **Required Baselines**：DGI、MVGRL、GRACE、GCA、BGRL、CCA-SSG、GraphMAE、GraphMAE2、GREET、HLCL、HGMS、H2GCN、Geom-GCN、LINKX；若方法含 negative-free，还必须比较 AFGRL。
- **Key Experiments**：
  - 主结果：同配图、经典异配图、大规模异配图的 node classification。
  - 消融：去掉 edge-type estimator、去掉 reliability weighting、只用随机 edge dropping、只用 feature masking、只用双通道 encoder。
  - 鲁棒性：人为增加 heterophilic edges、删除 bridge edges、改变同配率。
  - 可扩展性：在 Penn94 / pokec / snap-patents 上报告时间、显存和 batch 训练能力。
  - 机制分析：按边类型统计被保留/删除概率；按 homophily ratio 分组看提升来源；可视化 low-reliability view 是否对应性能下降。
- **Key Risk**：边类型估计可能需要标签或伪标签，如果无监督估计不准，会导致方法复杂但收益不稳定。
- **Novelty Risk**：高于原判断。`GREET` 已做 edge heterophily discriminating，`HLCL` 已用 low-pass / high-pass graph filters 构造 heterophily-aware contrastive views，`HGMS` 已在 heterogeneous graph 中用 connection-strength-guided heterogeneous edge dropping 增强同配性；因此不能再把“异配图上语义保持增强”本身作为主要 novelty。剩余空间必须收窄为“带不确定性的 view reliability / positive reliability calibration / 跨同构-异构-图文场景的统一增强可靠性”，而不是换一个 heterophily score。
- **Incrementality Risk**：中等。如果只是把 GCA 的中心性换成 heterophily score，会被认为小改；如果能提出可校准 reliability objective，并证明能预测 view failure，就不是简单 incremental。
- **Top-conference Potential**：4
- **是否已有高度相似工作**：有。`HLCL` 已经明确做 heterophily-aware augmentation / view construction，`HGMS` 已经在异构图中做 homophily-aware heterogeneous edge dropping，`GREET` 已经做 edge heterophily discriminating。该 gap 还成立的前提是把问题推进到“增强视图是否可靠、正样本是否可靠、边类型是否不确定”的校准框架。
- **是否只是换 augmentation / 换 loss**：风险升高。如果只是把 `HLCL` 的 graph filters 换成另一种 filter，或把 `HGMS` 的 connection strength 换成另一种边分数，会被认为 incremental；只有显式建模 view / pair reliability 并提供 failure diagnostics，才不是简单换增强。
- **是否能形成清楚的方法贡献**：能。核心贡献可以是 heterophily-aware view reliability estimator + reliability-weighted GCL。
- **是否有可验证的 failure mode**：有。可验证随机 edge dropping / diffusion 在低同配率区域导致 positive view 语义不一致。
- **是否有机会做理论或机制分析**：有。可以分析 homophily ratio、edge type uncertainty 与 InfoNCE 正样本噪声的关系。
- **是否适合短期启动实验**：适合。可先在 GRACE/GCA 框架上插入 edge-type reliability 模块做 Cora/Citeseer/PubMed + Chameleon/Squirrel/Actor。
- **强 baseline 攻击点**：HLCL、HGMS、GREET、GCA、BGRL、CCA-SSG、GraphMAE、LINKX。如果不能解释相对 HLCL 的 graph-filter views 和 HGMS 的 MCS-guided edge dropping 还有什么新增可靠性机制，选题会被认为已被覆盖。
- **相关论文与未解决点**：
  - `GRACE`：做 edge dropping + feature masking，但默认随机扰动语义保持；未解决异配边被误删问题。
  - `GCA`：用中心性和特征重要性做 adaptive augmentation，但中心性不等于异配语义可靠性。
  - `BGRL` / `CCA-SSG`：解决负样本和冗余问题，但仍使用 edge dropping / feature masking 视图。
  - `H2GCN` / `Geom-GCN` / `LINKX`：证明异配图需要不同建模，但不是 GCL 增强方法。
  - `GREET`：开始处理异配边判别，但仍可扩展到不确定增强、positive reliability 和大规模异配。
  - `HLCL`：已经做 graph-filter heterophily-aware views，并明确在 homophilic / heterophilic subgraphs 上分别使用 low-pass / high-pass contrast；但边类型来自特征相似度近似，未显式校准子图划分不确定性，也未处理 graph-text 或异构 metapath 冲突。
  - `HGMS`：已经做 connection-strength-guided heterogeneous edge dropping 和 multi-view self-expression，覆盖异构图同配增强；但它的场景主要是 metapath-based heterogeneous graph，未形成通用 view reliability 框架。
- **定向补强后剩余未解决问题**：heterophily-aware augmentation 已有强相关工作；真正未解决的是增强后正样本是否仍可靠、边类型估计是否可校准、低可靠视图是否应被降权，以及该机制能否跨 homophily/heterophily/heterogeneous/TAG 场景泛化。
- **为什么不是简单 incremental**：必须把核心问题定义为“GCL 正视图语义保持假设在异配图上存在可测量的可靠性噪声”，并用 reliability 统一 view generation、positive weighting 和 failure diagnosis；否则相对 `HLCL` / `HGMS` 很容易只是局部增强替换。
- **最可能的核心创新点**：uncertainty-calibrated heterophily-aware semantic reliability estimator，让增强强度、正样本权重和编码器通道共同受可靠性控制，并能预测 view failure。
- **Evidence**：`GRACE` Evidence: Method section on graph augmentation and contrastive objective；`GCA` Evidence: Method section on adaptive augmentation；`BGRL` Evidence: Method section on bootstrapping；`H2GCN` Evidence: Method/theory sections；`LINKX` Evidence: Benchmark/method sections；`GREET` Evidence: Method section on edge heterophily discriminating；`HLCL` Evidence: PMLR Abstract, arXiv Section 4.1, Section 5.1, Tables 1/5/6, Section 6 limitations；`HGMS` Evidence: arXiv Abstract, Sections 3.3/3.4/3.5, Section 4.1, Tables 2/3/5；`method_taxonomy.md` 5.2 Heterophilic Graph 与 6.1 Augmentation Semantic Preservation。

## Gap 2: Reliability-aware False Negative and False Positive Correction

- **Gap Name**：Reliability-aware False Negative and False Positive Correction
- **Target Scenario**：node-level GCL、graph-level GCL、异配图、推荐图、graph-text contrastive pretraining
- **Existing Assumption**：InfoNCE-style GCL 默认正样本语义一致，batch 内其他样本大多为负样本；hard negative 越难越有价值。
- **Why This Assumption May Fail**：同类节点、相似分子、相似用户偏好或文本语义相似图可能被当作负样本；同时，增强过强时同一实例跨视图也可能变成 false positive view。
- **Failure Mode**：false negative pair、false positive view、class collision、hard negative misweighting、semantic inconsistency。
- **Possible Method**：提出 pair reliability network，同时估计 positive reliability 和 negative reliability。正样本可靠性低时降低 alignment；负样本疑似 false negative 时降低 repulsion；hard negative 只有在 true-negative confidence 足够高时才增强。
- **Possible Modules**：
  - Multi-evidence reliability estimator：融合表示相似度、结构距离、局部标签传播不确定性、增强一致性、可选文本/时间证据。
  - Positive reliability gate：识别过强增强导致的 false positive view。
  - Negative confidence calibration：对 batch negatives 进行连续权重。
  - Hard-negative triage：分为 true-hard、false-hard、uncertain-hard。
  - Reliability diagnostics：输出 pair reliability 与下游错误的相关性。
- **Required Datasets**：Cora、Citeseer、PubMed、Amazon、Coauthor；Chameleon、Squirrel、Actor；TU datasets / MoleculeNet；推荐数据 Gowalla、Yelp、Amazon-Book；text-attributed graph 可作为扩展。
- **Required Baselines**：DGI、MVGRL、InfoGraph、GRACE、GCA、GraphCL、AD-GCL、JOAO、BGRL、CCA-SSG、GDCL、ProGCL、CGC、HLCL、HGMS、GraphMAE、GraphMAE2。
- **Key Experiments**：
  - 主结果：node classification、graph classification、recommendation 或 molecule property 至少覆盖两个图类型。
  - 消融：只修正 negative、只修正 positive、去掉 hard-negative triage、只用相似度可靠性、只用聚类可靠性。
  - 机制分析：用标签后验统计被降权的 negatives 中有多少同类；统计低可靠 positives 是否对应增强破坏。
  - 鲁棒性：提高 batch size、增加同类节点密度、增强强度加大，观察 false negative / false positive 对性能影响。
  - 可扩展性：比较 reliability estimator 的额外时间和显存。
- **Key Risk**：无标签场景下 pair reliability 难以准确估计，若估计器本身依赖当前表示，会出现 early-stage confirmation bias。
- **Novelty Risk**：高于原判断。`GDCL`、`ProGCL`、`CGC` 已覆盖 false negative / hard negative；新增 `HGMS` 还在 heterogeneous graph 中用 multi-view self-expression 缓解 false negatives，`HLCL` 则从 heterophily-aware views 侧面减少 false positive views。因此 Gap 2 不能只声称“修正 false negative”。剩余 novelty 必须是 positive reliability 与 negative reliability 的双向校准、true-hard / false-hard / uncertain-hard 区分，以及跨 node/graph/heterogeneous/graph-text 场景的统一证据融合。
- **Incrementality Risk**：中等偏高。如果只是给 InfoNCE 加一个相似度权重，会被认为 incremental；如果能证明 false positive view 和 false negative pair 同时存在，并统一处理，风险下降。
- **Top-conference Potential**：5
- **是否已有高度相似工作**：有。`GDCL`、`ProGCL`、`CGC` 是 negative reliability / hard negative 方向强相关工作；`HGMS` 已经把 self-expression 用于 HeteroGCL 的 false negative mitigation；`HLCL` 已经通过 heterophily-aware view construction 间接减少 false positive views。但目前仍缺少同时估计 positive reliability 与 negative reliability 的统一框架。
- **是否只是换 augmentation / 换 loss**：不是，若方法输出可解释 pair reliability 并改变 positive/negative 双侧训练；否则可能被看成 loss reweighting。
- **是否能形成清楚的方法贡献**：能。核心是 pair reliability as a first-class variable。
- **是否有可验证的 failure mode**：有。可以用真实标签后验统计 false negatives，用增强强度/结构破坏制造 false positive views。
- **是否有机会做理论或机制分析**：有。可将 InfoNCE 视为带噪 positive/negative labels 的风险最小化，分析 reliability weighting 降低噪声偏差。
- **是否适合短期启动实验**：适合。可先在 GRACE/GCA + ProGCL 风格 hard negative 上实现。
- **强 baseline 攻击点**：ProGCL、GDCL、CGC、HGMS、HLCL、GCA、BGRL、CCA-SSG。如果不能说明相对 ProGCL/GDCL/CGC 的负样本处理、相对 HGMS 的 false negative mitigation、相对 HLCL 的 view reliability 还有新增机制，选题站不稳。
- **相关论文与未解决点**：
  - `GRACE` / `GraphCL` / `InfoGraph`：使用 batch 或跨图 negatives，但未识别同类 false negatives。
  - `GCA`：改善增强，但仍把其他节点当负样本。
  - `GDCL`：用聚类估计 false negatives，但聚类可靠性和早期训练不稳定未完全解决。
  - `ProGCL`：渐进式 true-negative probability，但主要针对 hard negatives。
  - `CGC`：生成 counterfactual hard negatives，但生成负样本语义是否真正相异难验证。
  - `HLCL`：通过 heterophily-aware filtered views 降低异配图中 false positive view 的风险，但并没有显式给每个 positive / negative pair 校准可靠性。
  - `HGMS`：通过 multi-view self-expression 缓解 heterogeneous graph 中的 false negatives，但主要针对 metapath/HeteroGCL 场景，未覆盖 false positive view 与跨域 pair reliability。
- **定向补强后剩余未解决问题**：positive/negative reliability 已有局部处理，但还没有一个同时回答“正对是否仍语义一致、负对是否确实相异、hard negative 是否真实、跨模态证据冲突时如何降权”的统一模型。
- **为什么不是简单 incremental**：因为它同时挑战两个基础假设：正样本不一定真正、负样本不一定相异；要做成方法型论文，必须证明这是 GCL 训练标签噪声的统一校准问题，而不是给 InfoNCE 再加一层相似度权重。
- **最可能的核心创新点**：双向 pair reliability calibration，把 positive alignment 和 negative repulsion 都变成可置信训练信号，并输出可验证的 true-hard / false-hard / uncertain-hard 诊断。
- **Evidence**：`GRACE` Evidence: contrastive objective；`GraphCL` Evidence: graph augmentations and InfoNCE；`GDCL` Evidence: joint clustering/debiasing；`ProGCL` Evidence: Method/theory on ProGCL；`CGC` Evidence: counterfactual hard negatives；`HLCL` Evidence: arXiv Section 4.1/4.2 and Tables 1/5/6；`HGMS` Evidence: arXiv Sections 3.4/3.5 and Tables 2/3/5；`method_taxonomy.md` 4.4 False Negative Correction 与 6.2 False Negative / Class Collision。

## Gap 3: Negative-free GCL under Heterophily and Sparse Graphs

- **Gap Name**：Negative-free GCL under Heterophily and Sparse Graphs
- **Target Scenario**：异配图、稀疏图、大规模图、无负样本 GCL
- **Existing Assumption**：negative-free GCL 假设 bootstrap、stop-gradient、predictor、decorrelation 或 reconstruction 足以避免坍塌，同时增强视图仍保持语义。
- **Why This Assumption May Fail**：异配图和稀疏图中邻域上下文不稳定，随机 edge dropping 会改变关键结构；无负样本目标没有显式 repulsion，可能在局部结构噪声下发生 class mixing 或局部坍塌。
- **Failure Mode**：representation collapse、class mixing、over-smoothing、false positive view、degree bias。
- **Possible Method**：设计 structure-aware anti-collapse regularizer，不引入传统 negatives，而是用谱约束、局部同配率、prototype dispersion 或 uncertainty-aware decorrelation 控制表示坍塌。
- **Possible Modules**：
  - Local homophily estimator：估计节点区域的同配/异配强度。
  - Conditional redundancy reduction：不同区域采用不同 decorrelation 强度。
  - Prototype dispersion without negatives：原型级分散，避免节点级 false negatives。
  - Collapse diagnostics：监控 embedding spectrum、rank、class mixing、degree-wise variance。
  - Heterophily-safe augmentation：低同配区域弱化 edge dropping。
- **Required Datasets**：Cora、Citeseer、PubMed、Amazon、Coauthor；Chameleon、Squirrel、Actor、Cornell、Texas、Wisconsin；Penn94、pokec、arXiv-year、snap-patents。
- **Required Baselines**：BGRL、CCA-SSG、AFGRL、SelfGNN、GRACE、GCA、GREET、GraphMAE、LINKX、H2GCN。
- **Key Experiments**：
  - 主结果：node classification across homophily ratios。
  - 消融：去掉 anti-collapse regularizer、去掉 local homophily conditioning、固定 decorrelation、固定 augmentation。
  - 机制分析：embedding rank、singular value spectrum、不同同配率分组的 collapse 指标。
  - 鲁棒性：低标签率、稀疏边、噪声边、degree imbalance。
  - 可扩展性：mini-batch 训练和 OGBN-Arxiv / Penn94 级别图。
- **Key Risk**：防坍塌约束可能只是已有 CCA-SSG/BGRL 的变体；必须证明 heterophily/sparsity 下已有 negative-free 方法确实失败。
- **Novelty Risk**：`BGRL`、`CCA-SSG`、`AFGRL` 已经是强相关工作；若只是加谱正则，很容易撞已有 redundancy / covariance regularization。
- **Incrementality Risk**：中等偏高。需要把问题明确成“negative-free 在异配/稀疏图上的结构性失败”，并提出图特有条件化机制。
- **Top-conference Potential**：4
- **是否已有高度相似工作**：没有完全相同，但有强相邻工作。`CCA-SSG` 做 redundancy reduction，`BGRL` 做 bootstrap，`AFGRL` 做 augmentation-free positive mining。
- **是否只是换 augmentation / 换 loss**：有风险。若只是把 BGRL loss 加上 covariance penalty，就是换 loss；若加入局部同配率条件化和 collapse 机制分析，则更清楚。
- **是否能形成清楚的方法贡献**：可以，但需要理论或机制分析支撑。
- **是否有可验证的 failure mode**：有。可以验证 BGRL/CCA-SSG 在低同配率或稀疏图上的 embedding rank 和 class mixing。
- **是否有机会做理论或机制分析**：很适合。可分析 negative-free objective 在 graph smoothing operator 下的谱坍塌风险。
- **是否适合短期启动实验**：中等适合。先做诊断实验，再决定是否方法足够新。
- **强 baseline 攻击点**：BGRL、CCA-SSG、AFGRL、GraphMAE、GREET。如果不能解释为什么这些不够，容易被拒。
- **相关论文与未解决点**：
  - `BGRL`：解决大规模负样本成本，但仍依赖 edge dropping / feature masking。
  - `CCA-SSG`：用 decorrelation 防坍塌，但未针对异配区域自适应。
  - `AFGRL`：无增强正样本选择，但主要验证常见同配图。
  - `GREET`：处理异配图 SSL，但仍使用对比负样本，并非 negative-free 防坍塌路线。
  - `LINKX`：暴露大规模异配图挑战，但不是 SSL。
- **为什么不是简单 incremental**：必须把贡献做成“图结构条件化防坍塌机制”，而不是 BYOL/CCA 的图上复刻。
- **最可能的核心创新点**：local-homophily-conditioned anti-collapse objective。
- **Evidence**：`BGRL` Evidence: Method section on bootstrapping and scalability；`CCA-SSG` Evidence: Method/theory deriving CCA-SSG；`AFGRL` Evidence: Method section on AFGRL；`GREET` Evidence: edge heterophily discriminating；`LINKX` Evidence: large-scale non-homophilous benchmark；`method_taxonomy.md` 3.3、3.4、6.3。

## Gap 4: Contrastive-Generative Reliability Learning

- **Gap Name**：Contrastive-Generative Reliability Learning
- **Target Scenario**：GCL 与 GraphMAE 统一、通用属性图、异配图、分子图
- **Existing Assumption**：GCL 假设视图之间语义一致，GraphMAE 假设被 mask 的属性/结构可由上下文重构；二者通常被并列或简单加权组合。
- **Why This Assumption May Fail**：对比视图可能语义不一致，重构目标也可能只恢复表面特征或 adjacency pattern。简单相加 InfoNCE 和 reconstruction 不能判断哪个训练信号可靠。
- **Failure Mode**：false positive view、semantic inconsistency、surface-level reconstruction、overfitting to attributes、hybrid loss conflict。
- **Possible Method**：让 masked reconstruction 不是独立预训练目标，而是用来估计 view 或 pair 的可靠性。例如，一个增强视图若无法重构关键 masked semantic tokens，则降低其 positive alignment 权重；一个负样本若重构语义高度相似，则降低 repulsion。
- **Possible Modules**：
  - Masked semantic probe：用 masked feature/edge/subgraph reconstruction 评估视图是否保留语义。
  - Contrastive reliability gate：用 reconstruction confidence 调节 InfoNCE。
  - Dual decoder：分别重构属性和结构，检测哪类语义被破坏。
  - Conflict-aware loss scheduler：当 contrastive 与 generative signals 冲突时动态调整权重。
  - Reliability report：输出每种 augmentation 的破坏率。
- **Required Datasets**：Cora、Citeseer、PubMed、Amazon、Coauthor；Chameleon、Squirrel、Actor；MUTAG、NCI1、MoleculeNet；OGBN-Arxiv 或 OGBN-Papers100M 子集用于可扩展性。
- **Required Baselines**：GRACE、GCA、GraphCL、AD-GCL、JOAO、BGRL、CCA-SSG、GraphMAE、GraphMAE2、MaskGAE、MVGRL。
- **Key Experiments**：
  - 主结果：node classification、graph classification、molecular property。
  - 消融：只用 contrastive、只用 reconstruction、简单 loss 相加、用 reconstruction 只做 auxiliary、不用 reliability gate。
  - 机制分析：不同 augmentation 的 reconstruction failure rate 与下游性能相关性。
  - 鲁棒性：增强强度从弱到强，观察 reliability gate 是否降低坏视图权重。
  - 可扩展性：比较双目标训练开销与 GraphMAE2 / BGRL。
- **Key Risk**：如果方法只是“GraphMAE + InfoNCE”，会非常 incremental；必须证明生成目标确实用于可靠性决策，而非辅助 loss。
- **Novelty Risk**：`GraphMVP`、`Mole-BERT` 已经有 contrastive-generative hybrid；`GraphMAE2` 和 `MaskGAE` 已经深入 masked modeling。需要避开“混合目标”泛泛叙事。
- **Incrementality Risk**：高。只有在核心模块是 reliability learning 而不是 loss addition 时才值得投顶会。
- **Top-conference Potential**：4
- **是否已有高度相似工作**：有相邻但不完全相同。`GraphMVP` 和 `Mole-BERT` 结合 contrastive/generative，但主要在分子预训练；`GraphMAE` 系列不是用 reconstruction 评估 GCL view reliability。
- **是否只是换 augmentation / 换 loss**：风险很高。必须避免只是换 loss。
- **是否能形成清楚的方法贡献**：能，但贡献点应是“generative probe for contrastive reliability”。
- **是否有可验证的 failure mode**：有。强增强导致 reconstruction failure 和 downstream drop；坏正样本被 gate 降权。
- **是否有机会做理论或机制分析**：有。可分析 reconstruction confidence 作为 latent semantic preservation proxy 的条件。
- **是否适合短期启动实验**：适合做 prototype，但完整论文需要多任务验证。
- **强 baseline 攻击点**：GraphMAE、GraphMAE2、MaskGAE、GRACE、GCA、BGRL、CCA-SSG、GraphMVP、Mole-BERT。
- **相关论文与未解决点**：
  - `GraphMAE`：masked feature reconstruction，未判断 GCL view 是否可靠。
  - `GraphMAE2`：增强 decoder，但仍是 masked SSL 主线。
  - `MaskGAE`：结构 mask 与 GAE 关系，未服务于 contrastive reliability。
  - `GRACE` / `GCA`：使用增强对比，但没有生成式 probe 检测增强破坏。
  - `GraphMVP` / `Mole-BERT`：hybrid 主要在分子，不是通用 view reliability 框架。
- **为什么不是简单 incremental**：只有当生成任务输出直接控制正负样本权重，并能诊断 view failure，才不是增量。
- **最可能的核心创新点**：masked reconstruction as a semantic reliability estimator for GCL。
- **Evidence**：`GraphMAE` Evidence: Section 3 GraphMAE；`GraphMAE2` Evidence: decoding enhancement；`MaskGAE` Evidence: masked graph modeling；`GRACE` / `GCA` Evidence: graph augmentation and adaptive augmentation；`GraphMVP` Evidence: 2D-3D pretraining；`method_taxonomy.md` 3.6、3.7、6.1。

## Gap 5: Mini-batch Friendly Scalable GCL with Controlled Negative Noise

- **Gap Name**：Mini-batch Friendly Scalable GCL with Controlled Negative Noise
- **Target Scenario**：大规模图、large-scale heterophily graph、OGB 级别图
- **Existing Assumption**：全图或大 batch 对比学习可以提供足够 negatives；采样后的局部子图仍能代表全图语义；negative-free 方法可绕开 pairwise 成本。
- **Why This Assumption May Fail**：全图 negatives 显存成本高，mini-batch 采样改变负样本分布；大规模异配图中高相似节点可能被采样为负样本，导致 false negative；diffusion-based views 在大图上成本更高。
- **Failure Mode**：scalability issue、false negative pair、sampling bias、degree bias、memory bottleneck。
- **Possible Method**：设计 mini-batch compatible GCL objective：用 memory bank / sketching / sampled prototypes 提供低噪声 negatives，同时用 reliability estimator 控制采样偏差；或者用 negative-free core + prototype dispersion 替代 batch negatives。
- **Possible Modules**：
  - Subgraph sampler with reliability constraints。
  - Prototype memory bank：避免存储所有节点 pair。
  - Negative noise estimator：估计 mini-batch negatives 的 collision risk。
  - Degree-aware sampling correction。
  - Complexity-aware objective：目标函数显式约束时间和显存。
- **Required Datasets**：OGBN-Arxiv、OGBN-Products、Reddit、PPI；LINKX benchmark 中 Penn94、pokec、snap-patents；可补 OGBN-Papers100M 子集或 GraphMAE2 报告的大图设置。
- **Required Baselines**：GraphSAGE、GCC、BGRL、GRACE、GCA、CCA-SSG、GraphMAE2、LINKX、DGI、MVGRL；大图推荐扩展可比 LightGCL。
- **Key Experiments**：
  - 主结果：大规模 node classification，报告性能/时间/显存。
  - 消融：无 reliability sampling、无 memory bank、全图 negatives、小 batch negatives、negative-free variant。
  - 可扩展性：节点数、边数、batch size 扩展曲线。
  - 机制分析：mini-batch negatives 中同类/近邻 collision rate。
  - 鲁棒性：degree imbalance、边稀疏、同配率变化。
- **Key Risk**：工程复杂度高；如果性能只比 BGRL/GraphMAE2 略高但成本更大，贡献不成立。
- **Novelty Risk**：`BGRL` 已强调 large-scale negative-free，`GraphSAGE` 早有采样，`GraphMAE2` 报告大规模 masked SSL；新方法必须解决“采样负样本噪声”这个明确缺口。
- **Incrementality Risk**：中等。如果只是加 memory bank 或改 sampler，容易被认为工程优化；若有 negative noise 控制和复杂度证明，风险下降。
- **Top-conference Potential**：4
- **是否已有高度相似工作**：有相邻工作。`BGRL` 解决无负样本大规模，`GraphSAGE` 解决采样，`GCC` 解决跨图子图预训练，但没有统一 mini-batch negative noise correction。
- **是否只是换 augmentation / 换 loss**：不是，若重点是 scalable objective + sampling bias correction。
- **是否能形成清楚的方法贡献**：能，但需要强大图实验。
- **是否有可验证的 failure mode**：有。小 batch negatives 分布偏差和 class collision 可统计。
- **是否有机会做理论或机制分析**：有。可分析 sampled InfoNCE estimator 的 bias / variance 和 false negative probability。
- **是否适合短期启动实验**：中等。需要大图训练环境；可先在 OGBN-Arxiv 和 Penn94 原型验证。
- **强 baseline 攻击点**：BGRL、GraphMAE2、GraphSAGE、LINKX、GCC。如果不能显示效率-性能优势，风险大。
- **相关论文与未解决点**：
  - `GraphSAGE`：采样式大图学习，但不是 GCL。
  - `GCC`：子图 instance discrimination，但跨图预训练和负样本噪声仍存在。
  - `BGRL`：避免 negatives，但没有处理异配/采样噪声下的语义可靠性。
  - `GraphMAE2`：大规模 masked SSL，但不是 contrastive negative noise。
  - `LINKX`：强调大规模异配挑战，但非自监督。
- **为什么不是简单 incremental**：只要目标是“mini-batch sampled contrastive estimator 的噪声校正”，它比换增强更基础。
- **最可能的核心创新点**：scalable reliability-controlled sampled contrastive objective。
- **Evidence**：`BGRL` Evidence: scalability section；`GraphSAGE` Evidence: sampling/aggregators；`GCC` Evidence: subgraph sampling；`GraphMAE2` Evidence: large-scale graph；`LINKX` Evidence: large-scale non-homophilous benchmarks；`method_taxonomy.md` 5.8 与 6.4。

## Gap 6: Recommendation GCL Beyond Noise Regularization

- **Gap Name**：Recommendation GCL Beyond Noise Regularization
- **Target Scenario**：推荐图、user-item graph、长尾推荐、稀疏交互图
- **Existing Assumption**：推荐 GCL 中 node/edge dropout、embedding noise、邻居增强或 SVD view 都默认保留用户偏好语义，并将对比收益解释为更好的协同表示。
- **Why This Assumption May Fail**：推荐图中的交互可能受曝光偏差、流行度偏差和时间变化影响；embedding noise 的收益可能只是正则化或 uniformity，而不是结构语义学习；SVD view 可能强化 popularity bias。
- **Failure Mode**：degree bias、popularity bias、false negative item/user、semantic inconsistency、spurious neighbor contrast。
- **Possible Method**：构建 bias-aware recommendation GCL。把 user-item pair 的曝光/流行度/时间不确定性引入 view generation 与 contrastive weighting，区分“真实偏好正样本”和“曝光造成的伪正样本”。
- **Possible Modules**：
  - Popularity-aware view reliability。
  - Exposure debiasing module。
  - Temporal preference drift detector。
  - Long-tail preserving augmentation。
  - Bias-aware contrastive loss with BPR。
- **Required Datasets**：Gowalla、Yelp、Amazon-Book；可加 KuaiRec / MovieLens / Amazon 多领域数据用于曝光或时间分析。
- **Required Baselines**：LightGCN、SGL、SimGCL、NCL、LightGCL、BPR、NGCF；如果引入时间，需要动态推荐 baseline。
- **Key Experiments**：
  - 主结果：Recall@K、NDCG@K。
  - 分组实验：按 item popularity、user activity、交互稀疏度分组。
  - 消融：去掉 popularity reliability、去掉 exposure correction、去掉 temporal module、只用 SimGCL noise。
  - 鲁棒性：人为加入热门 item 噪声和随机曝光边。
  - 机制分析：表示 uniformity、alignment、长尾 item recall、被降权边的 popularity 分布。
- **Key Risk**：推荐 GCL 已经拥挤，容易被看成 SGL/SimGCL/NCL/LightGCL 的领域小改。
- **Novelty Risk**：高。必须证明研究对象不是“再加一种增强”，而是解释和纠正推荐 GCL 的 bias failure。
- **Incrementality Risk**：高。如果没有 exposure/popularity failure mode 诊断，容易 incremental。
- **Top-conference Potential**：3
- **是否已有高度相似工作**：强相关工作很多：`SGL`、`SimGCL`、`NCL`、`LightGCL`。它们分别覆盖随机增强、无结构增强、邻域正样本、SVD 全局视图。
- **是否只是换 augmentation / 换 loss**：风险很高。必须做 bias-aware 机制和分组验证。
- **是否能形成清楚的方法贡献**：可以，但更像 KDD / WWW / SIGIR / TKDE 方向，而非纯 NeurIPS/ICML 方法。
- **是否有可验证的 failure mode**：有。可验证热门 item false negatives、SVD view popularity amplification、long-tail recall 下降。
- **是否有机会做理论或机制分析**：有一定机会。可分析 contrastive uniformity 与 popularity distribution 的关系。
- **是否适合短期启动实验**：适合。推荐数据和 LightGCN 框架成熟。
- **强 baseline 攻击点**：SimGCL 和 LightGCL 非常强；如果不能稳定提升长尾和整体指标，风险大。
- **相关论文与未解决点**：
  - `SGL`：随机 dropout 视图，未显式建模曝光/流行度偏差。
  - `SimGCL`：说明结构增强不必要，embedding noise 很强；会攻击任何新增强的必要性。
  - `NCL`：结构邻居和语义邻居，但可能受 popularity-driven neighbors 影响。
  - `LightGCL`：SVD view 捕获全局协同，但可能强化主流模式。
  - `BGRL` / `CCA-SSG`：提供 negative-free 思路，但未处理推荐偏差。
- **为什么不是简单 incremental**：只有当方法回答“GCL 在推荐中到底学到偏好还是学到 popularity regularization”时，才不是小改。
- **最可能的核心创新点**：bias-aware view reliability for recommendation contrastive learning。
- **Evidence**：`SGL` Evidence: Method section on SGL augmentations；`SimGCL` Evidence: Method section on SimGCL；`NCL` Evidence: Method section on NCL；`LightGCL` Evidence: SVD view；`method_taxonomy.md` 5.4 Recommendation Graph 与 6.5 Robustness。

## Gap 7: Graph-Text Conflict-aware Contrastive Pretraining

- **Gap Name**：Graph-Text Conflict-aware Contrastive Pretraining
- **Target Scenario**：graph foundation model、text-attributed graph、molecule-text pretraining、graph-to-LLM alignment
- **Existing Assumption**：graph-text contrastive pretraining 默认匹配的 graph-text pair 语义一致，不匹配的 batch pairs 是负样本。
- **Why This Assumption May Fail**：文本描述可能不完整、噪声大或与图结构关注点不同；不同图可能有相似文本，不同文本也可能描述相似结构。简单 CLIP-style negatives 会产生 text-level false negatives 和 structure-text conflict。
- **Failure Mode**：graph-text false negative、semantic conflict、modality collapse、spurious alignment、instruction overfitting。
- **Possible Method**：设计 conflict-aware graph-text contrastive objective。显式检测结构相似但文本冲突、文本相似但结构冲突、两模态均不确定三类样本，并用软标签或三元关系目标替代硬 InfoNCE。
- **Possible Modules**：
  - Graph-text agreement estimator。
  - Cross-modal conflict classifier。
  - Soft contrastive labels for near-duplicate text or structure。
  - Structure-preserving text augmentation。
  - Optional LLM explanation module：生成冲突原因但不直接参与评分。
- **Required Datasets**：MoleculeSTM 使用的 molecule-text corpus；text-attributed citation/product graphs；OGB-Arxiv with titles/abstracts；若可行加入 PubMed / arXiv text-attributed node classification。
- **Required Baselines**：GAugLLM、MoleculeSTM、GraphCLIP、GraphGPT；GraphMAE / GraphMAE2 作为 structure-only pretraining；GRACE/GCA/BGRL/CCA-SSG 作为 graph-only SSL；CLIP-style graph-text baseline。
- **Key Experiments**：
  - 主结果：graph-text retrieval、zero-shot / few-shot node classification、transfer learning。
  - 消融：去掉 conflict classifier、硬 InfoNCE、只用文本相似软标签、只用结构相似软标签。
  - 机制分析：人工或启发式构造 conflict pairs，测模型是否降低错误 alignment。
  - 鲁棒性：文本噪声、标题替换、摘要截断、结构扰动。
  - 可扩展性：预训练成本和检索索引规模。
- **Key Risk**：graph-text 方向数据和模型工程量较大；如果没有高质量 conflict benchmark，很难证明 gap。
- **Novelty Risk**：中等偏高。`GAugLLM` 已经用 LLM 同时做 TAG feature augmentation 和 edge augmentation，`GraphCLIP` / `MoleculeSTM` 已覆盖 graph-text contrastive alignment，`GraphGPT` 覆盖图到 LLM 指令调优；因此不能把“LLM 改进 graph-text/TAG augmentation”当作主要 novelty。剩余空间必须是 structure-text conflict taxonomy、conflict-aware soft labels、cross-modal positive/negative reliability，以及能证明 GAugLLM 这类 LLM augmentation 仍会失败的机制实验。
- **Incrementality Risk**：中等偏高。如果只是把 CLIP loss 换成加权 loss，或在 GAugLLM 上再换一个 LLM prompt，会被质疑；如果有明确 conflict taxonomy、可复现实验集和软标签/可靠性目标，风险较低。
- **Top-conference Potential**：5
- **是否已有高度相似工作**：有部分高度相似。`GAugLLM` 已经是 text-attributed graph 上的 LLM-based GCL augmentation，`GraphCLIP` 已经做 TAG 的 language-graph pretraining；但它们没有系统定义结构-文本冲突类型，也没有显式给 graph-text pairs 做 reliability calibration。
- **是否只是换 augmentation / 换 loss**：有风险。若只是把 GAugLLM 的 LLM feature/edge augmentation 换成新 prompt 或换损失，很容易 incremental；核心必须是 conflict modeling、soft pair semantics 和可验证的 conflict failure mode。
- **是否能形成清楚的方法贡献**：能。graph-text pair reliability / conflict-aware contrastive learning。
- **是否有可验证的 failure mode**：有。可构造文本相似但结构不同、结构相似但文本不同的 conflict sets。
- **是否有机会做理论或机制分析**：有。可分析多模态对比中的 false negative / false positive pair noise。
- **是否适合短期启动实验**：中等。若先用 OGB-Arxiv title/abstract + graph structure 可较快启动；分子图文需要更多工程。
- **强 baseline 攻击点**：GAugLLM、GraphCLIP、MoleculeSTM、GraphGPT、GraphMAE2、BGRL、CCA-SSG。若不能解释相对 GAugLLM 的 LLM augmentation 仍有什么未解决的 structure-text conflict，或只在一个 graph-text 数据集有效，泛化会被质疑。
- **相关论文与未解决点**：
  - `MoleculeSTM`：对齐 molecule-text pair，但主要在分子检索/编辑；冲突样本未系统处理。
  - `GraphCLIP`：CLIP-style text-attributed graph pretraining，但容易继承 CLIP 的 in-batch false negative 问题。
  - `GraphGPT`：图指令调优，更多关注 LLM 图理解，不是 pair reliability。
  - `GAugLLM`：已经用 LLM 做 TAG feature augmentation 和 edge modifier，处理了“文本语义可帮助增强”的问题；但没有把结构-文本冲突分成可诊断类型，也未显式处理 graph-text positive / negative reliability。
  - `GraphMAE2`：结构 masked pretraining，可作为结构-only 对照，但无文本冲突机制。
  - `GRACE` / `GCA`：graph-only GCL，不能处理文本语义。
- **定向补强后剩余未解决问题**：graph-text / TAG augmentation 已有 GAugLLM 这样的强相关工作；真正未解决的是文本相似但结构冲突、结构相似但文本冲突、LLM 生成文本与真实结构证据冲突时，正负样本语义如何重新定义和校准。
- **为什么不是简单 incremental**：它不是给 graph-text loss 加权，也不是再做 LLM augmentation，而是定义结构-文本冲突类型并改变正负样本语义；需要证明现有 GAugLLM/GraphCLIP 在冲突样本上会产生可测失败。
- **最可能的核心创新点**：cross-modal pair reliability and conflict-aware contrastive objective，配合可复现的 structure-text conflict benchmark / diagnostics。
- **Evidence**：`GAugLLM` Evidence: arXiv Abstract, Sections 4.1/4.2, Section 5.1, Tables 2/3/4, KDD DOI, official GitHub；`MoleculeSTM` Evidence: molecule-text contrastive learning；`GraphCLIP` Evidence: Method section on GraphCLIP；`GraphGPT` Evidence: graph instruction tuning；`GraphMAE2` Evidence: large-scale masked graph SSL；`method_taxonomy.md` 2.6 Graph-Text 与 6.7 Graph Foundation Model Pretraining。

## Gap 8: Molecular Semantic-valid Augmentation beyond 2D Random Perturbation

- **Gap Name**：Molecular Semantic-valid Augmentation beyond 2D Random Perturbation
- **Target Scenario**：分子图、molecular property prediction、2D-3D molecular pretraining
- **Existing Assumption**：GraphCL-style node/edge/subgraph perturbation 或 graph-level augmented views 不改变分子语义；2D-3D views 天然互补且语义一致。
- **Why This Assumption May Fail**：分子图中删除原子/键可能改变化学有效性或性质；3D conformer 有噪声和多构象不确定性；文本/属性描述可能关注不同化学语义。
- **Failure Mode**：semantic inconsistency、invalid molecule view、false positive molecular pair、3D conformer noise、property-specific view conflict。
- **Possible Method**：设计 property-aware molecular view reliability。增强操作必须满足化学有效性约束，并根据目标性质或预训练任务估计视图是否保持关键化学 motif；对 2D-3D 对齐加入 conformer uncertainty。
- **Possible Modules**：
  - Chemistry-valid augmenter：约束 atom/bond perturbation。
  - Motif-preservation checker。
  - 3D conformer uncertainty weighting。
  - Property-aware contrastive gate。
  - Hybrid masked token + 2D-3D contrastive objective。
- **Required Datasets**：MoleculeNet、ZINC、GEOM、PCQM4M 子集；若做 molecule-text，可加 MoleculeSTM corpus。
- **Required Baselines**：GraphCL、JOAO、AD-GCL、GROVER、GraphMVP、Mole-BERT、MoleculeSTM、GraphMAE/GraphMAE2 molecular setting。
- **Key Experiments**：
  - 主结果：MoleculeNet classification/regression，scaffold split。
  - 消融：无化学约束增强、无 motif checker、无 conformer uncertainty、只用 GraphCL 增强、只用 GraphMVP 2D-3D。
  - 鲁棒性：不同 conformer noise、不同 scaffold、低数据迁移。
  - 机制分析：被拒绝/降权的增强是否破坏关键 functional groups；按 property type 分组。
  - 可扩展性：预训练数据规模和 3D 计算成本。
- **Key Risk**：需要化学先验；如果方法太领域化，可能不被通用 GCL 会议审稿人认为是一般方法。
- **Novelty Risk**：中等偏高。`GraphMVP`、`Mole-BERT`、`GROVER` 已覆盖分子预训练多个方向；必须聚焦 semantic-valid augmentation，而不是又一个分子预训练组合。
- **Incrementality Risk**：中等。如果只是换分子增强算子，风险高；若建模 view validity / motif preservation，则更有贡献。
- **Top-conference Potential**：4
- **是否已有高度相似工作**：相邻工作多，但不完全相同。GraphMVP 做 2D-3D，Mole-BERT 做 token + graph contrastive，GROVER 做大规模分子自监督。
- **是否只是换 augmentation / 换 loss**：有风险。需要把增强合法性和性质保持作为核心变量。
- **是否能形成清楚的方法贡献**：能，但偏领域方法。
- **是否有可验证的 failure mode**：有。可检测增强后分子是否无效、functional group 是否被破坏、property prediction 是否下降。
- **是否有机会做理论或机制分析**：有限但可做机制分析，如 motif preservation 与性能相关性。
- **是否适合短期启动实验**：中等。需要分子工具和 3D 数据处理。
- **强 baseline 攻击点**：GraphMVP、Mole-BERT、GROVER、GraphCL/JOAO/AD-GCL。如果无法赢分子强 baseline，难投顶会。
- **相关论文与未解决点**：
  - `GraphCL`：通用图增强，分子语义合法性不充分。
  - `AD-GCL` / `JOAO`：学习或搜索增强，但未显式保证化学 motif。
  - `GROVER`：分子 Transformer 预训练，不是 contrastive view validity。
  - `GraphMVP`：2D-3D 对齐，但 conformer uncertainty 仍可深入。
  - `Mole-BERT`：tokenization + masked/contrastive，但不是 property-aware augmentation。
- **为什么不是简单 incremental**：如果以“化学语义有效性约束 + 视图可靠性”为核心，而非新增增强，就不是简单算子替换。
- **最可能的核心创新点**：property-aware molecular view reliability estimator。
- **Evidence**：`GraphCL` Evidence: graph augmentations；`AD-GCL` Evidence: adversarial augmentation；`GraphMVP` Evidence: 2D-3D pretraining；`Mole-BERT` Evidence: masked atom/token + graph contrastive；`GROVER` Evidence: molecular self-supervised tasks；`method_taxonomy.md` 5.3 Molecular Graph。

## Gap 9: Non-stationary Temporal View Reliability for Dynamic GCL

- **Gap Name**：Non-stationary Temporal View Reliability for Dynamic GCL
- **Target Scenario**：动态图、temporal graph、dynamic prediction
- **Existing Assumption**：动态 GCL 假设相近时间窗口、temporal subgraph 或 timespan views 共享可对齐语义。
- **Why This Assumption May Fail**：真实动态图存在突变、周期性、事件驱动变化和概念漂移；相邻时间视图可能语义不同，远距离时间视图可能周期相似。
- **Failure Mode**：false positive temporal view、temporal false negative、semantic drift、non-stationary collapse、time-window bias。
- **Possible Method**：设计 non-stationary temporal reliability model。根据变化点、时间频率、边事件强度和表示漂移判断两个 temporal views 是否应对齐；对突变区域降低正样本权重或引入 change-aware contrast。
- **Possible Modules**：
  - Change-point detector on graph events。
  - Temporal view reliability estimator。
  - Drift-aware positive pair selection。
  - Time-conditioned negative sampling。
  - Temporal consistency vs change contrastive objectives。
- **Required Datasets**：DDGCL / DySubC / CLDG 使用的动态数据集；可补 Wikipedia、Reddit temporal interactions、MOOC、Enron、UCI、LastFM、CollegeMsg 等常用 temporal graph。
- **Required Baselines**：DDGCL、DySubC、CLDG、DGI/GRACE 静态扩展、TGAT/TGN/DySAT/EvolveGCN 等动态图 baseline。
- **Key Experiments**：
  - 主结果：temporal link prediction、dynamic node classification。
  - 消融：无 change detector、固定时间窗口、只用相邻正样本、只用 timespan view。
  - 鲁棒性：人为插入突变事件、改变时间窗口长度、周期性子集分析。
  - 机制分析：高 drift 时间段的 positive pair 权重是否下降；变化点附近性能。
  - 可扩展性：事件数增加时训练时间和内存。
- **Key Risk**：动态图实验协议复杂，若数据集没有明显非平稳性，方法优势不明显。
- **Novelty Risk**：中等。`DDGCL`、`DySubC`、`CLDG` 已覆盖 dynamic contrastive views；新点必须是 non-stationary reliability，而不是又一种 temporal view。
- **Incrementality Risk**：中等。如果只是换时间窗口采样，容易 incremental；如果能检测并解释 temporal false positives，则较强。
- **Top-conference Potential**：4
- **是否已有高度相似工作**：部分相似。`CLDG` 有 timespan view 和 temporal translation invariance，`DySubC` 有 temporal subgraph contrast，`DDGCL` 有 dynamic debiasing；但非平稳可靠性未系统解决。
- **是否只是换 augmentation / 换 loss**：有风险。必须围绕 temporal reliability 和 change point。
- **是否能形成清楚的方法贡献**：能，尤其是 change-aware positive pair selection。
- **是否有可验证的 failure mode**：有。突变时间段相邻 view alignment 会错误拉近不同语义状态。
- **是否有机会做理论或机制分析**：可以分析 temporal drift 与 positive-pair noise。
- **是否适合短期启动实验**：中等。需要动态数据处理和协议复现。
- **强 baseline 攻击点**：CLDG、DySubC、DDGCL、TGN/DySAT。如果不能比 CLDG 强，风险大。
- **相关论文与未解决点**：
  - `DDGCL`：考虑动态自监督和 debiased sampling，但未明确处理非平稳突变的 positive reliability。
  - `DySubC`：temporal subgraph contrast，但子图窗口选择仍可能带来 bias。
  - `CLDG`：timespan view 与 temporal translation invariance，但 invariance 假设在突变下可能失败。
  - `BGRL` / `GRACE`：静态视图方法，不能直接处理时间漂移。
  - `GCC`：子图采样思想可借鉴，但非 temporal drift。
- **为什么不是简单 incremental**：核心不是新增 temporal augmentation，而是把时间非平稳性作为正样本噪声来源。
- **最可能的核心创新点**：change-aware temporal view reliability and drift-conditioned contrastive learning。
- **Evidence**：`DDGCL` Evidence: dynamic graph SSL/debiased sampling；`DySubC` Evidence: temporal subgraph contrast；`CLDG` Evidence: timespan view/temporal invariance；`method_taxonomy.md` 5.6 Temporal Graph 与 6.5 Robustness。

## Gap 10: Cross-domain View Reliability as a General GCL Principle

- **Gap Name**：Cross-domain View Reliability as a General GCL Principle
- **Target Scenario**：通用 GCL、跨图类型迁移、foundation-style graph pretraining
- **Existing Assumption**：不同领域分别设计自己的增强：citation graph 用 edge dropping/feature masking，推荐图用 dropout/noise/SVD，分子图用 2D-3D，动态图用 timespan，graph-text 用 paired text；这些方法默认领域增强是可靠的。
- **Why This Assumption May Fail**：每个领域的增强都有不同失效机制：异配图删边破坏角色，推荐图增强放大 popularity，分子增强破坏化学语义，动态图时间视图遇到漂移，graph-text pair 出现模态冲突。
- **Failure Mode**：semantic inconsistency、domain-specific false positive view、false negative pair、transferability issue、spurious invariance。
- **Possible Method**：提出跨领域的 view reliability framework。不是给每个领域手写增强，而是定义统一的 reliability variables：structural reliability、attribute reliability、temporal reliability、text reliability、domain prior reliability。不同场景实例化不同证据源。
- **Possible Modules**：
  - Unified reliability scoring API：输入 view pair 和 domain evidence，输出 positive/negative reliability。
  - Domain adapters：heterophily adapter、recommendation bias adapter、molecular validity adapter、temporal drift adapter、graph-text conflict adapter。
  - Reliability-conditioned contrastive objective。
  - Generalization diagnostics across graph types。
  - Meta-learning or calibration module for new graph domains。
- **Required Datasets**：至少覆盖三类图：同配/异配节点图，推荐图，分子图或 graph-text；更完整可加动态图。具体可用 Cora/Citeseer/PubMed、Chameleon/Squirrel/Actor、Gowalla/Yelp/Amazon-Book、MoleculeNet/GEOM、OGB-Arxiv text。
- **Required Baselines**：每个领域强 baseline 都要比较：GRACE、GCA、BGRL、CCA-SSG、GraphMAE/GraphMAE2；推荐 SGL、SimGCL、NCL、LightGCL；分子 GraphCL、GraphMVP、Mole-BERT；异配 GREET、H2GCN、LINKX；graph-text GraphCLIP/MoleculeSTM。
- **Key Experiments**：
  - 主结果：至少三种 graph type 上的统一框架是否优于领域强 baseline 或接近强 baseline。
  - 消融：只用统一 reliability、加 domain adapter、去掉某类 evidence。
  - 迁移：在一种图类型学 reliability calibration，迁移到另一种图类型。
  - 机制分析：不同领域的 low-reliability views 是否对应已知失效机制。
  - 反例分析：在哪些领域统一框架不如专用方法。
- **Key Risk**：范围过大，容易做成系统拼盘；同时打赢多个领域强 baseline 难度很高。
- **Novelty Risk**：中等。单个模块可能都被已有工作覆盖，但统一 reliability principle 可能有新意。
- **Incrementality Risk**：中等偏高。如果没有统一理论或统一接口，只是多个领域技巧组合，会被认为拼接。
- **Top-conference Potential**：3
- **是否已有高度相似工作**：没有完全相同，但所有子模块都有相关工作，因此容易被拆解攻击。
- **是否只是换 augmentation / 换 loss**：风险高。必须有统一变量和跨领域机制验证。
- **是否能形成清楚的方法贡献**：可以，但需要非常聚焦，例如只覆盖 3 个代表性 domain。
- **是否有可验证的 failure mode**：有，但每个 domain 的 failure mode 不同，需要统一度量。
- **是否有机会做理论或机制分析**：有。可把 view reliability 定义为 latent semantic preservation probability。
- **是否适合短期启动实验**：不太适合一次性全做。适合作为长期主线，短期应先从 Gap 1/2/7 之一切入。
- **强 baseline 攻击点**：所有领域专用强方法都会攻击它：GCA、BGRL、GraphMAE2、LightGCL、GraphMVP、GREET、GraphCLIP。
- **相关论文与未解决点**：
  - `GraphCL` / `GCA` / `AD-GCL` / `JOAO`：通用或自动增强，但跨领域可靠性未统一。
  - `SGL` / `SimGCL` / `LightGCL`：推荐专用，不能解释分子或异配图。
  - `GraphMVP` / `Mole-BERT`：分子专用，不能解释推荐和异配。
  - `CLDG` / `DySubC`：动态图专用，未统一到其他 graph type。
  - `GraphCLIP` / `MoleculeSTM`：graph-text 专用，未处理所有图增强可靠性。
- **为什么不是简单 incremental**：只有在提出统一 reliability theory / objective，并跨领域验证时才不是 incremental；否则非常像拼盘。
- **最可能的核心创新点**：domain-conditioned view reliability as a general abstraction for GCL。
- **Evidence**：`method_taxonomy.md` 总体判断、1.7 Domain-Specific Augmentation、6.7 Graph Foundation Model Pretraining；文献表中 `GraphCL`、`GCA`、`SGL`、`GraphMVP`、`CLDG`、`GraphCLIP` 的 View Generation 和 Possible Gap 字段。

## 总结性排序

| Rank | Gap | Top-conference Potential | Incrementality Risk | Short-term Start | 更适合 Venue |
|---:|---|---:|---|---|---|
| 1 | Heterophily-aware Semantic-Preserving Augmentation | 5 | 中 | 适合 | NeurIPS / ICLR / ICML；KDD / WWW |
| 2 | Reliability-aware False Negative and False Positive Correction | 5 | 中偏高 | 适合 | ICML / NeurIPS / ICLR；KDD / WWW |
| 3 | Graph-Text Conflict-aware Contrastive Pretraining | 5 | 中 | 中等 | NeurIPS / ICLR / ICML；KDD / WWW |
| 4 | Contrastive-Generative Reliability Learning | 4 | 高 | 适合 prototype | ICLR / NeurIPS；KDD / WWW |
| 5 | Negative-free GCL under Heterophily and Sparse Graphs | 4 | 中偏高 | 中等 | ICLR / ICML / AAAI |
| 6 | Mini-batch Friendly Scalable GCL with Controlled Negative Noise | 4 | 中 | 中等 | KDD / WWW / NeurIPS / TKDE |
| 7 | Non-stationary Temporal View Reliability for Dynamic GCL | 4 | 中 | 中等 | KDD / WWW / ICDE / TKDE |
| 8 | Molecular Semantic-valid Augmentation beyond 2D Random Perturbation | 4 | 中 | 中等 | ICLR / NeurIPS；KDD / WWW |
| 9 | Recommendation GCL Beyond Noise Regularization | 3 | 高 | 适合 | KDD / WWW / SIGIR / TKDE |
| 10 | Cross-domain View Reliability as a General GCL Principle | 3 | 中偏高 | 不建议直接全做 | NeurIPS / ICLR if narrowed；TKDE survey-style extension |

## 最不建议直接启动的方向

- **Recommendation GCL Beyond Noise Regularization**：不是不能做，而是推荐 GCL 强 baseline 太密集，必须有 bias / popularity / exposure 的机制证据，否则容易被 `SimGCL` 和 `LightGCL` 打成小改。
- **Cross-domain View Reliability as a General GCL Principle**：长期叙事好，但短期范围太大。建议先从 Gap 1、Gap 2 或 Gap 7 做出一个强核心，再把它扩展成统一框架。
- **普通 GraphMAE + GCL 混合**：如果没有 reliability gate，只是 loss 相加，增量风险最高。
