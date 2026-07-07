# Phase 2: Gap 2 Failure Verification

本阶段目标是验证 **Positive-Negative Pair Reliability Calibration for Graph Contrastive Learning** 是否值得继续推进。这里不实现完整新方法，只做 failure verification。

## 目录结构

```text
phase2_failure_verification/
  README.md
  configs/
    datasets.yaml
    augmentations.yaml
    diagnostics.yaml
    baselines.yaml
  scripts/
    compute_graph_statistics.py
    simulate_positive_view_failure.py
    diagnose_negative_pair_noise.py
    diagnose_embedding_pair_reliability.py
    aggregate_failure_results.py
    utils.py
  outputs/
    tables/
    figures/
    reports/
  notes/
    failure_verification_protocol.md
    diagnostic_metrics.md
    baseline_collision_check.md
```

## 环境依赖

最低依赖：

```bash
python -m pip install numpy
```

可选依赖：

```bash
python -m pip install torch torch-geometric
```

如果 PyG 不可用，可以使用自定义输入：

```bash
python phase2_failure_verification/scripts/compute_graph_statistics.py \
  --dataset CustomGraph \
  --npz-path path/to/graph.npz
```

`graph.npz` 需要包含 `edge_index` 或 `edges`，可选包含 `x` / `features` 和 `y` / `labels`。标签只用于后验诊断。

## 脚本命令

Step 1：计算图统计。

```bash
python phase2_failure_verification/scripts/compute_graph_statistics.py \
  --dataset Cora \
  --output phase2_failure_verification/outputs/tables/graph_statistics.csv
```

Step 2：扫描 positive view failure。

```bash
python phase2_failure_verification/scripts/simulate_positive_view_failure.py \
  --dataset Chameleon \
  --augmentation edge_drop \
  --rates 0.1 0.2 0.4 0.6 0.8 \
  --output phase2_failure_verification/outputs/tables/positive_view_failure.csv
```

Step 3：诊断 negative pair noise。

```bash
python phase2_failure_verification/scripts/diagnose_negative_pair_noise.py \
  --dataset Chameleon \
  --batch-sizes 128 256 512 1024 \
  --top-k 5 10 20 50 \
  --embedding-path optional/path/to/embeddings.npy \
  --output phase2_failure_verification/outputs/tables/negative_pair_noise.csv
```

如果不提供 `--embedding-path`，脚本会在有 node features 时用 raw features 作为 proxy，并在输出中标注 `embedding_source=raw_feature_proxy`。

Step 4：诊断两视图 embedding pair reliability。

```bash
python phase2_failure_verification/scripts/diagnose_embedding_pair_reliability.py \
  --dataset Chameleon \
  --view1-embedding path/to/view1.npy \
  --view2-embedding path/to/view2.npy \
  --labels path/to/labels.npy \
  --output phase2_failure_verification/outputs/tables/embedding_pair_reliability.csv
```

Step 5：汇总报告。

```bash
python phase2_failure_verification/scripts/aggregate_failure_results.py \
  --report-output phase2_failure_verification/outputs/reports/failure_verification_summary.md
```

## 推荐第一轮运行顺序

1. `compute_graph_statistics.py`
2. `simulate_positive_view_failure.py`
3. `diagnose_negative_pair_noise.py`
4. `aggregate_failure_results.py`
5. 根据结果判断是否进入方法设计。

第一轮建议数据集：

- 同配 sanity check：Cora、Citeseer、PubMed。
- 异配主测：Chameleon、Squirrel、Actor、Cornell、Texas、Wisconsin。
- Amazon Computers 和 Coauthor CS 可作为同配扩展。

## 如何解释结果

Gap 2 值得继续的信号：

- 异配图或低同配节点上 positive view failure 明显更高。
- hard negatives 的 false negative rate 明显高于随机 negatives。
- 增强越强，positive reliability 越低。
- positive failure 与 negative collision 在同一数据集或节点组共现。

需要 pivot 的信号：

- 只有 positive failure 明显：回到 Gap 1 的 view / positive reliability calibration。
- 只有 negative collision 明显：转向 scalable mini-batch negative noise。
- 二者都不明显：降低论文目标，不直接进入顶会方法主线。

## 下一步进入方法设计

只有 failure verification 支持 Gap 2 后，才设计不依赖标签训练的 reliability estimator。候选证据可以包括增强一致性、结构距离、embedding stability、局部同配不确定性和可选文本一致性；标签仍只在训练后用于诊断其行为。

