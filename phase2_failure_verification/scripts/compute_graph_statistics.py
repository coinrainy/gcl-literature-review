from __future__ import annotations

import argparse

from utils import graph_statistics, load_graph_data, setup_logger, set_random_seed, write_csv_rows


FIELDNAMES = [
    "dataset",
    "source",
    "num_nodes",
    "num_edges",
    "num_features",
    "num_classes",
    "global_edge_homophily",
    "local_node_homophily_mean",
    "local_node_homophily_std",
    "degree_mean",
    "degree_std",
    "class_distribution",
    "same_class_edge_ratio",
    "cross_class_edge_ratio",
    "labels_posthoc_only",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute graph statistics for Phase 2 failure verification.")
    parser.add_argument("--dataset", required=True, help="Dataset name, e.g., Cora or Chameleon.")
    parser.add_argument("--data-root", default="data", help="Root directory for PyG datasets.")
    parser.add_argument("--npz-path", default=None, help="Optional custom npz with edge_index/edges, x/features, y/labels.")
    parser.add_argument("--edge-index-path", default=None, help="Optional CSV/NPY edge index with shape [2,E] or [E,2].")
    parser.add_argument("--features-path", default=None, help="Optional CSV/NPY node feature matrix.")
    parser.add_argument("--labels-path", default=None, help="Optional CSV/NPY node labels for post-hoc diagnostics.")
    parser.add_argument(
        "--output",
        default="phase2_failure_verification/outputs/tables/graph_statistics.csv",
        help="CSV output path.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output instead of appending.")
    parser.add_argument("--log-path", default=None, help="Optional log file path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_random_seed(args.seed)
    logger = setup_logger(log_path=args.log_path)
    logger.info("Loading dataset %s", args.dataset)
    graph = load_graph_data(
        dataset=args.dataset,
        data_root=args.data_root,
        edge_index_path=args.edge_index_path,
        features_path=args.features_path,
        labels_path=args.labels_path,
        npz_path=args.npz_path,
    )
    logger.info("Computing graph statistics from source=%s", graph.source)
    row = graph_statistics(graph)
    write_csv_rows(args.output, FIELDNAMES, [row], append=not args.overwrite)
    logger.info("Wrote graph statistics to %s", args.output)


if __name__ == "__main__":
    main()

