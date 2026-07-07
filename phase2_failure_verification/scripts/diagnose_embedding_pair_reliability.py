from __future__ import annotations

import argparse

import numpy as np

from utils import (
    hard_negative_collision,
    positive_similarity_summary,
    read_array,
    set_random_seed,
    setup_logger,
    write_csv_rows,
)


FIELDNAMES = [
    "dataset",
    "group",
    "top_k",
    "positive_pair_cosine_similarity",
    "positive_pair_cosine_similarity_std",
    "positive_pair_rank",
    "positive_pair_similarity_drop",
    "low_reliability_positive_ratio",
    "positive_nodes_evaluated",
    "hard_negative_same_class_rate",
    "hard_negative_cross_class_rate",
    "hard_negative_false_negative_rate",
    "embedding_source",
    "labels_posthoc_only",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose pair-level reliability from two embedding views.")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--view1-embedding", required=True)
    parser.add_argument("--view2-embedding", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--group-path", default=None, help="Optional NPY/CSV boolean or integer group labels.")
    parser.add_argument("--positive-threshold", type=float, default=None)
    parser.add_argument("--top-k", nargs="+", type=int, default=[5, 10, 20, 50])
    parser.add_argument("--max-rank-nodes", type=int, default=2000)
    parser.add_argument("--max-nodes-for-hard-negative", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        default="phase2_failure_verification/outputs/tables/embedding_pair_reliability.csv",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--log-path", default=None)
    return parser.parse_args()


def _group_masks(labels: np.ndarray, group_path: str | None) -> dict[str, np.ndarray]:
    n = labels.shape[0]
    if not group_path:
        return {"all": np.ones(n, dtype=bool)}
    group_values = read_array(group_path).reshape(-1)[:n]
    masks = {"all": np.ones(n, dtype=bool)}
    for value in np.unique(group_values):
        masks[f"group_{value}"] = group_values == value
    return masks


def main() -> None:
    args = parse_args()
    set_random_seed(args.seed)
    logger = setup_logger(log_path=args.log_path)
    view1 = read_array(args.view1_embedding)
    view2 = read_array(args.view2_embedding)
    labels = read_array(args.labels, dtype=np.int64).reshape(-1)
    n = min(view1.shape[0], view2.shape[0], labels.shape[0])
    view1 = view1[:n]
    view2 = view2[:n]
    labels = labels[:n]
    masks = _group_masks(labels, args.group_path)

    positive = positive_similarity_summary(
        view1,
        view2,
        labels,
        masks,
        threshold=args.positive_threshold,
        max_rank_nodes=args.max_rank_nodes,
        seed=args.seed,
    )
    hard_rows = hard_negative_collision(
        view1,
        labels,
        top_k_values=args.top_k,
        seed=args.seed,
        group_masks=masks,
        max_nodes=args.max_nodes_for_hard_negative,
        embedding_source="provided_embeddings",
    )
    hard_by_group_topk = {(row["group"], row["top_k"]): row for row in hard_rows}

    rows = []
    for group, stats in positive.items():
        for top_k in args.top_k:
            hard = hard_by_group_topk.get((group, min(top_k, max(1, n - 1))), {})
            rows.append(
                {
                    "dataset": args.dataset,
                    "group": group,
                    "top_k": top_k,
                    **stats,
                    "hard_negative_same_class_rate": hard.get("hard_negative_same_class_rate", "NaN"),
                    "hard_negative_cross_class_rate": hard.get("hard_negative_cross_class_rate", "NaN"),
                    "hard_negative_false_negative_rate": hard.get("hard_negative_false_negative_rate", "NaN"),
                    "embedding_source": "provided_embeddings",
                    "labels_posthoc_only": True,
                }
            )

    write_csv_rows(args.output, FIELDNAMES, rows, append=not args.overwrite)
    logger.info("Wrote embedding pair reliability diagnostics to %s", args.output)


if __name__ == "__main__":
    main()

