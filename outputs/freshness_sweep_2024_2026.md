# 2024–2026 Freshness Sweep：GCL 候选 Gap 定向补强

本报告基于 2026-07-07 的定向检索与 `outputs/gcl_literature_table.csv` 最新 57 篇文献表生成。目标不是重跑全流程，而是检查近期工作是否影响以下候选方向的新颖性：

- Gap 1：Heterophily-aware Semantic-Preserving Augmentation
- Gap 2：Reliability-aware False Negative and False Positive Correction
- Gap 7：Graph-Text Conflict-aware Contrastive Pretraining

## 1. 检索关键词

- Graph Contrastive Learning survey recent trend 2024
- Heterophily Graph Contrastive Learning 2024 2025 2026
- Heterophily Graph Self-supervised Learning
- Heterophilic Graph Learning benchmark evaluation 2024
- Text-attributed Graph Contrastive Learning 2024 2025
- LLM + Text-attributed Graph
- Graph Foundation Model survey 2025
- Graph-text contrastive pretraining
- Pair reliability false negative false positive in GCL
- View reliability semantic-preserving augmentation in GCL
- PolyGCL / HeterGCL / M3P-GCL / ROSEN / IFL-GCL / GCL-OT

## 2. 新增论文

| Paper | Year | Venue | Link | 影响 Gap | 加入原因 |
|---|---:|---|---|---|---|
| Towards Graph Contrastive Learning: A Survey and Beyond | 2024 | arXiv | https://arxiv.org/abs/2405.11868 | Gap 1/2/7 | 提供 GCL 最新分类框架，帮助判断 augmentation、objective、negative sampling 是否已拥挤。 |
| The Heterophilic Graph Learning Handbook | 2024 | arXiv | https://arxiv.org/abs/2407.09618 | Gap 1 | 提醒异配图 benchmark 需要区分 malignant / benign / ambiguous heterophily，不能只用传统小图声称有效。 |
| Re-evaluating the Advancements of Heterophilic Graph Learning | 2024 | arXiv | https://arxiv.org/abs/2409.05755 | Gap 1 | 指出 heterophily-specific 方法和 homophily metrics 评估存在陷阱，提高 Gap 1 的实验门槛。 |
| When Heterophily Meets Heterogeneity: Challenges and a New Large-Scale Graph Benchmark | 2025 | KDD | https://doi.org/10.1145/3711896.3737421 | Gap 1/2 | H2GB 提供大规模异配异构 benchmark 与 28 个 baseline，挑战只在小型异配图上验证的 claim。 |
| Graph Foundation Models: A Comprehensive Survey | 2025 | arXiv | https://arxiv.org/abs/2505.15116 | Gap 7 | 说明 graph foundation model 方向快速拥挤，普通 graph-text 预训练叙事不够。 |
| Large Language Models Meet Text-Attributed Graphs | 2025 | arXiv | https://arxiv.org/abs/2510.21131 | Gap 7 | 系统梳理 LLM4TAG / TAG4LLM，压缩普通 LLM-based TAG augmentation 的 novelty。 |
| PolyGCL: Graph Contrastive Learning via Learnable Spectral Polynomial Filters | 2024 | ICLR | https://proceedings.iclr.cc/paper_files/paper/2024/hash/6faf3b8ed0df532c14d0fc009e451b6d-Abstract-Conference.html | Gap 1 | 直接用 spectral polynomial filters 覆盖 heterophily-aware GCL 的 filter 路线。 |
| HeterGCL: Graph Contrastive Learning Framework on Heterophilic Graph | 2024 | IJCAI | https://www.ijcai.org/proceedings/2024/0265.pdf | Gap 1 | 放弃随机增强，结合结构学习和语义学习处理异配 GCL，是 Gap 1 强 baseline。 |
| Beyond Homophily: Graph Contrastive Learning with Macro-Micro Message Passing | 2025 | AAAI | https://ojs.aaai.org/index.php/AAAI/article/view/33751 | Gap 1 | M3P-GCL 从 macro structural/attribute views 和 micro self-propagation 改造异配 GCL。 |
| Graph Contrastive Learning Reimagined: Exploring Universality | 2024 | WWW | https://doi.org/10.1145/3589334.3645480 | Gap 1/2 | ROSEN 明确指出 local positive sampling 在异配图上会产生 false positive samples，并重构同配结构。 |
| InfoNCE is a Free Lunch for Semantically Guided Graph Contrastive Learning | 2025 | SIGIR | https://arxiv.org/abs/2505.06282 | Gap 2 | IFL-GCL 将 GCL 解释为 PU learning，并用 InfoNCE-derived score 挖掘语义相似未标注正样本。 |
| GCL-OT: Graph Contrastive Learning with Optimal Transport for Heterophilic Text-Attributed Graphs | 2026 | AAAI | https://arxiv.org/abs/2511.16778 | Gap 7 | 直接处理 heterophilic TAG 的 structure-text alignment，是 Gap 7 的强 collision paper。 |

## 3. Collision Papers

### Gap 1：Heterophily-aware Semantic-Preserving Augmentation

- `HLCL`：已经做 graph-filter heterophily-aware views。
- `HGMS`：已经做 heterogeneous homophily-aware edge dropping 和 multi-view self-expression。
- `PolyGCL`：已经做 learnable spectral polynomial filters，覆盖 high-pass / low-pass 异配视图。
- `HeterGCL`：已经放弃随机增强，改用 adaptive neighbor aggregation、结构学习和语义学习。
- `M3P-GCL`：已经从 structural / attribute views 和 self-loop role 改造 macro/micro message passing。
- `ROSEN`：已经显式处理异配图 local positive sampling 的 false positive samples。

结论：普通“异配图增强”已经拥挤。Gap 1 只有在转向 view reliability / positive reliability calibration 时仍有方法空间。

### Gap 2：Reliability-aware False Negative and False Positive Correction

- `GDCL` / `ProGCL` / `CGC`：已有 false negative、hard negative 或 counterfactual negative 处理。
- `IFL-GCL`：新增强 collision，已经用 PU learning 和 InfoNCE free-lunch 处理语义相似 non-augmented positives。
- `ROSEN`：已经从 positive side 处理异配 local positive false positives。
- `HGMS`：在异构图中用 multi-view self-expression 缓解 false negatives。

结论：只做 false negative correction 不够新。Gap 2 仍成立，但核心必须是 positive reliability 与 negative reliability 的双侧校准，并给出 true-hard / false-hard / uncertain-hard 诊断。

### Gap 7：Graph-Text Conflict-aware Contrastive Pretraining

- `GAugLLM`：已经覆盖 LLM-based TAG feature / edge augmentation。
- `GraphCLIP` / `MoleculeSTM`：已有 graph-text contrastive alignment。
- `GraphGPT`：已有 graph-to-LLM instruction tuning。
- `GCL-OT`：新增强 collision，已经覆盖 heterophilic TAG 的 OT-based structure-text alignment。
- `Large Language Models Meet Text-Attributed Graphs` / `Graph Foundation Models: A Comprehensive Survey`：说明 LLM+TAG / GFM 方向正在快速拥挤。

结论：普通 LLM augmentation 或普通 structure-text alignment 已不够新。Gap 7 只有在聚焦 structure-text conflict taxonomy、cross-modal pair reliability、conflict-aware soft labels，并证明 GAugLLM/GCL-OT 在冲突样本上失败时仍成立。

## 4. 变得更拥挤的方向

- Heterophily-aware augmentation：从 GREET/HLCL/HGMS 扩展到 PolyGCL/HeterGCL/M3P-GCL/ROSEN，普通边分数、filter、message passing 分支都容易 incremental。
- Heterophily benchmark claim：Handbook、Re-evaluating、H2GB 提高了评估要求；只用 Cornell/Texas/Wisconsin/Actor 或 Chameleon/Squirrel 不够。
- Negative-side reliability：IFL-GCL 已经把 semantic positives / PU learning 做得很明确，简单相似度重加权风险高。
- LLM-based TAG augmentation：GAugLLM 和 LLM+TAG survey 说明这个方向已经很热。
- Heterophilic TAG alignment：GCL-OT 已经覆盖 multi-granular heterophily + OT alignment，Gap 7 必须更细。

## 5. 仍然成立的 Gap

| Gap | 是否仍成立 | 收窄后的有效表述 |
|---|---|---|
| Gap 1 | 成立但风险高 | 不再做普通 heterophily-aware augmentation，而做 uncertainty-calibrated view reliability / positive reliability calibration。 |
| Gap 2 | 成立且最适合短期启动 | 不再只修正 false negatives，而做 positive/negative 双侧 pair reliability calibration。 |
| Gap 7 | 成立但工程和 novelty 风险高 | 不再做普通 LLM augmentation 或 OT alignment，而做 structure-text conflict-aware soft labels 与 graph-text pair reliability。 |

## 6. 最推荐进入 failure verification 的方向

1. **Gap 2：Reliability-aware False Negative and False Positive Correction**
   - 原因：failure mode 最容易构造和量化，可先用标签后验统计 false negatives，再用增强强度制造 false positive views。
   - 最强 baseline：IFL-GCL、ProGCL、GDCL、CGC、ROSEN、HLCL、HGMS。
   - 适合 venue：ICML / NeurIPS / ICLR；若加入大规模图实验，适合 KDD / WWW。

2. **Gap 1 的收窄版：View / Positive Reliability Calibration under Heterophily**
   - 原因：短期可在 GRACE/GCA/HLCL/PolyGCL/HeterGCL 风格框架上启动，但必须避开“又一个异配增强”。
   - 最强 baseline：GREET、HLCL、HGMS、PolyGCL、HeterGCL、M3P-GCL、ROSEN、LINKX。
   - 适合 venue：NeurIPS / ICLR / ICML；如果主打 benchmark / scalability，适合 KDD / WWW。

3. **Gap 7 的收窄版：Structure-Text Conflict-aware Pair Reliability**
   - 原因：方向潜力高，但必须先构造可复现 conflict benchmark，否则容易被 GAugLLM/GCL-OT 认为已覆盖。
   - 最强 baseline：GAugLLM、GCL-OT、GraphCLIP、MoleculeSTM、GraphGPT、IFL-GCL。
   - 适合 venue：NeurIPS / ICLR / ICML；如果以 TAG benchmark 和应用为主，适合 KDD / WWW。

## 7. 最终建议

可以进入下一阶段 failure verification，但进入时必须采用收窄后的 claim：

- Gap 1：只验证 view reliability / positive reliability calibration，不再声称普通 heterophily-aware augmentation 是主要创新。
- Gap 2：优先验证 positive/negative 双侧 reliability calibration，这是当前 novelty 风险最可控、短期实验最可启动的方向。
- Gap 7：先做 structure-text conflict set 和 GAugLLM/GCL-OT failure verification，再决定是否投入完整方法。

**最终判断：可以进入下一阶段；**
