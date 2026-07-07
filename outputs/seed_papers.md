# GCL 文献种子列表

本清单是第一批 Graph Contrastive Learning, GCL 与图自监督学习方法型论文阅读种子，共 42 篇。信息以论文页、arXiv、OpenReview、ACM/IEEE/NeurIPS/PMLR 页面和官方 GitHub 为准；未能确认的代码链接写为 `Unknown`。

## 1. 早期图自监督学习

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Variational Graph Auto-Encoders | 2016 | NIPS Workshop on Bayesian Deep Learning | https://arxiv.org/abs/1611.07308 | https://github.com/tkipf/gae | 早期将自编码器和 GCN 编码器结合用于无监督图表示学习，是 GraphMAE 类生成式路线的重要前史。 | High |
| Deep Graph Infomax | 2019 | ICLR | https://openreview.net/forum?id=rklz9iAcKQ | https://github.com/PetarV-/DGI | 提出局部节点/patch 表示与全图 summary 的互信息最大化，是后续 GCL 中 local-global contrast 的核心起点。 | High |
| Strategies for Pre-training Graph Neural Networks | 2020 | ICLR | https://openreview.net/forum?id=HJlWWJSFDH | https://github.com/snap-stanford/pretrain-gnns | 系统研究 node-level 与 graph-level 预训练策略，提出 context prediction、attribute masking、edge prediction 等任务，对方法型论文的预训练设计很关键。 | High |

## 2. 基础图对比学习

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Contrastive Multi-View Representation Learning on Graphs | 2020 | ICML | https://arxiv.org/abs/2006.05582 | https://github.com/kavehhassani/mvgrl | MVGRL 用邻接视图与 diffusion 视图做多视图对比，同时覆盖 node-level 和 graph-level，是理解 view design 的基础论文。 | High |
| GCC: Graph Contrastive Coding for Graph Neural Network Pre-Training | 2020 | KDD | https://dl.acm.org/doi/10.1145/3394486.3403168 | https://github.com/THUDM/GCC | 提出跨网络的子图实例判别预训练，强调结构模式可迁移性，是 GCL 走向预训练范式的重要工作。 | High |
| Deep Graph Contrastive Representation Learning | 2020 | ICML Workshop on Graph Representation Learning and Beyond | https://arxiv.org/abs/2006.04131 | https://github.com/CRIPAC-DIG/GRACE | GRACE 直接对齐两种扰动视图下的同一节点表示，形成了后续 node-level GCL 的标准范式。 | High |

## 3. node-level GCL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Simple Unsupervised Graph Representation Learning | 2022 | AAAI | https://ojs.aaai.org/index.php/AAAI/article/view/20748 | https://github.com/YujieMo/SUGRL | SUGRL 关注简单、高效的无监督节点表示学习，可作为 node-level GCL 简化路线和效率 baseline。 | Medium |
| Self-Supervised Graph Representation Learning via Global Context Prediction | 2020 | arXiv | https://arxiv.org/abs/2003.01604 | Unknown | 用全局上下文预测构造节点级自监督信号，适合对比 GCL 与 predictive SSL 的监督信号差异。 | Medium |

## 4. graph-level GCL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| InfoGraph: Unsupervised and Semi-supervised Graph-Level Representation Learning via Mutual Information Maximization | 2020 | ICLR | https://arxiv.org/abs/1908.01000 | https://github.com/sunfanyunn/InfoGraph | 将图级表示与多尺度子结构表示做互信息最大化，是 graph-level 表示学习和分子/社交图实验的经典基线。 | High |
| Self-supervised Graph-level Representation Learning with Local and Global Structure | 2021 | ICML | https://arxiv.org/abs/2106.04113 | https://github.com/DeepGraphLearning/GraphLoG | GraphLoG 同时建模图实例的局部相似和全局语义原型，对 graph-level 方法如何超越局部增强很有参考价值。 | Medium |

## 5. augmentation-based GCL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Graph Contrastive Learning with Augmentations | 2020 | NeurIPS | https://proceedings.neurips.cc/paper/2020/hash/3fe230348e9a12c13120749e3f9fa4cd-Abstract.html | https://github.com/Shen-Lab/GraphCL | GraphCL 系统研究 node dropping、edge perturbation、attribute masking、subgraph 等图增强，是 augmentation-based GCL 的核心起点。 | High |
| Adversarial Graph Augmentation to Improve Graph Contrastive Learning | 2021 | NeurIPS | https://arxiv.org/abs/2106.05819 | https://github.com/susheels/adgcl | AD-GCL 用可学习的对抗式边删除生成视图，直接回应随机增强可能保留冗余或破坏语义的问题。 | High |

## 6. adaptive augmentation GCL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Graph Contrastive Learning with Adaptive Augmentation | 2021 | WWW | https://arxiv.org/abs/2010.14945 | https://github.com/CRIPAC-DIG/GCA | GCA 根据结构中心性和属性重要性自适应调整拓扑/特征扰动，是 node-level adaptive augmentation 的代表。 | High |
| Graph Contrastive Learning Automated | 2021 | ICML | https://proceedings.mlr.press/v139/you21a.html | https://github.com/Shen-Lab/GraphCL_Automated | JOAO 用双层优化自动选择增强组合，提供了从手工增强到自动增强搜索的关键思路。 | High |

## 7. negative-free / redundancy-reduction GCL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| From Canonical Correlation Analysis to Self-supervised Graph Neural Networks | 2021 | NeurIPS | https://arxiv.org/abs/2106.12484 | https://github.com/hengruizhang98/CCA-SSG | CCA-SSG 去掉显式负样本并通过特征去相关防止坍塌，是 redundancy-reduction 目标在图上的代表。 | High |
| Augmentation-Free Self-Supervised Learning on Graphs | 2022 | AAAI | https://arxiv.org/abs/2112.02472 | https://github.com/Namkyeong/AFGRL | AFGRL 不依赖预设增强，通过局部结构与全局语义发现 alternative view，适合研究无增强 GCL。 | High |
| Self-supervised Graph Neural Networks without explicit negative sampling | 2021 | WWW Workshop | https://arxiv.org/abs/2103.14958 | https://github.com/zekarias-tilahun/SelfGNN | SelfGNN 探索不使用显式负样本的图自监督训练，并讨论 feature augmentation 与 batch normalization 的隐式对比效应。 | Medium |

## 8. false negative / debiased GCL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Graph Debiased Contrastive Learning with Joint Representation Clustering | 2021 | IJCAI | https://www.ijcai.org/proceedings/2021/473 | https://github.com/hzhao98/GDCL | GDCL 明确指出随机负采样会引入 false negative，并用联合聚类估计类别信息进行去偏。 | High |
| ProGCL: Rethinking Hard Negative Mining in Graph Contrastive Learning | 2022 | ICML | https://arxiv.org/abs/2110.02027 | https://github.com/junxia97/ProGCL | ProGCL 从 hard negative 中存在 false negative 的角度重新设计负样本权重，是负样本处理方向的高优先级论文。 | High |
| Generating Counterfactual Hard Negative Samples for Graph Contrastive Learning | 2023 | WWW | https://dl.acm.org/doi/10.1145/3543507.3583499 | Unknown | CGC 用反事实机制生成语义相异但相似度高的 hard negative，为 false negative 问题提供了生成式替代路线。 | Medium |

## 9. GraphMAE / masked graph autoencoder / 生成式图自监督

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| GraphMAE: Self-Supervised Masked Graph Autoencoders | 2022 | KDD | https://arxiv.org/abs/2205.10803 | https://github.com/THUDM/GraphMAE | GraphMAE 将 masked autoencoding 引入图 SSL，并强调特征重构和 scaled cosine error，是生成式图自监督的核心论文。 | High |
| GraphMAE2: A Decoding-Enhanced Masked Self-Supervised Graph Learner | 2023 | WWW | https://arxiv.org/abs/2304.04779 | https://github.com/THUDM/GraphMAE2 | GraphMAE2 通过 re-mask decoding 和 latent prediction 强化解码，且报告大规模 ogbn-Papers100M 结果，适合连接生成式 SSL 与大规模图。 | High |
| What's Behind the Mask: Understanding Masked Graph Modeling for Graph Autoencoders | 2023 | KDD | https://arxiv.org/abs/2205.10053 | https://github.com/EdisonLeeeee/MaskGAE | MaskGAE 从 masked graph modeling 角度分析边/结构遮蔽对 GAE 的作用，是理解生成式图 SSL 机制的重要补充。 | High |

## 10. heterophily graph learning / heterophily graph SSL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Beyond Homophily in Graph Neural Networks: Current Limitations and Effective Designs | 2020 | NeurIPS | https://arxiv.org/abs/2006.11468 | https://github.com/GemsLab/H2GCN | H2GCN 系统指出同配假设下 GNN 的局限，为评估 GCL 是否只适合 homophilous graph 提供基础。 | High |
| Geom-GCN: Geometric Graph Convolutional Networks | 2020 | ICLR | https://arxiv.org/abs/2002.05287 | https://github.com/graphdml-uiuc-jlu/geom-gcn | Geom-GCN 是早期面向 disassortative/heterophilous 图的代表方法，适合纳入异配图实验与 split 讨论。 | Medium |
| Large Scale Learning on Non-Homophilous Graphs: New Benchmarks and Strong Simple Methods | 2021 | NeurIPS | https://arxiv.org/abs/2110.14446 | https://github.com/CUAI/Non-Homophily-Large-Scale | LINKX 论文提供大规模异配图 benchmark，并指出 minibatching 在异配图上的退化，对可扩展异配 GCL 很关键。 | High |
| Beyond Smoothing: Unsupervised Graph Representation Learning with Edge Heterophily Discriminating | 2023 | AAAI | https://arxiv.org/abs/2211.14065 | https://github.com/yixinliu233/GREET | GREET 面向无监督异配图表示学习，区分同配边与异配边并做双通道对比，是 heterophily graph SSL 的直接相关工作。 | High |

## 11. scalable GCL / large-scale graph SSL

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Large-Scale Representation Learning on Graphs via Bootstrapping | 2022 | ICLR | https://arxiv.org/abs/2102.06514 | https://github.com/nerdslab/bgrl | BGRL 用 bootstrapping 避免负样本带来的二次复杂度，强调大规模图上的内存和训练效率。 | High |
| Inductive Representation Learning on Large Graphs | 2017 | NeurIPS | https://arxiv.org/abs/1706.02216 | https://github.com/williamleif/GraphSAGE | GraphSAGE 的无监督邻居采样/负采样训练是大规模图表示学习的基础，对后续 scalable GCL 的采样设计仍有参考价值。 | Medium |

## 12. graph foundation model / graph-text contrastive pretraining

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| GraphGPT: Graph Instruction Tuning for Large Language Models | 2024 | SIGIR | https://arxiv.org/abs/2310.13023 | https://github.com/HKUDS/GraphGPT | GraphGPT 将图结构知识与 LLM 指令调优结合，代表图基础模型从 GNN 预训练走向 LLM 对齐的方向。 | High |
| Multi-modal Molecule Structure-text Model for Text-based Retrieval and Editing | 2023 | Nature Machine Intelligence | https://doi.org/10.1038/s42256-023-00759-6 | https://github.com/chao1224/MoleculeSTM | MoleculeSTM 用分子结构-文本对比预训练支撑检索和编辑，是 graph-text contrastive pretraining 的关键分子场景论文。 | High |
| GraphCLIP: Enhancing Transferability in Graph Foundation Models for Text-Attributed Graphs | 2024 | arXiv | https://arxiv.org/abs/2410.10329 | https://github.com/ZhuYun97/GraphCLIP | GraphCLIP 面向 text-attributed graphs 做 language-graph pretraining，适合关注 GCL 与 graph foundation model 的交叉。 | Medium |

## 13. recommendation graph contrastive learning

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Self-supervised Graph Learning for Recommendation | 2021 | SIGIR | https://arxiv.org/abs/2010.10783 | https://github.com/wujcan/SGL | SGL 在 user-item graph 上引入 node dropout、edge dropout、random walk 视图，是推荐图 GCL 的经典起点。 | High |
| Are Graph Augmentations Necessary? Simple Graph Contrastive Learning for Recommendation | 2022 | SIGIR | https://arxiv.org/abs/2112.08679 | Unknown | SimGCL 质疑推荐图中结构增强的必要性，改用 embedding noise，适合反思图增强是否真的贡献核心增益。 | High |
| Improving Graph Collaborative Filtering with Neighborhood-enriched Contrastive Learning | 2022 | WWW | https://arxiv.org/abs/2202.06200 | https://github.com/RUCAIBox/NCL | NCL 将结构邻居和语义邻居纳入正样本/对比对设计，是推荐图中正样本定义的重要代表。 | High |
| LightGCL: Simple Yet Effective Graph Contrastive Learning for Recommendation | 2023 | ICLR | https://arxiv.org/abs/2302.08191 | https://github.com/HKUDS/LightGCL | LightGCL 使用 SVD 视图建模全局协同关系，关注稀疏性和 popularity bias，对轻量推荐 GCL 很有参考价值。 | High |

## 14. molecular graph contrastive learning

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Self-Supervised Graph Transformer on Large-Scale Molecular Data | 2020 | NeurIPS | https://arxiv.org/abs/2007.02835 | https://github.com/tencent-ailab/grover | GROVER 在大规模分子上设计 node、edge、graph-level 自监督任务，是分子图预训练的重要基线。 | High |
| Pre-training Molecular Graph Representation with 3D Geometry | 2022 | ICLR | https://arxiv.org/abs/2110.07728 | https://github.com/chao1224/GraphMVP | GraphMVP 对齐 2D 分子图与 3D 几何视图，是 multi-view molecular contrastive pretraining 的关键论文。 | High |
| Mole-BERT: Rethinking Pre-training Graph Neural Networks for Molecules | 2023 | ICLR | https://openreview.net/forum?id=jevY-DtiZTR | https://github.com/junxia97/Mole-BERT | Mole-BERT 结合 masked atom modeling 与 graph-level contrastive learning，适合研究分子预训练中的 tokenization 和语义相似性。 | High |

## 15. dynamic graph contrastive learning

| Paper | Year | Venue | Link | Code | Why Relevant | Priority |
|---|---:|---|---|---|---|---|
| Self-supervised Representation Learning on Dynamic Graphs | 2021 | CIKM | https://dl.acm.org/doi/10.1145/3459637.3482389 | Unknown | DDGCL 是较早面向动态图的自监督/去偏动态图对比学习框架，关注时间邻近视图和采样偏差。 | High |
| Self-Supervised Dynamic Graph Representation Learning via Temporal Subgraph Contrast | 2023 | ACM TKDD | https://arxiv.org/abs/2112.08733 | Unknown | DySubC 用时间子图对比同时学习结构和演化特征，是 temporal subgraph contrast 的代表。 | Medium |
| CLDG: Contrastive Learning on Dynamic Graphs | 2023 | ICDE | https://ieeexplore.ieee.org/document/10184608/ | https://github.com/yimingxu24/cldg | CLDG 基于 timespan view 和 temporal translation invariance 构造动态图对比信号，适合扩展静态 GCL 到动态图。 | High |
