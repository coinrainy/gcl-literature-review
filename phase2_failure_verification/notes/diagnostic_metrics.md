# Diagnostic Metrics

## 使用原则

所有标签相关指标只用于 post-hoc diagnostic analysis。标签不能用于无监督训练、增强选择、pair weighting 或目标函数优化。

## 1. Graph Statistics

- `num_nodes`：节点数。
- `num_edges`：去重后的无向边数，不含 self-loop。
- `num_features`：节点特征维度。
- `num_classes`：可见标签类别数，仅用于后验统计。
- `global_edge_homophily`：同类边数 / 有标签边数。
- `local_node_homophily_mean/std`：每个节点同类邻居比例的均值和标准差。
- `degree_mean/std`：无向度均值和标准差。
- `class_distribution`：标签分布。
- `same_class_edge_ratio` 与 `cross_class_edge_ratio`：同类边和跨类边比例。

能证明什么：数据集是否真的覆盖同配和异配场景，后续 failure 结果是否可能由类别极度不均衡或度分布造成。

局限：同配率不能完全描述 benign / malignant / ambiguous heterophily，也不能替代任务性能。

## 2. Positive View Failure

### Edge preservation by label relation

对 edge dropping rate `r`：

- `retained_same_class_edges`
- `retained_cross_class_edges`
- `dropped_same_class_edges`
- `dropped_cross_class_edges`
- `same_class_edge_retention_rate = retained_same_class_edges / original_same_class_edges`
- `cross_class_edge_retention_rate = retained_cross_class_edges / original_cross_class_edges`

能证明什么：随机删边是否更容易破坏某类语义边，尤其是在异配图中是否误删 role-preserving / cross-class edges。

局限：边的同类 / 跨类关系来自标签后验，不等同于真实语义边类型。

### Local neighborhood semantic drift

对每个节点，比较增强前后邻域标签分布：

- `neighbor_label_distribution_js_divergence = JS(P_original_neighbor_label || P_augmented_neighbor_label)`
- `neighbor_label_distribution_l1_distance = ||P_original - P_augmented||_1`
- `local_homophily_change = local_homophily_augmented - local_homophily_original`

按 local homophily 分组：

- low homophily：`local_homophily < 0.33`
- medium homophily：`0.33 <= local_homophily < 0.66`
- high homophily：`local_homophily >= 0.66`

能证明什么：增强是否在低同配节点上造成更强邻域语义漂移。

局限：邻域标签分布是后验 proxy，不能说明训练时模型已经知道这些标签。

### Positive embedding reliability

如果有两视图 embeddings 或 raw feature proxy：

- `positive_pair_cosine_similarity = cos(z_i^view1, z_i^view2)`
- `positive_pair_rank`：同节点跨视图相似度在该节点对所有 view2 节点相似度中的排名。
- `positive_pair_similarity_drop = same_class_average_similarity - same_node_cross_view_similarity`
- `low_reliability_positive_ratio`：低可靠 positive 的比例。

默认低可靠规则：

`same_node_cross_view_similarity < same_class_node_average_similarity`

也可用阈值：

`same_node_cross_view_similarity < preset_threshold`

能证明什么：同一节点跨视图是否仍然比同类节点平均相似度更可靠。

局限：raw feature proxy 不是训练后的 GCL embedding；如果 encoder 很弱，rank 与 cosine 只能作为初筛。

## 3. Negative Pair Noise

### Batch negative class collision rate

对随机 batch：

- `total_negative_pairs = batch_size * (batch_size - 1)`，按有效标签 anchor 过滤。
- `same_class_negative_pairs`：负样本中同类 pair 数。
- `false_negative_rate = same_class_negative_pairs / total_negative_pairs`

扫描 batch size：128、256、512、1024、full batch if feasible。

能证明什么：普通 batch negatives 中是否已经有明显同类 collision。

局限：同类不一定语义等价，异类也不一定语义相反。

### Hard negative false negative rate

用 embedding similarity 或 feature proxy 找 top-k hard negatives：

- `top_k = 5, 10, 20, 50`
- `hard_negative_same_class_rate`
- `hard_negative_cross_class_rate`
- `hard_negative_false_negative_rate`

能证明什么：越 hard 的 negatives 是否越容易混入同类样本，从而攻击“hard negative 越难越有价值”的假设。

局限：如果 embedding 是 raw feature proxy，结论只能说明输入空间近邻的 collision，不等同于训练后的表示空间 collision。

### Degree-aware / homophily-aware collision

分组：

- low-degree nodes
- high-degree nodes
- low-homophily nodes
- high-homophily nodes

能证明什么：false negative 是否集中在结构稀疏、低同配或高密度区域。

局限：分组阈值是诊断便利设定，不是理论边界。

## 4. Joint Positive-Negative Reliability Conflict

第一版：

`joint_reliability_risk_score = normalized_positive_failure_score + normalized_negative_collision_score`

其中 positive failure score 由 JS drift、local homophily change、low reliability positive ratio 聚合；negative collision score 由 random batch collision 与 hard-negative collision 聚合。

能证明什么：同一数据集 / 节点组是否同时存在正样本视图失效和负样本 collision。

局限：这是排序指标，不是训练目标，也不是论文最终结论。

