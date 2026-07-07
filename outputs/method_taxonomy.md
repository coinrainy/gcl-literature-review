# Graph Contrastive Learning 方法分类图谱

本文档基于 `outputs/gcl_literature_table.csv` 中 57 篇论文整理，用于支持方法型 GCL / 图自监督学习论文选题。整体判断遵循一个原则：不要只看某个模块是否新，而要看它是否改变了 view、positive pair、negative sampling、objective 或 graph type 中的关键假设。

## 总体判断

### 已经拥挤的方向

- 随机增强式 node-level GCL：`GRACE`、`GCA`、`BGRL`、`CCA-SSG`、`AFGRL` 等已经覆盖 edge dropping、feature masking、无负样本、去冗余和 bootstrap。仅替换增强概率或加一个轻量权重模块，容易被认为 incremental。
- graph-level random augmentation：`GraphCL`、`JOAO`、`AD-GCL` 已经把手工增强、自动增强、对抗增强都做过。若仍停留在 TU datasets / MoleculeNet 上调增强组合，创新空间偏小。
- 推荐图 GCL：`SGL`、`SimGCL`、`NCL`、`LightGCL` 已经形成很强链条。只在 LightGCN 上换一个噪声或邻居选择策略，风险较高。
- GraphMAE 类 masked feature reconstruction：`GraphMAE`、`GraphMAE2`、`MaskGAE` 已经覆盖 attribute mask、decoding enhancement、edge/structure mask。简单改 mask ratio 或 decoder 结构容易显得增量。

### 仍有方法创新空间的方向

- heterophily graph SSL：`GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN` 已经覆盖 edge heterophily discriminating、graph-filter / spectral views、heterogeneous homophily-aware edge dropping、macro-micro message passing 和 false-positive local structure reconstruction；`The Heterophilic Graph Learning Handbook`、`Re-evaluating the Advancements of Heterophilic Graph Learning`、`H2GB` 还抬高了评估门槛。后续创新点应从“再设计一种异配增强”收窄到 view reliability、positive reliability calibration 和 pair reliability。
- false negative / class collision：`GDCL`、`ProGCL`、`CGC` 已经提出去偏和 hard negative 处理，`IFL-GCL` 进一步把 GCL 解释为 positive-unlabeled learning 并从 InfoNCE 中挖掘语义正样本；剩余空间是正负样本双侧、可解释、可验证、跨图类型的 pair reliability calibration。
- scalable + negative-free + heterophily：`BGRL` 解决大规模负样本成本，`LINKX` 暴露大规模异配图挑战，但二者尚未充分结合。
- graph-text / graph foundation model pretraining：`GraphGPT`、`MoleculeSTM`、`GraphCLIP`、`GAugLLM`、`GCL-OT` 以及 `Graph Foundation Models: A Comprehensive Survey`、`Large Language Models Meet Text-Attributed Graphs` 说明图-文本对齐、LLM-based TAG augmentation 和 heterophilic TAG alignment 都很活跃；后续创新点应收窄到 structure-text conflict、cross-modal pair reliability 和 conflict-aware soft labels，而不是再做泛泛的 LLM 增强。
- dynamic graph contrastive learning：`DDGCL`、`DySubC`、`CLDG` 说明 temporal view 可行，但非平稳、突变、时间因果和 false negative 的关系仍不清楚。

### 顶会/顶刊方法型潜力更高的切入

- 异配图上的语义保持增强：`GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN` 已经部分覆盖该方向；更有价值的切入是估计增强视图、正样本对和结构推断是否可靠，而不是只做类型自适应增强。
- 不确定性感知的 false negative correction：不要只依赖聚类或相似度，结合结构证据、时间证据、文本证据或多视图一致性估计负样本可信度。
- 大规模图上的无负样本 + 可解释防坍塌：连接 `BGRL` / `CCA-SSG` 的效率优势与 heterophily / recommendation / temporal graph 的真实任务。
- graph-text contrastive pretraining 的冲突建模：在 `GAugLLM` 已覆盖 LLM-based TAG augmentation、`GCL-OT` 已覆盖 heterophilic TAG 的 OT-based structure-text alignment 后，重点应转向文本相似但结构不同、结构相似但文本冲突时如何定义正负样本、软标签和目标函数。
- hybrid contrastive-generative objective：不是简单把 InfoNCE 和 reconstruction 相加，而是让生成目标服务于 view reliability 或 negative reliability。

## 1. 按 View Generation 分类

### 1.1 Random Edge Dropping

- 代表论文：`GRACE`、`GraphCL`、`GCA`、`BGRL`、`SGL`。
- 核心思想：随机删除边构造结构扰动视图，让同一节点或同一图在不同拓扑扰动下保持表示一致。
- 共同假设：被删除的边大多是冗余或噪声边，删除少量边不会改变语义标签。
- 优势：简单、通用、易复现，是 node-level 和 graph-level GCL 的标准起点。
- 局限：在异配图、分子图、推荐图中，某些边具有强语义或化学/交互含义，随机删除可能破坏标签相关结构。
- 可能的 method-level gap：推断：边删除应从随机扰动走向语义约束和类型感知，例如区分同配边、异配边、桥接边、时间关键边。
- 与方法型选题的关系：如果只提出新的删边概率函数，增量风险很高；若能证明“哪些边不能删”并在异配/动态图/推荐图上验证，潜力明显更高。

### 1.2 Feature Masking

- 代表论文：`GRACE`、`GCA`、`GraphCL`、`BGRL`、`GraphMAE`。
- 核心思想：遮蔽或扰动节点/图属性，要求模型从剩余结构和属性中恢复一致表示或重构被遮蔽特征。
- 共同假设：部分特征缺失不改变语义，邻域上下文足以补全关键属性。
- 优势：适合属性图，和 masked modeling 自然连接；实现成本低。
- 局限：当节点特征本身就是主要标签证据时，随机 mask 可能制造无意义难度；异配图中邻居特征不一定能补全目标节点。
- 可能的 method-level gap：推断：mask 策略应与特征语义、节点角色和图同配/异配程度联合建模。
- 与方法型选题的关系：单纯改 mask ratio 容易 incremental；把 feature masking 和 heterophily-aware context 或 graph-text evidence 结合更有空间。

### 1.3 Subgraph Sampling

- 代表论文：`GCC`、`GraphCL`、`GraphLoG`、`DySubC`、`GraphSAGE`。
- 核心思想：通过 random walk、ego-network、temporal subgraph 或局部子图采样构造上下文视图。
- 共同假设：局部子图包含可迁移结构模式或时间演化模式，同一 anchor 附近子图可作为语义相关视图。
- 优势：比全图增强更适合大规模图；天然支持跨图预训练和 temporal graph。
- 局限：子图边界、采样半径和时间窗口强依赖超参数；同一 anchor 子图不一定语义一致。
- 可能的 method-level gap：推断：学习式选择 informative subgraph，避免固定 random walk / ego sampling 对结构偏置过强。
- 与方法型选题的关系：跨图预训练、动态图和大规模图中仍有潜力；若只换 sampling heuristic，贡献可能偏弱。

### 1.4 Diffusion-Based Views

- 代表论文：`MVGRL`。
- 核心思想：用 graph diffusion 生成全局平滑视图，与原始 adjacency view 做跨视图对比。
- 共同假设：扩散视图能保留并补充原图语义，平滑后的长程信息对表示学习有益。
- 优势：能够引入高阶邻域和全局结构，适合早期 citation graph setting。
- 局限：diffusion 预处理在大图上成本高，并且默认同配平滑有效；异配图上可能把不同类别节点混合得更严重。
- 可能的 method-level gap：推断：构造非同配友好的 diffusion，例如 signed diffusion、role-aware diffusion 或 edge-type-aware diffusion。
- 与方法型选题的关系：传统 diffusion-view 已不新；如果能解决 heterophily 或 scalability，则有较强方法价值。

### 1.5 Adaptive / Learnable Augmentation

- 代表论文：`GCA`、`JOAO`、`AD-GCL`。
- 核心思想：不再均匀随机增强，而是根据中心性、特征重要性、自动增强分布或对抗式增强器选择视图。
- 共同假设：存在可估计的“重要结构/属性”，增强应尽量扰动非关键部分或生成更有挑战的视图。
- 优势：直接回应 random augmentation 的语义破坏问题，是 GCL 方法创新的核心路线之一。
- 局限：重要性估计常为启发式；对抗增强可能追求困难度而牺牲语义保持；自动增强搜索空间仍由人工定义。
- 可能的 method-level gap：推断：从“结构重要性”升级为“任务语义重要性”或“图类型条件化增强”。
- 与方法型选题的关系：方向已经拥挤，但如果与 heterophily、temporal graph、graph-text conflict 或 false negative reliability 结合，仍有顶会潜力。

### 1.6 Semantic-Preserving Augmentation

- 代表论文：`GraphCL`、`GCA`、`AD-GCL`、`GraphMVP`、`MoleculeSTM`。
- 核心思想：构造两个不同但语义一致的视图，例如随机图增强、2D-3D 分子视图、结构-文本视图。
- 共同假设：正视图共享同一底层语义，模型应忽略视图特有噪声。
- 优势：这是 GCL 的核心归纳偏置；如果语义保持成立，对下游泛化很有效。
- 局限：语义保持通常是假设而非被验证；在异配图、推荐图、动态图中，什么叫“语义不变”并不清楚。
- 可能的 method-level gap：推断：显式估计 view semantic reliability，并让低可靠正对降低权重或转为不确定对。
- 与方法型选题的关系：非常关键。直接围绕“语义保持假设失效”提出方法，通常比改 encoder 更像方法型贡献。

### 1.7 Domain-Specific Augmentation

- 代表论文：`SGL`、`SimGCL`、`NCL`、`LightGCL`、`GraphMVP`、`Mole-BERT`、`CLDG`。
- 核心思想：根据领域构造视图，如推荐图的 edge/node dropout、embedding noise、SVD view，分子图的 2D-3D view，动态图的 timespan view。
- 共同假设：领域先验能定义更可靠的正样本和增强视图。
- 优势：通常比通用随机增强更有效，容易产生清晰动机和实验收益。
- 局限：跨领域泛化弱，方法可能被审稿人认为只是“把 GCL 套到某领域”。
- 可能的 method-level gap：推断：提炼跨领域通用原则，例如“视图可靠性估计”“结构-语义冲突检测”，而不是只做领域工程。
- 与方法型选题的关系：推荐、分子方向较拥挤；动态图、graph-text、异配图的领域特定增强仍有空间。

## 2. 按 Contrastive Granularity 分类

### 2.1 Node-Node

- 代表论文：`GRACE`、`GCA`、`BGRL`、`CCA-SSG`、`AFGRL`、`GREET`。
- 核心思想：同一节点在不同视图中的表示作为正对，其他节点或其他视图作为负对或无需负样本。
- 共同假设：节点身份跨视图不变，视图扰动不会改变节点语义。
- 优势：适合 node classification，是 GCL 最成熟的粒度。
- 局限：同类节点可能被当作负样本；异配图中邻域扰动对节点语义影响更复杂。
- 可能的 method-level gap：推断：从 identity-based positive pair 转向 uncertainty-aware semantic positive pair。
- 与方法型选题的关系：非常拥挤。除非切入 heterophily、false negative、large-scale 或 graph-text，否则普通 node-node GCL 增量风险高。

### 2.2 Graph-Graph

- 代表论文：`GraphCL`、`JOAO`、`AD-GCL`、`InfoGraph`、`GraphLoG`。
- 核心思想：同一图的两个增强视图或同一语义图实例形成正对，用于 graph classification 和 molecule pretraining。
- 共同假设：图增强不改变图标签，图级读出能捕捉稳定语义。
- 优势：适合分子图和 TU datasets，和预训练/迁移结合自然。
- 局限：图级 benchmark 常规模较小，增强是否语义保持尤其在分子中很敏感。
- 可能的 method-level gap：推断：面向 graph-level 的因果子结构保持增强，避免扰动标签决定性 motif。
- 与方法型选题的关系：GraphCL 系列已很成熟，若只是新增增强算子容易 incremental；与因果 motif、3D 几何或文本解释结合更有潜力。

### 2.3 Node-Graph

- 代表论文：`DGI`、`MVGRL`、`InfoGraph`。
- 核心思想：最大化局部节点/patch 表示与全局 summary 或 graph representation 的一致性。
- 共同假设：全局 summary 能代表图级语义，局部和全局信息互补。
- 优势：为早期 GCL 提供互信息最大化范式，结构清晰。
- 局限：global summary 可能过粗，容易忽视多社区、多角色或异配结构。
- 可能的 method-level gap：推断：用多原型、多尺度或区域自适应 summary 替代单一全局 summary。
- 与方法型选题的关系：传统 DGI-style 方法已旧；若能解决 heterophily / large graph 上 summary 过度平均问题，仍可形成新贡献。

### 2.4 Subgraph-Graph

- 代表论文：`GCC`、`InfoGraph`、`GraphLoG`、`DySubC`。
- 核心思想：将子图、patch 或 temporal subgraph 与图级/上下文表示对齐，学习局部到全局的结构语义。
- 共同假设：子图能代表图的关键语义片段或可迁移结构模式。
- 优势：有利于预训练、跨图迁移和动态图建模。
- 局限：子图采样质量决定上限；随机子图可能包含无关或误导信息。
- 可能的 method-level gap：推断：学习选择“任务相关子图”或“语义稳定子图”，并量化子图正样本可靠性。
- 与方法型选题的关系：比单纯 node-node 更有空间，尤其适合构建可解释方法或大规模预训练。

### 2.5 Cluster / Prototype-Level

- 代表论文：`GraphLoG`、`GDCL`、`NCL`。
- 核心思想：使用聚类、原型或语义邻居作为中间粒度，缓解 instance-level 对比过细的问题。
- 共同假设：数据中存在稳定簇结构，簇或原型能近似语义类别。
- 优势：有助于缓解 false negative 和捕捉更高层语义。
- 局限：早期聚类不稳定会放大错误；簇数和原型更新策略敏感。
- 可能的 method-level gap：推断：引入不确定性或多粒度原型，避免硬聚类导致错误传播。
- 与方法型选题的关系：中等拥挤但仍有潜力，尤其可与 false negative correction 或 graph foundation model 对齐结合。

### 2.6 Graph-Text

- 代表论文：`MoleculeSTM`、`GraphGPT`、`GraphCLIP`、`GAugLLM`、`GCL-OT`；survey 包括 `Graph Foundation Models: A Comprehensive Survey`、`Large Language Models Meet Text-Attributed Graphs`。
- 核心思想：将图结构表示和文本表示映射到共同空间，构造 molecule-text、node-text、TAG augmented views 或 graph-instruction 正对。
- 共同假设：文本描述、LLM 增强文本和图结构共享底层语义。
- 优势：直接连接图基础模型和 LLM，具备迁移、解释和零样本潜力。
- 局限：`GAugLLM` 已经覆盖 LLM-based TAG feature / edge augmentation，`GCL-OT` 已经覆盖 heterophilic TAG 的 optimal-transport structure-text alignment；但真实文本可能噪声大、与结构证据冲突，简单 CLIP-style in-batch negatives 和 soft alignment 仍可能存在语义碰撞。
- 可能的 method-level gap：推断：研究 graph-text conflict-aware contrastive learning 和 pair reliability，例如文本相似但结构相反、结构相似但文本冲突、LLM 生成语义与结构证据冲突时如何处理。
- 与方法型选题的关系：高潜力方向。若能从 GCL 理论或机制上解决图-文本正负样本可靠性，顶会/顶刊方法潜力较强。

## 3. 按 Objective 分类

### 3.1 InfoNCE-Based

- 代表论文：`GRACE`、`GraphCL`、`GCC`、`GCA`、`JOAO`、`SGL`、`NCL`、`LightGCL`。
- 核心思想：拉近正样本对，推远负样本对，常用 batch negatives。
- 共同假设：正样本语义一致，负样本语义不同。
- 优势：强、稳定、可扩展到多领域，是 GCL 主流 objective。
- 局限：false negative / class collision 是根本问题；大 batch 或全图负样本成本高。
- 可能的 method-level gap：推断：将 InfoNCE 从“所有负样本同等可信”改为“负样本可信度连续建模”。
- 与方法型选题的关系：单纯换 InfoNCE 变体风险高；结合 false negative、domain shift、graph-text conflict 更有价值。

### 3.2 Mutual Information Maximization

- 代表论文：`DGI`、`MVGRL`、`InfoGraph`。
- 核心思想：用 JSD 等估计器最大化局部-全局或跨视图互信息。
- 共同假设：互信息高的表示保留更多任务相关语义。
- 优势：理论动机清楚，是早期 GCL 的范式基础。
- 局限：MI 估计不一定对应下游语义；global summary 容易过粗。
- 可能的 method-level gap：推断：从粗粒度 MI 转向条件互信息或语义受控 MI，避免最大化噪声相关性。
- 与方法型选题的关系：作为主线略旧；作为理论解释或辅助目标仍有价值。

### 3.3 Bootstrap / Negative-Free

- 代表论文：`BGRL`、`AFGRL`、`SelfGNN`。
- 核心思想：用 online/target network、stop-gradient、predictor 或正样本选择实现无负样本对齐。
- 共同假设：网络结构、EMA、predictor 或正样本机制足以防止坍塌。
- 优势：避免负样本成本和 false negative，适合大规模图。
- 局限：防坍塌机制在图上的理论仍不充分；仍依赖增强或正样本可靠性。
- 可能的 method-level gap：推断：解释并控制 heterophily / temporal graph 中 negative-free 目标的坍塌风险。
- 与方法型选题的关系：有潜力，但普通 BYOL-style 图改版已拥挤；需要新的图结构机制或理论。

### 3.4 Redundancy Reduction

- 代表论文：`CCA-SSG`。
- 核心思想：最大化两视图相关性，同时去除表示维度冗余，避免显式负样本。
- 共同假设：去相关后的共享因素更接近任务语义。
- 优势：避免负样本，同时具备较清晰的 CCA 理论动机。
- 局限：去冗余不总是有益，某些下游任务可能需要冗余或相关特征。
- 可能的 method-level gap：推断：研究结构条件化 redundancy reduction，让不同图区域采用不同去冗余强度。
- 与方法型选题的关系：方向不算完全拥挤，但单纯套 Barlow Twins/CCA 风格目标风险中等；与异配图或 foundation model 表征分析结合更强。

### 3.5 Debiased Contrastive Objective

- 代表论文：`GDCL`、`ProGCL`、`CGC`、`DDGCL`。
- 核心思想：识别或降低 false negative、hard negative 误用、动态图采样偏差对对比学习的影响。
- 共同假设：负样本并非同等可信，可以通过聚类、概率、反事实或时间机制估计其可靠性。
- 优势：直指 InfoNCE 的核心缺陷，方法型问题明确。
- 局限：可靠性估计本身可能不准；没有标签时很难验证 false negative 是否真实。
- 可能的 method-level gap：推断：多证据融合的 negative reliability estimation，例如结构、文本、时间和模型不确定性共同判断。
- 与方法型选题的关系：高潜力方向，尤其适合和异配图、graph-text、temporal graph 结合。

### 3.6 Reconstruction / Masked Modeling

- 代表论文：`VGAE`、`GraphMAE`、`GraphMAE2`、`MaskGAE`、`GROVER`。
- 核心思想：遮蔽属性、边或结构，再通过 encoder-decoder 重构目标信息。
- 共同假设：被遮蔽信息可由上下文预测，重构能力能迁移到下游表示。
- 优势：不需要负样本，避免 class collision；与 Transformer / foundation model 预训练兼容。
- 局限：重构表面特征或邻接不一定等于学习语义；mask 策略决定任务质量。
- 可能的 method-level gap：推断：让 masked modeling 预测“语义可靠性”或“视图有效性”，而不是只重构原始特征/边。
- 与方法型选题的关系：GraphMAE 主线已拥挤，但与 GCL 的可靠性、异配图或图-文本预训练结合仍有空间。

### 3.7 Hybrid Contrastive-Generative Objective

- 代表论文：`GraphMVP`、`Mole-BERT`、`Strategies for Pre-training GNNs`。
- 核心思想：同时使用对比对齐和生成/预测任务，让模型既学习不变性又保留可恢复信息。
- 共同假设：对比目标和生成目标互补，一个提供语义对齐，一个提供细节保持。
- 优势：适合复杂领域，如分子 2D-3D、多任务预训练和 graph-text 对齐。
- 局限：简单加权多个 loss 容易变成工程组合，缺少清晰机制。
- 可能的 method-level gap：推断：让生成目标动态校准对比样本可靠性，例如重构失败的视图降低正样本权重。
- 与方法型选题的关系：有潜力，但必须解释为什么 hybrid 不是 loss 拼接。

## 4. 按 Negative Sampling 分类

### 4.1 Explicit Negative Samples

- 代表论文：`DGI`、`MVGRL`、`InfoGraph`、`GraphSAGE`。
- 核心思想：通过 corruption、随机游走负节点或其他图实例构造负样本。
- 共同假设：人工构造的负样本与 anchor 语义不同。
- 优势：训练信号明确，早期方法稳定。
- 局限：负样本可能太简单，也可能包含 false negative。
- 可能的 method-level gap：推断：从显式负样本转为带置信度的负样本池。
- 与方法型选题的关系：作为基础组件可以保留，但单独创新空间有限。

### 4.2 In-Batch Negatives

- 代表论文：`GRACE`、`GraphCL`、`GCC`、`SGL`、`LightGCL`。
- 核心思想：batch 内其他节点/图/用户物品作为负样本。
- 共同假设：batch 中不同实例语义不同。
- 优势：实现简单，和 InfoNCE 配合高效。
- 局限：batch 越大 false negative 可能越多；推荐图和 graph-text 中语义碰撞尤其明显。
- 可能的 method-level gap：推断：构造 batch-aware semantic collision detector。
- 与方法型选题的关系：负样本可靠性仍是高价值问题，但“换 batch 采样方式”本身容易显得小。

### 4.3 Hard Negatives

- 代表论文：`ProGCL`、`CGC`。
- 核心思想：选择表示相似但应为负的样本，让模型学习更细粒度边界。
- 共同假设：困难负样本包含更强监督信号。
- 优势：能提升判别性，问题定义清楚。
- 局限：图中 hard negatives 很可能是同类节点或语义近邻。
- 可能的 method-level gap：推断：将 hard negative 分成 true-hard、false-hard 和 uncertain-hard 三类，而不是二分。
- 与方法型选题的关系：高潜力但需要扎实证据；没有可靠 false negative 识别会被质疑。

### 4.4 False Negative Correction

- 代表论文：`GDCL`、`ProGCL`、`CGC`、`DDGCL`。
- 核心思想：通过聚类、概率估计、反事实生成或时间去偏降低 false negative 损害。
- 共同假设：可以无监督估计样本语义相似度或负样本可信度。
- 优势：直面 GCL 的关键缺陷，容易形成方法型贡献。
- 局限：估计器可能循环依赖当前表示，早期训练不稳定。
- 可能的 method-level gap：推断：加入不确定性校准和跨视图一致性验证，防止错误去偏。
- 与方法型选题的关系：非常推荐。适合作为方法论文主问题，但需要强实验和可解释诊断。

### 4.5 Negative-Free Learning

- 代表论文：`BGRL`、`AFGRL`、`CCA-SSG`、`SelfGNN`、`GraphMAE`。
- 核心思想：不用显式负样本，通过 bootstrap、decorrelation 或 reconstruction 避免坍塌。
- 共同假设：目标函数或网络机制能提供足够约束。
- 优势：绕开 false negative 和大规模负样本成本。
- 局限：坍塌防止机制和语义学习机制常被混在一起，理论解释不足。
- 可能的 method-level gap：推断：建立图结构条件下的 negative-free 防坍塌诊断和自适应约束。
- 与方法型选题的关系：有潜力，但“又一个 BYOL on graphs”风险高；需要图特有新机制。

## 5. 按 Graph Type 分类

### 5.1 Homophilic Graph

- 代表论文：`DGI`、`GRACE`、`GCA`、`MVGRL`、`BGRL`、`GraphMAE`。
- 核心思想：利用邻域相似和随机增强语义保持学习节点表示。
- 共同假设：相邻节点或局部上下文大概率语义相似。
- 优势：benchmark 成熟，方法比较充分。
- 局限：方向拥挤，许多方法主要在 Cora/Citeseer/PubMed/Amazon/Coauthor 上验证。
- 可能的 method-level gap：推断：从同配默认 setting 转向同配-异配混合区域的自适应 SSL。
- 与方法型选题的关系：只在同配图上改方法很危险；应作为基础验证而非唯一贡献。

### 5.2 Heterophilic Graph

- 代表论文：`H2GCN`、`Geom-GCN`、`LINKX`、`GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN`；benchmark / survey 包括 `The Heterophilic Graph Learning Handbook`、`Re-evaluating the Advancements of Heterophilic Graph Learning`、`H2GB`。
- 核心思想：邻居不一定同类，应区分 ego、同配边、异配边、高阶关系、graph-filter views 或 metapath connection strength。
- 共同假设：异配图需要不同于平滑同配聚合的表示机制；增强视图也应区分同配/异配/不确定结构。
- 优势：能挑战 GCL 的语义保持和正样本假设，并暴露随机增强在低同配区域的失败模式。
- 局限：`GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN` 已经把普通 heterophily-aware augmentation、spectral/filter views、message passing 改造和 local positive 修正推得很密；若只换边分数、filter、metapath 权重或 self-loop 策略，容易 incremental。
- 可能的 method-level gap：推断：从 heterophily-aware augmentation 进一步收窄到 view reliability / positive reliability / pair reliability calibration，使低可靠视图、不确定正对或结构推断噪声被降权。
- 与方法型选题的关系：仍有潜力，但主张必须避开“又一个异配增强”，转向可验证的视图可靠性和正样本可靠性。

### 5.3 Molecular Graph

- 代表论文：`GraphCL`、`GROVER`、`GraphMVP`、`Mole-BERT`、`MoleculeSTM`。
- 核心思想：利用化学结构、2D/3D 几何、文本描述和 mask/token prediction 进行预训练。
- 共同假设：分子结构扰动、几何视图或文本描述能保留化学语义。
- 优势：领域先验丰富，下游任务明确，预训练价值高。
- 局限：分子增强必须满足化学有效性；方向已有强工作，普通增强很难新。
- 可能的 method-level gap：推断：将 2D、3D、文本和性质标签的不确定性统一进 view reliability。
- 与方法型选题的关系：潜力中高，但需要化学先验和强实验；不适合只做通用 GCL 小改动。

### 5.4 Recommendation Graph

- 代表论文：`SGL`、`SimGCL`、`NCL`、`LightGCL`。
- 核心思想：在 user-item 二部图上构造增强视图或全局视图，提升稀疏交互下的推荐表示。
- 共同假设：用户/物品在扰动交互图或 embedding noise 下偏好语义保持不变。
- 优势：工业相关强，指标清楚，稀疏性和噪声问题天然适合 SSL。
- 局限：LightGCN + contrastive 已很拥挤；很多增益可能来自正则化而非图语义。
- 可能的 method-level gap：推断：区分 GCL 增益来自去噪、uniformity、popularity debias 还是真实结构语义。
- 与方法型选题的关系：若定位为推荐专用方法，可以做；若目标是通用 GCL 方法，需抽象出跨图可用原则。

### 5.5 Knowledge Graph

- 代表论文：当前 57 篇表中没有专门 KG-GCL 论文。
- 核心思想：Unknown from current table。
- 共同假设：当前表无法确认。
- 优势：KG 有关系类型、路径、逻辑规则，理论上适合多视图和语义约束对比。
- 局限：本项目当前文献覆盖不足，不能据此下结论。
- 可能的 method-level gap：推断：补充 KG SSL / KG contrastive pretraining 文献，比较关系类型视图、路径视图和文本视图。
- 与方法型选题的关系：这是当前阅读工程的明显缺口；若你考虑 KG，需要另建种子列表。

### 5.6 Temporal Graph

- 代表论文：`DDGCL`、`DySubC`、`CLDG`。
- 核心思想：用 temporal context、temporal subgraph 或 timespan view 捕获动态图演化。
- 共同假设：相近或相关时间视图共享可对齐语义。
- 优势：比静态 GCL 更贴近真实图数据，方法空间未完全拥挤。
- 局限：非平稳、突变和时间窗口选择会破坏正样本假设。
- 可能的 method-level gap：推断：用时间因果和变化点检测约束动态图正负样本。
- 与方法型选题的关系：高潜力，但实验复杂度更高，需要严谨 temporal split。

### 5.7 Heterogeneous Graph

- 代表论文：`HGMS`、`H2GB`；相关 graph-text / TAG 工作包括 `GraphGPT`、`GraphCLIP`、`GAugLLM`、`GCL-OT`，但它们不等同于传统 heterogeneous information network。
- 核心思想：在多类型节点/边或 metapath views 中建模同配性与语义连接强度，避免低同配 metapath 产生低质量正样本。
- 共同假设：metapath connection strength 或多视图 self-expression 能近似节点语义同配，并帮助筛选更可靠的增强视图和样本对。
- 优势：多类型节点/边天然需要类型感知 view 和 positive pair。
- 局限：当前文献表已补入 `HGMS` 和 `H2GB`，但专门 HeteroGCL 仍覆盖有限；方法若只沿用 connection strength、self-expression 或 benchmark-driven 模型选择，容易被 HGMS/H2GB 攻击。
- 可能的 method-level gap：推断：补充更多 metapath-based SSL / heterogeneous GCL 文献后，研究 heterogeneous view reliability、metapath conflict 和 positive/negative reliability calibration。
- 与方法型选题的关系：有潜在空间，但短期更适合作为 Gap 1/2 的扩展验证场景，而不是单独宣称“异构图 GCL 尚无人覆盖”。

### 5.8 Large-Scale Graph

- 代表论文：`GraphSAGE`、`BGRL`、`LINKX`、`GraphMAE2`、`GCC`。
- 核心思想：通过采样、无负样本、简单模型或大规模预训练降低训练成本。
- 共同假设：可扩展机制不能显著损害表示语义。
- 优势：顶会很看重 scalability，尤其当方法不仅在小 citation graph 上有效。
- 局限：大规模实验成本高，许多 GCL 目标在全图负样本或 diffusion 上不可扩展。
- 可能的 method-level gap：推断：设计 sublinear 或 mini-batch friendly 的 GCL/GraphMAE 目标，同时处理 false negatives。
- 与方法型选题的关系：高潜力，但必须给出复杂度、内存、时间和大图实验。

## 6. 按研究问题分类

### 6.1 Augmentation Semantic Preservation

- 代表论文：`GraphCL`、`GCA`、`JOAO`、`AD-GCL`、`GraphMVP`、`GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN`、`GCL-OT`。
- 核心思想：构造既不同又不改变语义的视图。
- 共同假设：语义保持可以由增强类型、重要性估计或领域先验近似保证。
- 优势：是 GCL 最核心的问题，直接决定正样本质量。
- 局限：`GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN` 已经部分覆盖 heterophily-aware / homophily-aware augmentation 和 positive structure reconstruction，多数论文仍只通过下游结果间接证明语义保持，没有直接度量 view reliability；`GCL-OT` 进一步覆盖 heterophilic TAG alignment，使普通 TAG 增强空间更窄。
- 可能的 method-level gap：推断：建立可观测的 semantic preservation / view reliability score，并让训练动态使用它，尤其校准低可靠 positive pairs。
- 与方法型选题的关系：高潜力，但需要避免只做增强技巧堆叠；更好的主线是“增强可靠性如何被估计和验证”。

### 6.2 False Negative / Class Collision

- 代表论文：`GDCL`、`ProGCL`、`CGC`、`DDGCL`。
- 核心思想：识别本应相近却被当作负样本的节点/图，降低错误推远。
- 共同假设：false negative 可以通过聚类、概率、反事实或时间信息估计。
- 优势：问题明确、痛点强，和 InfoNCE 的基础假设直接相关。
- 局限：无标签条件下验证困难，估计错误会导致负样本退化。
- 可能的 method-level gap：推断：结合多视图一致性和不确定性校准构造 false negative detector。
- 与方法型选题的关系：非常适合方法型论文，尤其与 heterophily 或 graph-text 结合时更有新意。

### 6.3 Representation Collapse

- 代表论文：`BGRL`、`CCA-SSG`、`AFGRL`、`SelfGNN`。
- 核心思想：不用负样本时，通过 stop-gradient、EMA、predictor、decorrelation 或正样本选择避免所有表示相同。
- 共同假设：架构和目标中的非对称性或去冗余约束足以防坍塌。
- 优势：绕开负样本和大 batch 问题。
- 局限：图上为什么不坍塌仍缺少统一解释，尤其在异配图和稀疏图中。
- 可能的 method-level gap：推断：构建图结构条件下的 collapse diagnostics，如谱分布、社区混合度和同配率共同分析。
- 与方法型选题的关系：理论味较强，适合顶刊/顶会，但需要比经验方法更扎实的分析。

### 6.4 Scalability

- 代表论文：`GraphSAGE`、`GCC`、`BGRL`、`LINKX`、`GraphMAE2`。
- 核心思想：通过采样、跨图预训练、无负样本或轻量架构扩展到大图。
- 共同假设：局部采样或简化目标足以保留全图有用信息。
- 优势：大图实验能显著增强论文说服力。
- 局限：很多高质量 view generation 或 diffusion 方法在大图上不可承受。
- 可能的 method-level gap：推断：让 view generation 和 objective 都支持 mini-batch，同时显式控制 false negative。
- 与方法型选题的关系：高潜力但工程和实验门槛高；需要复杂度分析支撑。

### 6.5 Robustness

- 代表论文：`SGL`、`SimGCL`、`AD-GCL`、`GCA`、`GREET`。
- 核心思想：通过扰动、去噪、对抗增强或异配边判别提升表示对噪声和结构变化的鲁棒性。
- 共同假设：适当扰动可以逼迫模型学习稳定语义。
- 优势：和真实图噪声、推荐稀疏性、异配边混杂联系紧密。
- 局限：鲁棒性常被下游准确率间接衡量，缺少专门攻击/噪声协议。
- 可能的 method-level gap：推断：建立 GCL view-level robustness benchmark，区分结构噪声、属性噪声、时间噪声和语义冲突。
- 与方法型选题的关系：有潜力，尤其适合把增强语义保持和 robustness 统一。

### 6.6 Transferability

- 代表论文：`GCC`、`Strategies for Pre-training GNNs`、`GraphLoG`、`GraphMVP`、`Mole-BERT`、`MoleculeSTM`。
- 核心思想：通过预训练学习可迁移结构、语义或跨模态表示。
- 共同假设：预训练任务捕获的结构/语义因素能迁移到新任务或新数据集。
- 优势：更符合顶会/顶刊对方法泛化性的期待。
- 局限：负迁移普遍存在，预训练任务和下游任务不一致时效果不稳定。
- 可能的 method-level gap：推断：提出预训练任务和下游图类型之间的 compatibility estimator。
- 与方法型选题的关系：高潜力，但必须有跨数据集、跨图类型或跨任务证据。

### 6.7 Graph Foundation Model Pretraining

- 代表论文：`GraphGPT`、`GraphCLIP`、`MoleculeSTM`、`GraphMAE2`、`GAugLLM`、`GCL-OT`；survey 包括 `Graph Foundation Models: A Comprehensive Survey`、`Large Language Models Meet Text-Attributed Graphs`。
- 核心思想：将图结构、文本、LLM 增强、指令或大规模 masked pretraining 结合，构建更通用的图表示基础模型。
- 共同假设：图结构信息可以和语言/LLM 增强文本/大规模预训练目标对齐。
- 优势：方向新、影响面大，容易形成顶会/顶刊叙事。
- 局限：`GAugLLM` 已经覆盖 LLM-based TAG augmentation，`GCL-OT` 已经覆盖 heterophilic TAG 的 OT-based structure-text alignment，算力和数据门槛高，评估标准尚未完全稳定；容易被质疑只是套 LLM、CLIP、OT 或 prompt。
- 可能的 method-level gap：推断：设计 graph-specific conflict-aware alignment objective，解决结构语义与文本语义冲突，并显式校准 graph-text pair reliability / conflict-aware soft labels。
- 与方法型选题的关系：潜力很高，但需要聚焦 structure-text conflict / pair reliability 这类清晰机制问题，否则会变成系统工程论文。

## 选题建议

### 更建议优先探索

- Heterophily-aware GCL：在 `GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN` 已部分覆盖异配增强和结构修正后，围绕 view reliability / positive reliability calibration 建立方法。
- Reliability-aware negative sampling：在 `IFL-GCL` 已覆盖 PU-style semantic positives 后，为 false positive view、false negative pair、hard negative 和 graph-text conflict 建立双侧可靠性估计。
- Scalable negative-free GCL：面向大规模异配图或推荐图，给出复杂度优势和防坍塌分析。
- Hybrid contrastive-generative reliability learning：用 masked reconstruction 判断视图或负样本是否可靠，而不是简单相加两个 loss。
- Temporal semantic-preserving augmentation：把时间稳定性、变化点和非平稳性引入动态图 GCL。

### 容易被认为 Incremental 的选题

- 在 `GRACE` / `GraphCL` 上换一种随机 edge dropping 或 feature masking。
- 在 `GraphMAE` 上只改 mask ratio、decoder 层数或重构 loss。
- 在 `LightGCN` 推荐框架上只加一个新的 embedding noise。
- 在已有 `GCA` / `JOAO` / `AD-GCL` 之后再做无明确语义证明的增强选择器。
- 在 `GREET` / `HLCL` / `HGMS` / `PolyGCL` / `HeterGCL` / `M3P-GCL` / `ROSEN` 之后只换 heterophily score、graph filter、metapath 权重或 message passing 分支。
- 在 `GAugLLM` / `GCL-OT` 之后只换 LLM prompt、文本增强模板、edge modifier 阈值或普通 structure-text alignment loss。
- 只在 Cora/Citeseer/PubMed/Amazon/Coauthor 上报告提升，而没有异配、大规模或跨领域验证。

### 最值得形成论文主线的问题表述

> 现有 GCL 普遍假设增强视图语义保持、负样本语义相异、同配邻域可靠；但这些假设在异配图、动态图、推荐图和 graph-text 预训练中经常失效。考虑到 heterophily-aware augmentation / structure reconstruction 已被 `GREET`、`HLCL`、`HGMS`、`PolyGCL`、`HeterGCL`、`M3P-GCL`、`ROSEN` 部分覆盖，LLM-based TAG augmentation 和 heterophilic TAG alignment 已被 `GAugLLM`、`GCL-OT` 覆盖，一个更稳的方法型主线应显式建模“样本对可靠性”“视图语义可靠性”或“结构-文本冲突”，并让 view generation、negative sampling 和 objective 同时受该可靠性控制。
