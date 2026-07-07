from __future__ import annotations

import argparse
import math

import numpy as np

from utils import (
    degree_vector,
    drop_edges,
    edge_preservation_by_label,
    homophily_group_masks,
    infer_num_nodes,
    load_graph_data,
    mask_features,
    neighborhood_semantic_drift,
    positive_similarity_summary,
    read_array,
    safe_mean,
    safe_std,
    set_random_seed,
    setup_logger,
    unique_undirected_edges,
    write_csv_rows,
    local_node_homophily,
)


FIELDNAMES = [
    "dataset",
    "source",
    "augmentation_type",
    "augmentation_rate",
    "trial",
    "local_homophily_group",
    "num_nodes_in_group",
    "retained_same_class_edges",
    "retained_cross_class_edges",
    "dropped_same_class_edges",
    "dropped_cross_class_edges",
    "same_class_edge_retention_rate",
    "cross_class_edge_retention_rate",
    "neighbor_label_distribution_js_divergence",
    "neighbor_label_distribution_js_divergence_std",
    "neighbor_label_distribution_l1_distance",
    "local_homophily_change",
    "positive_pair_cosine_similarity",
    "positive_pair_rank",
    "positive_pair_similarity_drop",
    "low_reliability_positive_ratio",
    "positive_nodes_evaluated",
    "embedding_source",
    "labels_posthoc_only",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate positive view failure under graph augmentations.")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--npz-path", default=None)
    parser.add_argument("--edge-index-path", default=None)
    parser.add_argument("--features-path", default=None)
    parser.add_argument("--labels-path", default=None)
    parser.add_argument("--augmentation", choices=["edge_drop", "feature_mask", "both"], default="edge_drop")
    parser.add_argument("--rates", nargs="+", type=float, default=[0.1, 0.2, 0.4, 0.6, 0.8])
    parser.add_argument("--num-trials", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--feature-mask-mode", choices=["feature", "element"], default="feature")
    parser.add_argument("--view1-embedding", default=None, help="Optional embeddings for original view.")
    parser.add_argument("--view2-embedding", default=None, help="Optional embeddings for augmented view.")
    parser.add_argument("--positive-threshold", type=float, default=None)
    parser.add_argument("--max-rank-nodes", type=int, default=2000)
    parser.add_argument(
        "--output",
        default="phase2_failure_verification/outputs/tables/positive_view_failure.csv",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--log-path", default=None)
    return parser.parse_args()


def _embedding_views(args: argparse.Namespace, features: np.ndarray | None, augmented_features: np.ndarray | None):
    if args.view1_embedding and args.view2_embedding:
        return read_array(args.view1_embedding), read_array(args.view2_embedding), "provided_embeddings"
    if features is not None and augmented_features is not None:
        return features, augmented_features, "raw_feature_proxy"
    return None, None, "not_available"


def main() -> None:
    args = parse_args()
    rng = set_random_seed(args.seed)
    logger = setup_logger(log_path=args.log_path)
    graph = load_graph_data(
        args.dataset,
        data_root=args.data_root,
        edge_index_path=args.edge_index_path,
        features_path=args.features_path,
        labels_path=args.labels_path,
        npz_path=args.npz_path,
    )
    original_edges = unique_undirected_edges(graph.edge_index)
    num_nodes = infer_num_nodes(graph.edge_index, graph.features, graph.labels)
    original_local_h = local_node_homophily(num_nodes, original_edges, graph.labels)
    group_masks = homophily_group_masks(original_local_h)
    group_masks["all"] = np.ones(num_nodes, dtype=bool)
    rows = []

    logger.info("Running positive view diagnostics for %s", graph.name)
    for trial in range(args.num_trials):
        for rate in args.rates:
            if args.augmentation in {"edge_drop", "both"}:
                augmented_edges = drop_edges(original_edges, rate, rng)
            else:
                augmented_edges = original_edges.copy()

            if graph.features is not None and args.augmentation in {"feature_mask", "both"}:
                augmented_features = mask_features(graph.features, rate, rng, mode=args.feature_mask_mode)
            else:
                augmented_features = graph.features

            edge_stats = edge_preservation_by_label(original_edges, augmented_edges, graph.labels)
            drift = neighborhood_semantic_drift(num_nodes, original_edges, augmented_edges, graph.labels)
            view1, view2, embedding_source = _embedding_views(args, graph.features, augmented_features)
            positive_stats = {}
            if view1 is not None and view2 is not None:
                positive_stats = positive_similarity_summary(
                    view1,
                    view2,
                    graph.labels,
                    group_masks,
                    threshold=args.positive_threshold,
                    max_rank_nodes=args.max_rank_nodes,
                    seed=args.seed + trial,
                )

            for group, mask in group_masks.items():
                stats = positive_stats.get(
                    group,
                    {
                        "positive_pair_cosine_similarity": math.nan,
                        "positive_pair_rank": math.nan,
                        "positive_pair_similarity_drop": math.nan,
                        "low_reliability_positive_ratio": math.nan,
                        "positive_nodes_evaluated": 0,
                    },
                )
                rows.append(
                    {
                        "dataset": graph.name,
                        "source": graph.source,
                        "augmentation_type": args.augmentation,
                        "augmentation_rate": rate,
                        "trial": trial,
                        "local_homophily_group": group,
                        "num_nodes_in_group": int(mask.sum()),
                        **edge_stats,
                        "neighbor_label_distribution_js_divergence": safe_mean(
                            drift["neighbor_label_distribution_js_divergence"][mask]
                        ),
                        "neighbor_label_distribution_js_divergence_std": safe_std(
                            drift["neighbor_label_distribution_js_divergence"][mask]
                        ),
                        "neighbor_label_distribution_l1_distance": safe_mean(
                            drift["neighbor_label_distribution_l1_distance"][mask]
                        ),
                        "local_homophily_change": safe_mean(drift["local_homophily_change"][mask]),
                        **stats,
                        "embedding_source": embedding_source,
                        "labels_posthoc_only": True,
                    }
                )

    write_csv_rows(args.output, FIELDNAMES, rows, append=not args.overwrite)
    logger.info("Wrote positive view diagnostics to %s", args.output)


if __name__ == "__main__":
    main()

