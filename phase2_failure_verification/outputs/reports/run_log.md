# Phase 2 First-Round Run Log

Started: 2026-07-07 17:40:23 +08:00

Datasets: Cora, Citeseer, PubMed, Chameleon, Squirrel, Actor

Labels policy: labels are used only for post-hoc diagnostic analysis; no training, augmentation selection, or pair weighting was performed.

## Cora - compute_graph_statistics

Command: `python phase2_failure_verification\scripts\compute_graph_statistics.py --dataset Cora --output phase2_failure_verification\outputs\tables\graph_statistics.csv --overwrite`

Start: 2026-07-07 17:40:23 +08:00
End: 2026-07-07 17:40:28 +08:00
Exit code: 0

```text
2026-07-07 17:40:23,961 | INFO | Loading dataset Cora
2026-07-07 17:40:27,516 | INFO | Computing graph statistics from source=pyg
2026-07-07 17:40:27,533 | INFO | Wrote graph statistics to phase2_failure_verification\outputs\tables\graph_statistics.csv
```

## Cora - simulate_positive_view_failure

Command: `python phase2_failure_verification\scripts\simulate_positive_view_failure.py --dataset Cora --augmentation edge_drop --rates 0.1 0.2 0.4 0.6 0.8 --num-trials 5 --output phase2_failure_verification\outputs\tables\positive_view_failure.csv --overwrite`

Start: 2026-07-07 17:40:28 +08:00
End: 2026-07-07 17:40:40 +08:00
Exit code: 0

```text
2026-07-07 17:40:31,684 | INFO | Running positive view diagnostics for Cora
2026-07-07 17:40:40,396 | INFO | Wrote positive view diagnostics to phase2_failure_verification\outputs\tables\positive_view_failure.csv
```

## Cora - diagnose_negative_pair_noise

Command: `python phase2_failure_verification\scripts\diagnose_negative_pair_noise.py --dataset Cora --batch-sizes 128 256 512 1024 --top-k 5 10 20 50 --num-batches 50 --output phase2_failure_verification\outputs\tables\negative_pair_noise.csv --overwrite`

Start: 2026-07-07 17:40:40 +08:00
End: 2026-07-07 17:40:46 +08:00
Exit code: 0

```text
2026-07-07 17:40:45,697 | INFO | Wrote negative pair diagnostics to phase2_failure_verification\outputs\tables\negative_pair_noise.csv
```

## Citeseer - compute_graph_statistics

Command: `python phase2_failure_verification\scripts\compute_graph_statistics.py --dataset Citeseer --output phase2_failure_verification\outputs\tables\graph_statistics.csv`

Start: 2026-07-07 17:40:46 +08:00
End: 2026-07-07 17:40:50 +08:00
Exit code: 0

```text
2026-07-07 17:40:46,310 | INFO | Loading dataset Citeseer
2026-07-07 17:40:49,735 | INFO | Computing graph statistics from source=pyg
2026-07-07 17:40:49,753 | INFO | Wrote graph statistics to phase2_failure_verification\outputs\tables\graph_statistics.csv
```

## Citeseer - simulate_positive_view_failure

Command: `python phase2_failure_verification\scripts\simulate_positive_view_failure.py --dataset Citeseer --augmentation edge_drop --rates 0.1 0.2 0.4 0.6 0.8 --num-trials 5 --output phase2_failure_verification\outputs\tables\positive_view_failure.csv`

Start: 2026-07-07 17:40:50 +08:00
End: 2026-07-07 17:41:11 +08:00
Exit code: 0

```text
2026-07-07 17:40:53,911 | INFO | Running positive view diagnostics for Citeseer
2026-07-07 17:41:10,649 | INFO | Wrote positive view diagnostics to phase2_failure_verification\outputs\tables\positive_view_failure.csv
```

## Citeseer - diagnose_negative_pair_noise

Command: `python phase2_failure_verification\scripts\diagnose_negative_pair_noise.py --dataset Citeseer --batch-sizes 128 256 512 1024 --top-k 5 10 20 50 --num-batches 50 --output phase2_failure_verification\outputs\tables\negative_pair_noise.csv`

Start: 2026-07-07 17:41:11 +08:00
End: 2026-07-07 17:41:17 +08:00
Exit code: 0

```text
2026-07-07 17:41:16,546 | INFO | Wrote negative pair diagnostics to phase2_failure_verification\outputs\tables\negative_pair_noise.csv
```

## PubMed - compute_graph_statistics

Command: `python phase2_failure_verification\scripts\compute_graph_statistics.py --dataset PubMed --output phase2_failure_verification\outputs\tables\graph_statistics.csv`

Start: 2026-07-07 17:41:17 +08:00
End: 2026-07-07 17:41:21 +08:00
Exit code: 0

```text
2026-07-07 17:41:17,190 | INFO | Loading dataset PubMed
2026-07-07 17:41:20,770 | INFO | Computing graph statistics from source=pyg
2026-07-07 17:41:20,910 | INFO | Wrote graph statistics to phase2_failure_verification\outputs\tables\graph_statistics.csv
```

## PubMed - simulate_positive_view_failure

Command: `python phase2_failure_verification\scripts\simulate_positive_view_failure.py --dataset PubMed --augmentation edge_drop --rates 0.1 0.2 0.4 0.6 0.8 --num-trials 5 --output phase2_failure_verification\outputs\tables\positive_view_failure.csv`

Start: 2026-07-07 17:41:21 +08:00
End: 2026-07-07 17:42:23 +08:00
Exit code: 0

```text
2026-07-07 17:41:25,610 | INFO | Running positive view diagnostics for PubMed
2026-07-07 17:42:22,664 | INFO | Wrote positive view diagnostics to phase2_failure_verification\outputs\tables\positive_view_failure.csv
```

## PubMed - diagnose_negative_pair_noise

Command: `python phase2_failure_verification\scripts\diagnose_negative_pair_noise.py --dataset PubMed --batch-sizes 128 256 512 1024 --top-k 5 10 20 50 --num-batches 50 --output phase2_failure_verification\outputs\tables\negative_pair_noise.csv`

Start: 2026-07-07 17:42:23 +08:00
End: 2026-07-07 17:42:28 +08:00
Exit code: 0

```text
2026-07-07 17:42:28,485 | INFO | Wrote negative pair diagnostics to phase2_failure_verification\outputs\tables\negative_pair_noise.csv
```

## Chameleon - compute_graph_statistics

Command: `python phase2_failure_verification\scripts\compute_graph_statistics.py --dataset Chameleon --output phase2_failure_verification\outputs\tables\graph_statistics.csv`

Start: 2026-07-07 17:42:28 +08:00
End: 2026-07-07 17:42:33 +08:00
Exit code: 0

```text
2026-07-07 17:42:29,122 | INFO | Loading dataset Chameleon
2026-07-07 17:42:32,576 | INFO | Computing graph statistics from source=pyg
2026-07-07 17:42:32,654 | INFO | Wrote graph statistics to phase2_failure_verification\outputs\tables\graph_statistics.csv
```

## Chameleon - simulate_positive_view_failure

Command: `python phase2_failure_verification\scripts\simulate_positive_view_failure.py --dataset Chameleon --augmentation edge_drop --rates 0.1 0.2 0.4 0.6 0.8 --num-trials 5 --output phase2_failure_verification\outputs\tables\positive_view_failure.csv`

Start: 2026-07-07 17:42:33 +08:00
End: 2026-07-07 17:42:50 +08:00
Exit code: 0

```text
2026-07-07 17:42:36,595 | INFO | Running positive view diagnostics for Chameleon
2026-07-07 17:42:50,158 | INFO | Wrote positive view diagnostics to phase2_failure_verification\outputs\tables\positive_view_failure.csv
```

## Chameleon - diagnose_negative_pair_noise

Command: `python phase2_failure_verification\scripts\diagnose_negative_pair_noise.py --dataset Chameleon --batch-sizes 128 256 512 1024 --top-k 5 10 20 50 --num-batches 50 --output phase2_failure_verification\outputs\tables\negative_pair_noise.csv`

Start: 2026-07-07 17:42:50 +08:00
End: 2026-07-07 17:42:55 +08:00
Exit code: 0

```text
2026-07-07 17:42:54,879 | INFO | Wrote negative pair diagnostics to phase2_failure_verification\outputs\tables\negative_pair_noise.csv
```

## Squirrel - compute_graph_statistics

Command: `python phase2_failure_verification\scripts\compute_graph_statistics.py --dataset Squirrel --output phase2_failure_verification\outputs\tables\graph_statistics.csv`

Start: 2026-07-07 17:42:55 +08:00
End: 2026-07-07 17:42:59 +08:00
Exit code: 0

```text
2026-07-07 17:42:55,429 | INFO | Loading dataset Squirrel
2026-07-07 17:42:58,614 | INFO | Computing graph statistics from source=pyg
2026-07-07 17:42:59,215 | INFO | Wrote graph statistics to phase2_failure_verification\outputs\tables\graph_statistics.csv
```

## Squirrel - simulate_positive_view_failure

Command: `python phase2_failure_verification\scripts\simulate_positive_view_failure.py --dataset Squirrel --augmentation edge_drop --rates 0.1 0.2 0.4 0.6 0.8 --num-trials 5 --output phase2_failure_verification\outputs\tables\positive_view_failure.csv`

Start: 2026-07-07 17:42:59 +08:00
End: 2026-07-07 17:43:52 +08:00
Exit code: 0

```text
2026-07-07 17:43:03,322 | INFO | Running positive view diagnostics for Squirrel
2026-07-07 17:43:52,033 | INFO | Wrote positive view diagnostics to phase2_failure_verification\outputs\tables\positive_view_failure.csv
```

## Squirrel - diagnose_negative_pair_noise

Command: `python phase2_failure_verification\scripts\diagnose_negative_pair_noise.py --dataset Squirrel --batch-sizes 128 256 512 1024 --top-k 5 10 20 50 --num-batches 50 --output phase2_failure_verification\outputs\tables\negative_pair_noise.csv`

Start: 2026-07-07 17:43:52 +08:00
End: 2026-07-07 17:43:58 +08:00
Exit code: 0

```text
2026-07-07 17:43:58,004 | INFO | Wrote negative pair diagnostics to phase2_failure_verification\outputs\tables\negative_pair_noise.csv
```

## Actor - compute_graph_statistics

Command: `python phase2_failure_verification\scripts\compute_graph_statistics.py --dataset Actor --output phase2_failure_verification\outputs\tables\graph_statistics.csv`

Start: 2026-07-07 17:43:58 +08:00
End: 2026-07-07 17:44:02 +08:00
Exit code: 0

```text
2026-07-07 17:43:58,656 | INFO | Loading dataset Actor
2026-07-07 17:44:02,025 | INFO | Computing graph statistics from source=pyg
2026-07-07 17:44:02,092 | INFO | Wrote graph statistics to phase2_failure_verification\outputs\tables\graph_statistics.csv
```

## Actor - simulate_positive_view_failure

Command: `python phase2_failure_verification\scripts\simulate_positive_view_failure.py --dataset Actor --augmentation edge_drop --rates 0.1 0.2 0.4 0.6 0.8 --num-trials 5 --output phase2_failure_verification\outputs\tables\positive_view_failure.csv`

Start: 2026-07-07 17:44:02 +08:00
End: 2026-07-07 17:44:28 +08:00
Exit code: 0

```text
2026-07-07 17:44:06,058 | INFO | Running positive view diagnostics for Actor
2026-07-07 17:44:28,370 | INFO | Wrote positive view diagnostics to phase2_failure_verification\outputs\tables\positive_view_failure.csv
```

## Actor - diagnose_negative_pair_noise

Command: `python phase2_failure_verification\scripts\diagnose_negative_pair_noise.py --dataset Actor --batch-sizes 128 256 512 1024 --top-k 5 10 20 50 --num-batches 50 --output phase2_failure_verification\outputs\tables\negative_pair_noise.csv`

Start: 2026-07-07 17:44:28 +08:00
End: 2026-07-07 17:44:34 +08:00
Exit code: 0

```text
2026-07-07 17:44:33,780 | INFO | Wrote negative pair diagnostics to phase2_failure_verification\outputs\tables\negative_pair_noise.csv
```

## ALL - aggregate_failure_results

Command: `python phase2_failure_verification\scripts\aggregate_failure_results.py --graph-statistics phase2_failure_verification\outputs\tables\graph_statistics.csv --positive-view-failure phase2_failure_verification\outputs\tables\positive_view_failure.csv --negative-pair-noise phase2_failure_verification\outputs\tables\negative_pair_noise.csv --joint-output phase2_failure_verification\outputs\tables\joint_reliability_risk.csv --report-output phase2_failure_verification\outputs\reports\failure_verification_summary.md`

Start: 2026-07-07 17:44:34 +08:00
End: 2026-07-07 17:44:34 +08:00
Exit code: 0

```text
2026-07-07 17:44:34,400 | INFO | Wrote joint CSV to phase2_failure_verification\outputs\tables\joint_reliability_risk.csv
2026-07-07 17:44:34,400 | INFO | Wrote report to phase2_failure_verification\outputs\reports\failure_verification_summary.md
```

Completed: 2026-07-07 17:44:34 +08:00
